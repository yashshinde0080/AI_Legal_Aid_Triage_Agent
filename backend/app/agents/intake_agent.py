"""
Intake Agent
Handles initial processing of user input and context attachment.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from app.utils.logger import logger


class IntakeAgent:
    """
    Intake Agent: Normalizes user input and attaches memory context.
    
    Responsibilities:
    - Clean and normalize user input
    - Attach short-term memory context
    - Detect follow-up vs new issue
    - Populate initial agent state
    """
    
    def __init__(self):
        self.max_input_length = 5000
        self.min_input_length = 5
    
    async def process(
        self,
        user_input: str,
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process user input through intake.
        
        Args:
            user_input: Raw user input
            chat_history: Previous conversation messages
            
        Returns:
            Processed input with context
        """
        # Clean input
        cleaned_input = self._clean_input(user_input)
        
        # Validate input
        validation = self._validate_input(cleaned_input)
        if not validation["valid"]:
            return {
                "valid": False,
                "error": validation["error"],
                "cleaned_input": cleaned_input
            }
        
        # Detect conversation type
        is_followup = self._detect_followup(cleaned_input, chat_history)
        
        # Build context
        context = self._build_context(chat_history)
        
        return {
            "valid": True,
            "cleaned_input": cleaned_input,
            "is_followup": is_followup,
            "context": context,
            "context_length": len(context),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize user input."""
        if not text:
            return ""
        
        # Strip whitespace
        cleaned = text.strip()
        
        # Remove excessive whitespace
        import re
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Truncate if too long
        if len(cleaned) > self.max_input_length:
            cleaned = cleaned[:self.max_input_length]
        
        return cleaned
    
    def _validate_input(self, text: str) -> Dict[str, Any]:
        """Validate user input."""
        if not text:
            return {
                "valid": False,
                "error": "Please provide a description of your legal issue."
            }
        
        if len(text) < self.min_input_length:
            return {
                "valid": False,
                "error": "Please provide more details about your situation."
            }
        
        # Check for gibberish (very basic check)
        words = text.split()
        if len(words) < 2:
            return {
                "valid": False,
                "error": "Please describe your legal issue in more detail."
            }
        
        return {"valid": True, "error": None}
    
    def _detect_followup(
        self,
        current_input: str,
        chat_history: Optional[List[Dict[str, Any]]]
    ) -> bool:
        """Detect if this is a follow-up to previous conversation."""
        if not chat_history:
            return False
        
        # Check for follow-up indicators
        followup_indicators = [
            "what about",
            "and also",
            "additionally",
            "moreover",
            "regarding that",
            "about that",
            "you mentioned",
            "as i said",
            "like i mentioned"
        ]
        
        current_lower = current_input.lower()
        
        for indicator in followup_indicators:
            if indicator in current_lower:
                return True
        
        # Check for pronouns referring to previous context
        pronouns = ["it", "this", "that", "they", "them"]
        words = current_lower.split()
        
        if words and words[0] in pronouns:
            return True
        
        return False
    
    def _build_context(
        self,
        chat_history: Optional[List[Dict[str, Any]]],
        max_messages: int = 10
    ) -> str:
        """Build context string from chat history."""
        if not chat_history:
            return ""
        
        # Take recent messages
        recent = chat_history[-max_messages:]
        
        context_parts = []
        for msg in recent:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            
            # Truncate long messages
            if len(content) > 500:
                content = content[:500] + "..."
            
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)