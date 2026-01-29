"""
LangGraph Agent Graph
Main agent graph definition and execution.
"""

from typing import Any, Dict, Optional
import asyncio
from datetime import datetime

from langgraph.graph import StateGraph, END

from app.agent.state import LegalAgentState, create_initial_state
from app.agent.nodes import (
    intake_node,
    classify_node,
    clarification_node,
    retrieve_node,
    response_node,
    safety_node,
    memory_node,
    error_node
)
from app.llm.router import get_llm
from app.config import settings
from app.utils.logger import logger


def create_agent_graph() -> StateGraph:
    """
    Create the LangGraph state machine for the legal triage agent.
    
    Returns:
        Configured StateGraph
    """
    # Initialize graph with state schema
    graph = StateGraph(LegalAgentState)
    
    # Add nodes
    graph.add_node("intake", intake_node)
    graph.add_node("classify", classify_node)
    graph.add_node("clarify", clarification_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("respond", response_node)
    graph.add_node("validate", safety_node)
    graph.add_node("memory", memory_node)
    graph.add_node("error", error_node)
    
    # Set entry point
    graph.set_entry_point("intake")
    
    # Add edges
    
    # Intake -> Classify
    graph.add_edge("intake", "classify")
    
    # Classify -> Clarify OR Retrieve (conditional)
    graph.add_conditional_edges(
        "classify",
        _route_after_classify,
        {
            "clarify": "clarify",
            "retrieve": "retrieve",
            "error": "error"
        }
    )
    
    # Clarify -> END (wait for user input)
    graph.add_edge("clarify", END)
    
    # Retrieve -> Respond
    graph.add_edge("retrieve", "respond")
    
    # Respond -> Validate
    graph.add_edge("respond", "validate")
    
    # Validate -> Memory
    graph.add_edge("validate", "memory")
    
    # Memory -> END
    graph.add_edge("memory", END)
    
    # Error -> END
    graph.add_edge("error", END)
    
    return graph


def _route_after_classify(state: LegalAgentState) -> str:
    """
    Routing function after classification.
    Determines whether to ask for clarification or proceed to retrieval.
    """
    # Check for errors
    if state.get("error"):
        return "error"
    
    # Check if clarification needed
    if state.get("needs_clarification", False):
        # Check if we've exceeded max clarification loops
        if state.get("clarification_count", 0) >= settings.max_clarification_loops:
            logger.warning("Max clarification loops reached, proceeding to retrieval")
            return "retrieve"
        return "clarify"
    
    return "retrieve"


class LegalTriageAgent:
    """
    Main agent class that wraps the LangGraph.
    Provides a clean interface for running the agent.
    """
    
    def __init__(self, llm_provider: Optional[str] = None):
        """
        Initialize the agent.
        
        Args:
            llm_provider: LLM provider to use
        """
        self.llm_provider = llm_provider or settings.llm_provider
        self.graph = create_agent_graph()
        self._compiled_graph = None
    
    @property
    def compiled_graph(self):
        """Get or create compiled graph."""
        if self._compiled_graph is None:
            self._compiled_graph = self.graph.compile()
        return self._compiled_graph
    
    async def run(self, state: LegalAgentState) -> LegalAgentState:
        """
        Run the agent with the given state.
        
        Args:
            state: Initial agent state
            
        Returns:
            Final agent state
        """
        try:
            # Get LLM
            llm = get_llm(self.llm_provider)
            
            # Create node wrappers that inject LLM
            async def run_node(node_func, node_state):
                return await node_func(node_state, llm)
            
            # Run through the graph manually to inject LLM
            current_state = state.copy()
            
            # Execute intake
            current_state = await intake_node(current_state, llm)
            
            # Check if intake ended early
            if current_state["current_node"] == "end":
                return current_state
            
            # Execute classify
            current_state = await classify_node(current_state, llm)
            
            # Route based on classification
            if current_state["needs_clarification"]:
                if current_state["clarification_count"] < settings.max_clarification_loops:
                    current_state = await clarification_node(current_state, llm)
                    return current_state
            
            # Execute retrieve
            current_state = await retrieve_node(current_state, llm)
            
            # Execute respond
            current_state = await response_node(current_state, llm)
            
            # Execute safety validation
            current_state = await safety_node(current_state, llm)
            
            # Execute memory
            current_state = await memory_node(current_state, llm)
            
            return current_state
            
        except Exception as e:
            logger.error(f"Agent execution error: {str(e)}")
            state["error"] = str(e)
            state = await error_node(state, None)
            return state


# Convenience function for API use
async def run_agent(
    state: LegalAgentState,
    llm_provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run the legal triage agent.
    
    Args:
        state: Initial agent state
        llm_provider: Optional LLM provider override
        
    Returns:
        Final state as dictionary
    """
    agent = LegalTriageAgent(llm_provider)
    final_state = await agent.run(state)
    
    # Log execution
    logger.info(
        f"Agent execution complete: session={state['session_id']}, "
        f"nodes={len(final_state.get('logs', []))}, "
        f"confidence={final_state.get('confidence', 0)}"
    )
    
    return dict(final_state)


# Synchronous wrapper for testing
def run_agent_sync(
    state: LegalAgentState,
    llm_provider: Optional[str] = None
) -> Dict[str, Any]:
    """Synchronous wrapper for run_agent."""
    return asyncio.run(run_agent(state, llm_provider))