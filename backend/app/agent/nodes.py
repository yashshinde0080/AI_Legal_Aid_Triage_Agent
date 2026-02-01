"""
Agent Nodes
LangGraph node implementations for the agent state machine.
This module integrates specialized agents from app.agents package.
"""

from typing import List
from datetime import datetime

from app.agent.state import LegalAgentState, ClassificationResult, RetrievedDocument
from app.agents.intake_agent import IntakeAgent
from app.agents.classifier_agent import ClassifierAgent
from app.agents.clarification_agent import ClarificationAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.response_agent import ResponseAgent
from app.agents.safety_agent import SafetyAgent

from app.agent.prompts import (
    ERROR_RESPONSE,
    DISCLAIMER
)
from app.config import settings
from app.utils.logger import logger


async def intake_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Intake Node: Normalize input and attach context.
    """
    logger.info(f"Intake node processing: session={state['session_id']}")
    
    agent = IntakeAgent()
    
    # Run intake processing
    result = await agent.process(
        user_input=state["user_input"],
        chat_history=state["chat_history"]
    )
    
    if not result["valid"]:
        state["response"] = result["error"] or "Please provide more details."
        state["needs_clarification"] = True
        
        # Log failure
        state["logs"].append({
            "node": "intake",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "invalid_input",
            "error": result["error"]
        })
        
        state["current_node"] = "end" 
        return state
        
    # Update input with cleaned version
    state["user_input"] = result["cleaned_input"]
    
    # Log node entry
    state["logs"].append({
        "node": "intake",
        "timestamp": datetime.utcnow().isoformat(),
        "input_length": len(state["user_input"]),
        "is_followup": result["is_followup"]
    })
    
    state["current_node"] = "classify"
    return state


async def classify_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Classification Node: Classify the legal issue.
    """
    logger.info(f"Classify node processing: session={state['session_id']}")
    
    agent = ClassifierAgent(llm)
    
    # Build context string for classifier
    context = _build_context(state["chat_history"])
    
    # Run classification
    result = await agent.classify(
        user_input=state["user_input"],
        context=context
    )
    
    # Update state
    state["classification"] = ClassificationResult(
        domain=result.get("domain", "Unknown"),
        sub_domain=result.get("sub_domain", "Unknown"),
        confidence=result.get("confidence", 0.0),
        missing_fields=result.get("missing_fields", [])
    )
    state["confidence"] = result.get("confidence", 0.0)
    
    # Check if max clarification loops reached
    loop_limit_reached = state["clarification_count"] >= settings.max_clarification_loops
    
    # Determine if clarification needed
    # Only if confidence is low AND we haven't asked too many questions
    state["needs_clarification"] = (
        state["confidence"] < settings.confidence_threshold and
        not loop_limit_reached
    )
    
    if loop_limit_reached and state["confidence"] < settings.confidence_threshold:
        logger.warning("Max clarification loops reached. Forcing retrieval with best guess.")
    
    # Log
    state["logs"].append({
        "node": "classify",
        "timestamp": datetime.utcnow().isoformat(),
        "classification": state["classification"],
        "confidence": state["confidence"],
        "needs_clarification": state["needs_clarification"],
        "loop_count": state["clarification_count"]
    })
    
    state["current_node"] = "clarify" if state["needs_clarification"] else "retrieve"
    return state


async def clarification_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Clarification Node: Ask clarifying questions.
    """
    logger.info(f"Clarification node processing: session={state['session_id']}")
    
    agent = ClarificationAgent(llm)
    
    # Extract previously asked questions from history
    asked_questions = _extract_asked_questions(state["chat_history"])
    
    # Generate question
    result = await agent.generate_question(
        missing_fields=state["classification"]["missing_fields"],
        classification=state["classification"],
        user_input=state["user_input"],
        asked_questions=asked_questions
    )
    
    question = result["question"]
    
    state["clarification_question"] = question
    state["clarification_count"] += 1
    state["response"] = question
    
    # Log
    state["logs"].append({
        "node": "clarify",
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "details": result
    })
    
    state["current_node"] = "end"
    return state


async def retrieve_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Retrieval Node: Retrieve relevant legal documents.
    """
    logger.info(f"Retrieve node processing: session={state['session_id']}")
    
    agent = RetrieverAgent()
    classification = state["classification"]
    
    # Run retrieval
    result = await agent.retrieve(
        query=state["user_input"],
        domain=classification["domain"],
        sub_domain=classification["sub_domain"],
        k=5
    )
    
    # Convert dict docs to TypedDict format
    docs = []
    for doc in result.get("documents", []):
        docs.append(RetrievedDocument(
            id=doc.get("id", ""),
            content=doc.get("content", ""),
            title=doc.get("title", ""),
            section=doc.get("section", ""),
            source_url=doc.get("source_url"),
            score=doc.get("relevance_score", 0.0)
        ))
    
    state["retrieved_docs"] = docs
    
    # Log
    state["logs"].append({
        "node": "retrieve",
        "timestamp": datetime.utcnow().isoformat(),
        "doc_count": len(docs),
        "query": result.get("query", "")
    })
    
    state["current_node"] = "respond"
    return state


