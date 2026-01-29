"""
Conversation Summarizer
Summarizes long conversations to manage context size.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.utils.logger import logger


SUMMARIZATION_PROMPT = """You are summarizing a legal aid conversation.

Create a concise summary that captures:
1. Main legal issue(s) discussed
2. Classification/domain identified
3. Key facts provided by user
4. Procedural guidance given
5. Current status/outstanding questions

Keep the summary under 300 words. Focus on facts relevant for continuing the conversation.

Conversation:
{conversation}

Summary:
"""


class ConversationSummarizer:
    """
    Summarizes long conversations to manage token limits.
    """
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.max_summary_tokens = 500
    
    async def summarize(
        self,
        messages: List[Dict[str, Any]],
        existing_summary: Optional[str] = None
    ) -> str:
        """
        Summarize a conversation.
        
        Args:
            messages: List of messages to summarize
            existing_summary: Previous summary to incorporate
            
        Returns:
            Summary text
        """
        try:
            # Format conversation
            conversation = self._format_messages(messages)
            
            # Include existing summary if available
            if existing_summary:
                conversation = f"Previous summary:\n{existing_summary}\n\nNew messages:\n{conversation}"
            
            prompt = SUMMARIZATION_PROMPT.format(conversation=conversation)
            
            llm_messages = [
                SystemMessage(content="You are a conversation summarizer for legal aid."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(llm_messages)
            
            summary = response.content.strip()
            
            logger.info(f"Generated summary of {len(messages)} messages")
            
            return summary
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            return self._fallback_summary(messages)
    
    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for summarization."""
        formatted = []
        
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            
            # Truncate very long messages
            if len(content) > 500:
                content = content[:500] + "..."
            
            formatted.append(f"{role}: {content}")
        
        return "\n\n".join(formatted)
    
    def _fallback_summary(self, messages: List[Dict[str, Any]]) -> str:
        """Generate a basic summary without LLM."""
        user_messages = [m for m in messages if m.get("role") == "user"]
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        
        summary_parts = []
        
        if user_messages:
            first_issue = user_messages[0].get("content", "")[:200]
            summary_parts.append(f"Initial query: {first_issue}")
        
        summary_parts.append(f"Total exchanges: {len(messages)}")
        
        if assistant_messages:
            last_response = assistant_messages[-1].get("content", "")[:200]
            summary_parts.append(f"Last guidance: {last_response}")
        
        return " | ".join(summary_parts)
    
    def should_summarize(
        self,
        message_count: int,
        estimated_tokens: int,
        threshold_messages: int = 20,
        threshold_tokens: int = 4000
    ) -> bool:
        """
        Determine if summarization is needed.
        
        Args:
            message_count: Number of messages
            estimated_tokens: Estimated token count
            threshold_messages: Message count threshold
            threshold_tokens: Token count threshold
            
        Returns:
            True if summarization needed
        """
        return message_count > threshold_messages or estimated_tokens > threshold_tokens