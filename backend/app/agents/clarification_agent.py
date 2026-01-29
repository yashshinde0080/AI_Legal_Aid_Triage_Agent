"""
Clarification Agent
Generates targeted clarifying questions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.utils.logger import logger


CLARIFICATION_SYSTEM_PROMPT = """You are a legal aid assistant gathering information to help classify a legal issue.

Your task is to ask ONE clear, specific question to gather missing information.

Rules:
1. Ask only ONE question at a time
2. Be specific, not vague (ask for dates, amounts, locations, names of parties)
3. Use simple language that non-lawyers understand
4. Focus on facts, not opinions
5. Be polite and professional
6. Never ask for sensitive information like Aadhaar numbers or passwords

Good question examples:
- "When did this incident occur? (approximate date or month)"
- "What was the approximate amount involved?"
- "In which city/state did this happen?"
- "Was this a product you bought online or from a physical store?"

Bad question examples:
- "Can you tell me more?" (too vague)
- "What are the legal implications?" (user doesn't know)
- "What's your Aadhaar number?" (sensitive)
"""


# Question templates for common missing fields
QUESTION_TEMPLATES = {
    "date": "When did this incident occur? Please provide an approximate date or time period.",
    "location": "In which city and state did this happen?",
    "amount": "What is the approximate monetary value or amount involved?",
    "party": "Who is the other party involved? (company name, person's relation to you, etc.)",
    "document": "Do you have any documents related to this issue? (receipts, contracts, agreements)",
    "action_taken": "Have you already taken any steps to resolve this? (complained to company, filed police report, etc.)",
    "employment": "Is this related to your employment? If yes, are you still working there?",
    "relationship": "What is your relationship with the other party? (employer, seller, landlord, family member)",
    "purchase": "How did you make this purchase? (online, retail store, from individual)",
    "duration": "How long has this issue been ongoing?"
}


class ClarificationAgent:
    """
    Clarification Agent: Asks targeted follow-up questions.
    
    Responsibilities:
    - Ask only for missing legal facts
    - One question at a time
    - Never ask open-ended nonsense
    """
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.templates = QUESTION_TEMPLATES
    
    async def generate_question(
        self,
        missing_fields: List[str],
        classification: Dict[str, Any],
        user_input: str,
        asked_questions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a clarifying question.
        
        Args:
            missing_fields: List of missing information fields
            classification: Current classification result
            user_input: Original user input
            asked_questions: Previously asked questions
            
        Returns:
            Question and metadata
        """
        asked_questions = asked_questions or []
        
        # First, try to use templates for common fields
        for field in missing_fields:
            field_lower = field.lower()
            for template_key, template_question in self.templates.items():
                if template_key in field_lower and template_question not in asked_questions:
                    return {
                        "question": template_question,
                        "field": field,
                        "source": "template",
                        "timestamp": datetime.utcnow().isoformat()
                    }
        
        # If no template matches, use LLM to generate question
        try:
            question = await self._generate_llm_question(
                missing_fields,
                classification,
                user_input,
                asked_questions
            )
            
            return {
                "question": question,
                "field": missing_fields[0] if missing_fields else "general",
                "source": "llm",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Clarification generation error: {str(e)}")
            return {
                "question": "Could you please provide more specific details about your situation?",
                "field": "general",
                "source": "fallback",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_llm_question(
        self,
        missing_fields: List[str],
        classification: Dict[str, Any],
        user_input: str,
        asked_questions: List[str]
    ) -> str:
        """Generate question using LLM."""
        user_prompt = f"""
Missing information needed: {', '.join(missing_fields)}

Current classification:
- Domain: {classification.get('domain', 'Unknown')}
- Sub-domain: {classification.get('sub_domain', 'Unknown')}
- Confidence: {classification.get('confidence', 0)}

User's original message:
{user_input}

Questions already asked:
{chr(10).join(asked_questions) if asked_questions else 'None'}

Generate ONE specific question to gather the most important missing information:
"""
        
        messages = [
            SystemMessage(content=CLARIFICATION_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        # Clean response
        question = response.content.strip()
        
        # Remove any leading numbers or bullets
        if question and question[0] in '0123456789.-•':
            question = question.lstrip('0123456789.-•').strip()
        
        return question
    
    def get_priority_fields(self, classification: Dict[str, Any]) -> List[str]:
        """Get priority fields based on classification domain."""
        domain = classification.get("domain", "Unknown")
        
        # Domain-specific priority fields
        priority_map = {
            "Consumer Law": ["purchase_date", "seller_name", "amount", "product_description"],
            "Labour Law": ["employment_period", "employer_name", "salary", "termination_date"],
            "Criminal Law": ["incident_date", "location", "police_report", "injuries"],
            "Family Law": ["relationship", "marriage_date", "children", "residence"],
            "Property Law": ["property_location", "ownership_docs", "dispute_type", "other_party"],
        }
        
        return priority_map.get(domain, ["date", "location", "amount", "party"])