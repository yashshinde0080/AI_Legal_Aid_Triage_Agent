"""
Classifier Agent
Handles legal issue classification.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.utils.logger import logger


# Legal domains and their sub-domains
LEGAL_DOMAINS = {
    "Consumer Law": [
        "Defective Product",
        "Service Deficiency",
        "Unfair Trade Practice",
        "E-commerce Dispute",
        "Banking/Financial Service"
    ],
    "Labour Law": [
        "Wage Dispute",
        "Wrongful Termination",
        "Workplace Harassment",
        "Unpaid Benefits",
        "Working Conditions"
    ],
    "Criminal Law": [
        "Theft/Robbery",
        "Assault/Violence",
        "Fraud/Cheating",
        "Cyber Crime",
        "Domestic Violence"
    ],
    "Family Law": [
        "Divorce",
        "Child Custody",
        "Maintenance/Alimony",
        "Domestic Violence",
        "Inheritance"
    ],
    "Property Law": [
        "Property Dispute",
        "Landlord-Tenant",
        "Real Estate Fraud",
        "Encroachment",
        "Title Issues"
    ],
    "Civil Law": [
        "Contract Dispute",
        "Recovery of Money",
        "Defamation",
        "Negligence",
        "Injunction"
    ],
    "Constitutional Law": [
        "Fundamental Rights",
        "RTI Query",
        "Government Action",
        "Discrimination"
    ]
}


CLASSIFICATION_SYSTEM_PROMPT = """You are a legal issue classifier for the Indian legal system.

Your task is to:
1. Analyze the user's description
2. Classify into the most appropriate legal domain
3. Identify the specific sub-domain
4. Assess confidence (0.0 to 1.0)
5. List any missing information needed for accurate classification

Available domains and sub-domains:
{domains}

Rules:
- Set confidence below 0.7 if the issue is unclear
- List specific missing fields like "date of incident", "location", "amount"
- Consider Indian law context
- If truly unclassifiable, use domain "Unknown"

Respond ONLY in this JSON format:
{{
    "domain": "string",
    "sub_domain": "string",
    "confidence": float,
    "missing_fields": ["field1", "field2"],
    "reasoning": "brief explanation"
}}
"""


class ClassifierAgent:
    """
    Classifier Agent: Classifies legal issues into domains.
    
    Responsibilities:
    - Classify issue into domain + sub-domain
    - Output confidence score
    - Identify missing fields for clarification
    """
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.domains = LEGAL_DOMAINS
    
    async def classify(
        self,
        user_input: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify a legal issue.
        
        Args:
            user_input: User's description
            context: Previous conversation context
            
        Returns:
            Classification result
        """
        try:
            # Format domains for prompt
            domains_text = self._format_domains()
            
            # Build prompt
            system_prompt = CLASSIFICATION_SYSTEM_PROMPT.format(domains=domains_text)
            
            user_prompt = f"""
User's description:
{user_input}

Previous context:
{context if context else 'No previous context'}

Classify this legal issue:
"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get classification
            response = await self.llm.ainvoke(messages)
            
            # Parse result
            result = self._parse_response(response.content)
            
            # Validate domain
            result = self._validate_classification(result)
            
            logger.info(
                f"Classification: domain={result['domain']}, "
                f"confidence={result['confidence']}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return self._default_classification()
    
    def _format_domains(self) -> str:
        """Format domains for prompt."""
        lines = []
        for domain, sub_domains in self.domains.items():
            lines.append(f"\n{domain}:")
            for sub in sub_domains:
                lines.append(f"  - {sub}")
        return "\n".join(lines)
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        try:
            # Clean response
            content = content.strip()
            
            # Extract JSON if wrapped in code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            result = json.loads(content.strip())
            
            return {
                "domain": result.get("domain", "Unknown"),
                "sub_domain": result.get("sub_domain", "Unknown"),
                "confidence": float(result.get("confidence", 0.0)),
                "missing_fields": result.get("missing_fields", []),
                "reasoning": result.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse classification response: {e}")
            return self._default_classification()
    
    def _validate_classification(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and correct classification."""
        domain = result.get("domain", "Unknown")
        sub_domain = result.get("sub_domain", "Unknown")
        
        # Check if domain exists
        if domain not in self.domains and domain != "Unknown":
            # Try to find closest match
            for valid_domain in self.domains.keys():
                if domain.lower() in valid_domain.lower():
                    domain = valid_domain
                    break
            else:
                domain = "Unknown"
        
        # Check if sub_domain is valid for domain
        if domain in self.domains:
            valid_subs = self.domains[domain]
            if sub_domain not in valid_subs:
                # Try to find closest match
                for valid_sub in valid_subs:
                    if sub_domain.lower() in valid_sub.lower():
                        sub_domain = valid_sub
                        break
                else:
                    sub_domain = valid_subs[0] if valid_subs else "General"
        
        result["domain"] = domain
        result["sub_domain"] = sub_domain
        
        # Ensure confidence is valid
        result["confidence"] = max(0.0, min(1.0, result.get("confidence", 0.0)))
        
        return result
    
    def _default_classification(self) -> Dict[str, Any]:
        """Return default classification on error."""
        return {
            "domain": "Unknown",
            "sub_domain": "Unknown",
            "confidence": 0.0,
            "missing_fields": ["unable to classify - please provide more details"],
            "reasoning": "Classification failed"
        }