async def response_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Response Node: Generate procedural guidance.
    """
    logger.info(f"Response node processing: session={state['session_id']}")
    
    try:
        agent = ResponseAgent(llm)
        
        # Prepare retrieved docs in dict format expected by agent
        # (Actually RetreiverAgent returns dicts, but we converted to TypedDict in state)
        # We need to convert back or ensure agent handles it. 
        # ResponseAgent expects List[Dict]. RetrievedDocument is a TypedDict (which is a dict at runtime).
        # So passing state["retrieved_docs"] directly works.
        
        # Run generation
        result = await agent.generate(
            user_input=state["user_input"],
            classification=state["classification"],
            retrieved_docs=state["retrieved_docs"],
            chat_history=state["chat_history"]
        )
        
        full_response = result["response"]
        
        # Ensure disclaimer is present if agent didn't add it (it usually does or we add it)
        if DISCLAIMER not in full_response:
             full_response += f"\n\n{DISCLAIMER}"
        
        state["response"] = full_response
        
        # Log
        state["logs"].append({
            "node": "respond",
            "timestamp": datetime.utcnow().isoformat(),
            "response_length": len(full_response)
        })
        
        state["current_node"] = "validate"
        return state
        
    except Exception as e:
        logger.error(f"Response generation error: {str(e)}")
        state["response"] = ERROR_RESPONSE
        state["error"] = str(e)
        state["current_node"] = "end"
        return state


async def safety_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Safety Node: Validate response for safety.
    """
    logger.info(f"Safety node processing: session={state['session_id']}")
    
    try:
        agent = SafetyAgent(llm)
        
        # Validate response
        validation = await agent.validate(state["response"])
        
        if not validation["valid"]:
            logger.warning(f"Safety check failed: {validation['violations']}")
            
            # Use sanitized response if available, or fallback
            if validation.get("sanitized_response"):
                state["response"] = validation["sanitized_response"]
            else:
                state["response"] = (
                    "I can only provide general procedural guidance. "
                    "For specific advice on your situation, please consult with a qualified legal professional.\n\n"
                    f"{DISCLAIMER}"
                )
        
        # Log
        state["logs"].append({
            "node": "safety",
            "timestamp": datetime.utcnow().isoformat(),
            "valid": validation["valid"],
            "check_type": validation.get("check_type", "unknown")
        })
        
    except Exception as e:
        logger.error(f"Safety validation error: {str(e)}")
        # Log error but don't block
        state["logs"].append({
            "node": "safety",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        })
    
    state["current_node"] = "memory" # Should go to memory node next, or end
    # Graph definition says: Validate -> Memory -> END
    return state


async def memory_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Memory Node: Handle memory persistence.
    """
    logger.info(f"Memory node processing: session={state['session_id']}")
    
    # Persistence is handled by API layer, this node logs completion
    state["logs"].append({
        "node": "memory",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "complete"
    })
    
    state["current_node"] = "end"
    return state


async def error_node(state: LegalAgentState, llm) -> LegalAgentState:
    """
    Error Node: Handle errors gracefully.
    """
    logger.error(f"Error node processing: session={state['session_id']}, error={state.get('error')}")
    
    state["response"] = ERROR_RESPONSE
    
    state["logs"].append({
        "node": "error",
        "timestamp": datetime.utcnow().isoformat(),
        "error": state.get("error", "Unknown error")
    })
    
    state["current_node"] = "end"
    return state


# Helper functions

def _build_context(chat_history: list) -> str:
    """Build context string from chat history."""
    if not chat_history:
        return "No previous context."
    
    context_parts = []
    # Take last 5 messages for context
    recent_messages = chat_history[-5:]
    
    for msg in recent_messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")[:500]  # Truncate long messages
        context_parts.append(f"{role}: {content}")
    
    return "\n".join(context_parts)


def _extract_asked_questions(chat_history: list) -> List[str]:
    """Extract previously asked questions from chat history."""
    questions = []
    if not chat_history:
        return questions
        
    for msg in chat_history:
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            # Simple heuristic: if it ends with '?' or was a clarification (check metadata if available)
            # Since we maintain 'needs_clarification' in metadata now, check that first
            meta = msg.get("metadata", {})
            if meta.get("needs_clarification"):
                questions.append(content)
            elif "?" in content:
                questions.append(content)
                
    return questions
