"""
Agent Tools
LangChain tools used by the agent nodes.
"""

from typing import Dict, Any, List, Optional
import json

from langchain_core.tools import tool
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import (
    CLASSIFICATION_PROMPT,
    CLARIFICATION_PROMPT,
    SAFETY_PROMPT
)
from app.db.vector import VectorStore
from app.utils.logger import logger


class ClassifierTool:
    """Tool for classifying legal issues."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def run(
        self, 
        user_input: str, 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Classify a legal issue.
        
        Args:
            user_input: User's description of the issue
            context: Previous conversation context
            
        Returns:
            Classification result with domain, sub_domain, confidence, missing_fields
        """
        try:
            prompt = CLASSIFICATION_PROMPT.format(
                user_input=user_input,
                context=context
            )
            
            messages = [
                SystemMessage(content="You are a legal issue classifier. Respond only in JSON format."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Parse JSON response
            result = self._parse_json_response(response.content)
            
            return result
            
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return {
                "domain": "Unknown",
                "sub_domain": "Unknown",
                "confidence": 0.0,
                "missing_fields": ["unable to classify"]
            }
    
    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON from LLM response."""
        try:
            # Try to extract JSON from response
            content = content.strip()
            
            # Handle markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON: {content}")
            return {
                "domain": "Unknown",
                "sub_domain": "Unknown",
                "confidence": 0.0,
                "missing_fields": ["classification failed"]
            }


class ClarificationTool:
    """Tool for generating clarifying questions."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def run(
        self,
        missing_fields: List[str],
        classification: Dict[str, Any],
        user_input: str
    ) -> str:
        """
        Generate a clarifying question.
        
        Args:
            missing_fields: List of missing information fields
            classification: Current classification result
            user_input: Original user input
            
        Returns:
            Clarifying question string
        """
        try:
            prompt = CLARIFICATION_PROMPT.format(
                missing_fields=", ".join(missing_fields),
                classification=json.dumps(classification),
                user_input=user_input
            )
            
            messages = [
                SystemMessage(content="You are a helpful legal aid assistant."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Clarification error: {str(e)}")
            return "Could you please provide more details about your situation?"


class RetrieverTool:
    """Tool for retrieving relevant legal documents."""
    
    def __init__(self):
        self.vector_store = VectorStore()
    
    async def run(
        self,
        query: str,
        domain: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant legal documents.
        
        Args:
            query: Search query
            domain: Optional domain filter
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            documents = await self.vector_store.similarity_search(
                query=query,
                k=k,
                filter_domain=domain
            )
            
            return documents
            
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return []


class SafetyValidatorTool:
    """Tool for validating response safety."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def run(self, response: str) -> Dict[str, Any]:
        """
        Validate response for safety violations.
        
        Args:
            response: Response to validate
            
        Returns:
            Validation result with valid flag and violations
        """
        try:
            prompt = SAFETY_PROMPT.format(response=response)
            
            messages = [
                SystemMessage(content="You are a safety validator. Respond only in JSON format."),
                HumanMessage(content=prompt)
            ]
            
            result = await self.llm.ainvoke(messages)
            
            # Parse response
            validation = self._parse_json_response(result.content)
            
            return validation
            
        except Exception as e:
            logger.error(f"Safety validation error: {str(e)}")
            # Default to valid to avoid blocking
            return {"valid": True, "violations": [], "suggested_fix": None}
    
    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON from LLM response."""
        try:
            content = content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
        except json.JSONDecodeError:
            return {"valid": True, "violations": [], "suggested_fix": None}


from app.utils.guardrails import check_guardrails

# Quick validation functions (rule-based, no LLM)
def quick_safety_check(response: str) -> Dict[str, Any]:
    """
    Quick rule-based safety check without LLM.
    Use for fast validation before LLM validation.
    """
    result = check_guardrails(response)
    
    # Adapt format to match what nodes.py expects
    return {
        "valid": result["valid"],
        "violations": [v["description"] for v in result["violations"]]
    }