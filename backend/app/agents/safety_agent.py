"""
Safety Agent
Validates responses for safety and compliance.
"""

from typing import Dict, Any, List
from datetime import datetime
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
import json

from app.utils.logger import logger


# Unsafe patterns to detect
UNSAFE_PATTERNS = [
    # Legal advice patterns
    r"you should (definitely|certainly|absolutely)",
    r"you must (sue|file|take legal action)",
    r"i (advise|recommend|suggest) (you|that you) (must|should)",
    r"you (will|are going to) (win|lose|succeed|fail)",
    r"(guaranteed|certain|definitely) (outcome|result|win)",
    
    # Prediction patterns
    r"the (court|judge) will (definitely|certainly|likely)",
    r"you have a (strong|weak|good|bad) case",
    r"your chances (of winning|are)",
    
    # Specific recommendations
    r"contact (this|my|our) lawyer",
    r"hire (this|a specific) advocate",
    r"(?:phone|call|contact):\s*\+?\d{10,}",  # Phone numbers
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # Email addresses
]

# Replacement patterns for sanitization
REPLACEMENTS = {
    "you should definitely": "you may consider",
    "you must sue": "you have the option to file a case",
    "you will win": "the outcome will depend on the merits of your case",
    "you will lose": "outcomes depend on various factors",
    "guaranteed": "possible",
    "i advise you to": "one option is to",
    "i recommend that you": "you might consider",
}


class SafetyAgent:
    """
    Safety Agent: Validates and sanitizes responses.
    
    Responsibilities:
    - Detect legal advice
    - Detect predictions
    - Detect coercive language
    - Enforce refusal when needed
    """
    
    def __init__(self, llm: BaseChatModel = None):
        self.llm = llm
        self.patterns = [re.compile(p, re.IGNORECASE) for p in UNSAFE_PATTERNS]
    
    async def validate(self, response: str) -> Dict[str, Any]:
        """
        Validate response for safety violations.
        
        Args:
            response: Response to validate
            
        Returns:
            Validation result with violations and suggested fixes
        """
        # Run rule-based checks first (fast)
        rule_result = self._rule_based_check(response)
        
        # If rule-based finds issues, handle them
        if not rule_result["valid"]:
            sanitized = self._sanitize_response(response, rule_result["violations"])
            return {
                "valid": False,
                "original_response": response,
                "sanitized_response": sanitized,
                "violations": rule_result["violations"],
                "check_type": "rule_based",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Optionally run LLM-based check for thorough validation
        if self.llm:
            try:
                llm_result = await self._llm_based_check(response)
                if not llm_result["valid"]:
                    sanitized = self._sanitize_response(response, llm_result["violations"])
                    return {
                        "valid": False,
                        "original_response": response,
                        "sanitized_response": sanitized,
                        "violations": llm_result["violations"],
                        "check_type": "llm_based",
                        "timestamp": datetime.utcnow().isoformat()
                    }
            except Exception as e:
                logger.warning(f"LLM safety check failed: {e}")
        
        return {
            "valid": True,
            "original_response": response,
            "sanitized_response": response,
            "violations": [],
            "check_type": "passed",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _rule_based_check(self, response: str) -> Dict[str, Any]:
        """Fast rule-based safety check."""
        violations = []
        
        for pattern in self.patterns:
            matches = pattern.findall(response)
            if matches:
                violations.append({
                    "type": "pattern_match",
                    "pattern": pattern.pattern,
                    "matches": matches[:3]  # Limit to 3 matches
                })
        
        return {
            "valid": len(violations) == 0,
            "violations": violations
        }
    
    async def _llm_based_check(self, response: str) -> Dict[str, Any]:
        """Thorough LLM-based safety check."""
        prompt = f"""Analyze this legal aid response for safety violations.

Check for:
1. Legal advice (telling user what they SHOULD do, not what they CAN do)
2. Outcome predictions (claiming user will win/lose)
3. Specific lawyer/advocate recommendations with contact info
4. Coercive or manipulative language
5. Medical, financial, or personal advice outside legal scope
6. Incorrect or potentially harmful legal information

Response to check:
{response}

Respond in JSON:
{{
    "valid": boolean,
    "violations": ["list of specific violations found"],
    "severity": "low/medium/high"
}}
"""
        
        messages = [
            SystemMessage(content="You are a safety validator for a legal aid system."),
            HumanMessage(content=prompt)
        ]
        
        result = await self.llm.ainvoke(messages)
        
        try:
            content = result.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            parsed = json.loads(content.strip())
            return {
                "valid": parsed.get("valid", True),
                "violations": parsed.get("violations", []),
                "severity": parsed.get("severity", "low")
            }
        except json.JSONDecodeError:
            return {"valid": True, "violations": []}
    
    def _sanitize_response(
        self,
        response: str,
        violations: List[Dict[str, Any]]
    ) -> str:
        """Sanitize response by fixing violations."""
        sanitized = response
        
        # Apply text replacements
        for old, new in REPLACEMENTS.items():
            sanitized = re.sub(
                re.escape(old),
                new,
                sanitized,
                flags=re.IGNORECASE
            )
        
        # Remove phone numbers and emails
        sanitized = re.sub(
            r'(?:phone|call|contact):\s*\+?\d{10,}',
            '[Contact information removed]',
            sanitized,
            flags=re.IGNORECASE
        )
        sanitized = re.sub(
            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            '[Email removed]',
            sanitized
        )
        
        return sanitized
    
    def quick_check(self, response: str) -> bool:
        """Quick boolean check for safety."""
        result = self._rule_based_check(response)
        return result["valid"]