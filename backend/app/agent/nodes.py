"""
Agent Nodes
LangGraph node implementations for the agent state machine.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel

from app.agent.state import LegalAgentState, ClassificationResult
from app.agent.tools import (
    ClassifierTool,
    ClarificationTool,
    RetrieverTool,
    SafetyValidatorTool,
    quick_safety_check
)
from app.agent.prompts import (
    RESPONSE_PROMPT,
    DISCLAIMER,
    ERROR_RESPONSE,
    OUT_OF_SCOPE_RESPONSE
)
from app.config import settings
from app.utils.logger import logger


async def intake_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Intake Node: Normalize input and attach context.
    
    This is the entry point for processing user input.
    """
    logger.info(f"Intake node processing: session={state['session_id']}")
    
    # Log node entry
    state["logs"].append({
        "node": "intake",
        "timestamp": datetime.utcnow().isoformat(),
        "input": state["user_input"][:100]
    })
    
    # Clean and normalize input
    user_input = state["user_input"].strip()
    
    # Check for empty or too short input
    if len(user_input) < 5:
        state["response"] = "Could you please provide more details about your legal question?"
        state["needs_clarification"] = True
        state["current_node"] = "intake"
        return state
    
    # Build context from chat history
    context = _build_context(state["chat_history"])
    
    state["current_node"] = "classify"
    return state


async def classify_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Classification Node: Classify the legal issue.
    """
    logger.info(f"Classify node processing: session={state['session_id']}")
    
    if not llm:
        raise ValueError("LLM is required for classification node")

    classifier = ClassifierTool(llm)
    
    # Build context from history
    context = _build_context(state["chat_history"])
    
    # Run classification
    result = await classifier.run(
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
    
    # Determine if clarification needed
    state["needs_clarification"] = (
        state["confidence"] < settings.confidence_threshold and
        state["clarification_count"] < settings.max_clarification_loops
    )
    
    # Log
    state["logs"].append({
        "node": "classify",
        "timestamp": datetime.utcnow().isoformat(),
        "classification": state["classification"],
        "confidence": state["confidence"]
    })
    
    state["current_node"] = "clarify" if state["needs_clarification"] else "retrieve"
    return state


async def clarification_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Clarification Node: Ask clarifying questions.
    """
    logger.info(f"Clarification node processing: session={state['session_id']}")
    
    if not llm:
        raise ValueError("LLM is required for clarification node")

    clarifier = ClarificationTool(llm)
    
    classification = state["classification"]
    if not classification:
        # Fallback if classification failed
        classification = {
            "domain": "Unknown",
            "sub_domain": "Unknown",
            "confidence": 0.0,
            "missing_fields": []
        }

    # Generate question
    question = await clarifier.run(
        missing_fields=classification["missing_fields"],
        classification=classification,  # type: ignore
        user_input=state["user_input"]
    )
    
    state["clarification_question"] = question
    state["clarification_count"] += 1
    state["response"] = question
    
    # Log
    state["logs"].append({
        "node": "clarify",
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "count": state["clarification_count"]
    })
    
    state["current_node"] = "end"
    return state


async def retrieve_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Retrieval Node: Retrieve relevant legal documents.
    """
    logger.info(f"Retrieve node processing: session={state['session_id']}")
    
    retriever = RetrieverTool()
    
    # Build search query
    classification = state["classification"]
    if not classification:
        classification = {
            "domain": "General",
            "sub_domain": "Law",
            "confidence": 0.0,
            "missing_fields": []
        }

    query = f"{classification['domain']} {classification['sub_domain']} procedure India"
    
    # Retrieve documents
    documents = await retriever.run(
        query=query,
        domain=classification["domain"],
        k=5
    )
    
    # Map to RetrievedDocument format
    mapped_docs = []
    for doc in documents:
        mapped_docs.append({
            "id": doc.get("id", ""),
            "content": doc.get("content", ""),
            "title": doc.get("act_name", "Unknown Act"),
            "section": doc.get("section", ""),
            "source_url": doc.get("source_url"),
            "score": doc.get("score", 0.0)
        })

    state["retrieved_docs"] = mapped_docs  # type: ignore
    
    # Log
    state["logs"].append({
        "node": "retrieve",
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "doc_count": len(documents)
    })
    
    state["current_node"] = "respond"
    return state


"""
Agent Nodes (continued)
LangGraph node implementations for the agent state machine.
"""

async def response_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Response Node: Generate procedural guidance.
    """
    logger.info(f"Response node processing: session={state['session_id']}")
    
    if not llm:
        state["error"] = "LLM is required for response node"
        state["current_node"] = "end"
        return state

    try:
        classification = state["classification"]
        if not classification:
            classification = {
                "domain": "General",
                "sub_domain": "Law",
                "confidence": 0.0,
                "missing_fields": []
            }
        
        # Format retrieved documents
        legal_docs = _format_retrieved_docs(state["retrieved_docs"])
        
        # Format chat history
        chat_history = _format_chat_history(state["chat_history"])
        
        # Build prompt
        prompt = RESPONSE_PROMPT.format(
            domain=classification["domain"],
            sub_domain=classification["sub_domain"],
            user_input=state["user_input"],
            legal_docs=legal_docs,
            chat_history=chat_history
        )
        
        messages = [
            SystemMessage(content="You are a legal aid assistant providing procedural guidance for Indian citizens. Never give legal advice."),
            HumanMessage(content=prompt)
        ]
        
        # Generate response
        response = await llm.ainvoke(messages)
        
        # Add disclaimer
        full_response = response.content.strip() + "\n\n" + DISCLAIMER
        
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


