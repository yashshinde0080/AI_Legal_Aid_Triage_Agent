"""
Response Agent
Generates procedural guidance responses.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import DISCLAIMER
from app.utils.logger import logger


RESPONSE_SYSTEM_PROMPT = """You are a legal aid assistant providing PROCEDURAL GUIDANCE for Indian citizens.

Your role is to explain legal PROCEDURES - what steps to take, where to go, what to file.

STRICT RULES YOU MUST FOLLOW:
1. ONLY provide procedural steps (what to do, where to go, what to file)
2. NEVER give legal advice ("you should sue", "you will win")
3. NEVER predict case outcomes
4. ALWAYS cite relevant acts and sections when available
5. Use simple, clear language (assume user has no legal background)
6. Include relevant authorities (which court, tribunal, police station)
7. Mention time limits and deadlines if applicable
8. Always suggest consulting a legal professional for specific advice

RESPONSE STRUCTURE:
1. Brief acknowledgment of the issue
2. Applicable law (act name and relevant sections)
3. Step-by-step procedure
4. Relevant authorities
5. Required documents
6. Time limits (if any)
7. Where to get free legal help

Remember: You are a guide, not a lawyer. Provide the map, not the journey.
"""


class ResponseAgent:
    """
    Response Agent: Generates procedural guidance responses.
    
    Responsibilities:
    - Convert retrieved laws into steps
    - Stay procedural
    - Cite sections
    - Avoid advice language
    """
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def generate(
        self,
        user_input: str,
        classification: Dict[str, Any],
        retrieved_docs: List[Dict[str, Any]],
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate procedural guidance response.
        
        Args:
            user_input: User's query
            classification: Issue classification
            retrieved_docs: Retrieved legal documents
            chat_history: Conversation history
            
        Returns:
            Generated response with metadata
        """
        try:
            # Format documents for prompt
            docs_text = self._format_documents(retrieved_docs)
            
            # Format chat history
            history_text = self._format_history(chat_history)
            
            # Build prompt
            user_prompt = f"""
Issue Classification:
- Legal Domain: {classification.get('domain', 'Unknown')}
- Specific Issue: {classification.get('sub_domain', 'Unknown')}

User's Situation:
{user_input}

Relevant Legal Information:
{docs_text}

Previous Conversation:
{history_text}

Please provide procedural guidance for this legal issue:
"""
            
            messages = [
                SystemMessage(content=RESPONSE_SYSTEM_PROMPT),
                HumanMessage(content=user_prompt)
            ]
            
            # Generate response
            response = await self.llm.ainvoke(messages)
            
            # Add disclaimer
            full_response = response.content.strip()
            
            # Add sources
            sources = self._extract_sources(retrieved_docs)
            
            return {
                "response": full_response,
                "sources": sources,
                "classification": classification,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Response generation error: {str(e)}")
            return {
                "response": self._fallback_response(classification),
                "sources": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _format_documents(self, docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents for prompt."""
        if not docs:
            return "No specific legal documents found. Provide general guidance based on the classification."
        
        formatted = []
        for i, doc in enumerate(docs[:3], 1):  # Limit to top 3
            formatted.append(f"""
Document {i}:
- Act/Law: {doc.get('title', 'Unknown')}
- Section: {doc.get('section', 'N/A')}
- Content: {doc.get('content', '')[:1000]}
""")
        
        return "\n".join(formatted)
    
    def _format_history(self, history: Optional[List[Dict[str, Any]]]) -> str:
        """Format chat history for prompt."""
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-5:]:  # Last 5 messages
            role = "User" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content", "")[:300]
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    def _extract_sources(self, docs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract source information from documents."""
        sources = []
        seen = set()
        
        for doc in docs:
            title = doc.get("title", "")
            section = doc.get("section", "")
            
            key = f"{title}_{section}"
            if key not in seen:
                seen.add(key)
                sources.append({
                    "title": title,
                    "section": section,
                    "url": doc.get("source_url", "")
                })
        
        return sources
    
    def _fallback_response(self, classification: Dict[str, Any]) -> str:
        """Generate fallback response on error."""
        domain = classification.get("domain", "legal")
        
        return f"""I understand you have a {domain.lower()} related issue.

While I couldn't retrieve specific legal documents at this moment, here are some general steps you can take:

1. **Document Everything**: Keep records of all relevant documents, communications, and evidence.

2. **Seek Legal Aid**: Contact your nearest Legal Services Authority for free legal assistance:
   - National Legal Services Authority (NALSA): 15100
   - Visit: https://nalsa.gov.in

3. **File a Complaint**: Depending on your issue:
   - Consumer complaints: https://consumerhelpline.gov.in
   - General grievances: https://pgportal.gov.in

4. **Consult a Lawyer**: For specific advice on your situation, please consult a qualified legal professional.

{DISCLAIMER}
"""
    
    def add_disclaimer(self, response: str) -> str:
        """Add standard disclaimer to response."""
        return f"{response}\n\n{DISCLAIMER}"