async def safety_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Safety Node: Validate response for safety.
    """
    logger.info(f"Safety node processing: session={state['session_id']}")
    
    # Quick rule-based check first
    quick_result = quick_safety_check(state["response"])
    
    if not quick_result["valid"]:
        logger.warning(f"Quick safety check failed: {quick_result['violations']}")
        state["response"] = _sanitize_response(state["response"], quick_result["violations"])
    
    # LLM-based validation for thorough check
    if not llm:
         # Skip LLM check if not available, but log warning
        logger.warning("LLM not available for safety node, skipping LLM validation")
        state["current_node"] = "end"
        return state

    try:
        validator = SafetyValidatorTool(llm)
        validation = await validator.run(state["response"])
        
        if not validation.get("valid", True):
            logger.warning(f"LLM safety check failed: {validation.get('violations')}")
            
            # Replace with safe response
            state["response"] = (
                "I can only provide general procedural guidance. "
                "For specific advice on your situation, please consult with a qualified legal professional.\n\n"
                f"{DISCLAIMER}"
            )
        
        # Log
        state["logs"].append({
            "node": "safety",
            "timestamp": datetime.utcnow().isoformat(),
            "quick_valid": quick_result["valid"],
            "llm_valid": validation.get("valid", True)
        })
        
    except Exception as e:
        logger.error(f"Safety validation error: {str(e)}")
        # On error, let response through but log it
        state["logs"].append({
            "node": "safety",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        })
    
    state["current_node"] = "end"
    return state


async def memory_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
    """
    Memory Node: Handle memory persistence.
    This node is called at the end to manage session memory.
    """
    logger.info(f"Memory node processing: session={state['session_id']}")
    
    # Memory persistence is handled in the API layer
    # This node is for any memory-related transformations
    
    state["logs"].append({
        "node": "memory",
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return state


async def error_node(state: LegalAgentState, llm: Optional[BaseChatModel] = None) -> LegalAgentState:
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


def _format_retrieved_docs(docs: list) -> str:
    """Format retrieved documents for prompt."""
    if not docs:
        return "No specific legal documents retrieved."
    
    formatted = []
    for i, doc in enumerate(docs[:3], 1):  # Limit to top 3
        formatted.append(f"""
Document {i}:
- Source: {doc.get('act_name', 'Unknown Act')}
- Section: {doc.get('section', 'N/A')}
- Content: {doc.get('content', '')[:800]}
""")
    
    return "\n".join(formatted)


def _format_chat_history(history: list) -> str:
    """Format chat history for prompt."""
    if not history:
        return "No previous conversation."
    
    formatted = []
    for msg in history[-5:]:
        role = "User" if msg.get("role") == "user" else "Assistant"
        content = msg.get("content", "")[:300]
        formatted.append(f"{role}: {content}")
    
    return "\n".join(formatted)


def _sanitize_response(response: str, violations: list) -> str:
    """Attempt to sanitize response based on violations."""
    sanitized = response
    
    # Simple replacement patterns
    replacements = {
        "you should definitely": "you may consider",
        "you must": "you may need to",
        "i advise you to": "one option is to",
        "i recommend that you": "you might consider",
        "you will win": "the outcome depends on various factors",
        "you will lose": "the outcome depends on various factors",
        "guaranteed": "possible",
        "100% certain": "subject to case-specific factors"
    }
    
    for old, new in replacements.items():
        sanitized = sanitized.lower().replace(old, new)
    
    return sanitized + f"\n\n{DISCLAIMER}"