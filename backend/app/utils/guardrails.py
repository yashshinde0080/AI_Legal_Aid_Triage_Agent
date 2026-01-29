"""
Guardrails
Safety checks and content validation.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re


@dataclass
class GuardrailViolation:
    """Represents a guardrail violation."""
    rule: str
    description: str
    severity: str  # low, medium, high
    match: Optional[str] = None


# Guardrail rules
GUARDRAIL_RULES = {
    "legal_advice": {
        "patterns": [
            r"you should (definitely|certainly|absolutely) (sue|file|take)",
            r"you must (sue|file|take legal action)",
            r"i (strongly )?(advise|recommend) you to",
            r"my (professional )?advice is",
        ],
        "description": "Detected legal advice language",
        "severity": "high"
    },
    "outcome_prediction": {
        "patterns": [
            r"you will (definitely|certainly|likely) (win|lose|succeed|fail)",
            r"(guaranteed|certain) (outcome|result|success)",
            r"your chances (of winning|are) (good|bad|high|low)",
            r"the (court|judge) will (definitely|certainly|likely)",
        ],
        "description": "Detected outcome prediction",
        "severity": "high"
    },
    "specific_lawyer": {
        "patterns": [
            r"contact (this|my|our) lawyer",
            r"(call|contact|email) (advocate|lawyer|attorney) [A-Z][a-z]+",
            r"(?:phone|call|mobile):\s*\+?\d{10,}",
        ],
        "description": "Detected specific lawyer recommendation",
        "severity": "medium"
    },
    "medical_advice": {
        "patterns": [
            r"you (should|must) (take|stop taking) (medicine|medication)",
            r"(my|this) (medical|health) (advice|recommendation)",
        ],
        "description": "Detected medical advice",
        "severity": "high"
    },
    "financial_advice": {
        "patterns": [
            r"you (should|must) (invest|buy|sell)",
            r"(my|this) (financial|investment) (advice|recommendation)",
        ],
        "description": "Detected financial advice",
        "severity": "high"
    },
    "personal_info_request": {
        "patterns": [
            r"(send|give|share) (me|us) your (aadhaar|aadhar|pan|passport)",
            r"(your|the) (password|pin|otp)",
        ],
        "description": "Detected personal information request",
        "severity": "high"
    },
    "coercive_language": {
        "patterns": [
            r"you (have no choice|must act now|will regret)",
            r"(urgent|immediately|right now) or (you will|else)",
            r"don't (trust|listen to) anyone else",
        ],
        "description": "Detected coercive language",
        "severity": "medium"
    }
}


def check_guardrails(text: str) -> Dict[str, Any]:
    """
    Check text against all guardrail rules.
    
    Args:
        text: Text to check
        
    Returns:
        Result with violations and overall status
    """
    violations: List[GuardrailViolation] = []
    
    text_lower = text.lower()
    
    for rule_name, rule_config in GUARDRAIL_RULES.items():
        patterns = rule_config["patterns"]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                violation = GuardrailViolation(
                    rule=rule_name,
                    description=rule_config["description"],
                    severity=rule_config["severity"],
                    match=str(matches[0]) if matches else None
                )
                violations.append(violation)
                break  # One violation per rule is enough
    
    # Determine overall status
    high_severity = any(v.severity == "high" for v in violations)
    medium_severity = any(v.severity == "medium" for v in violations)
    
    return {
        "valid": len(violations) == 0,
        "violations": [
            {
                "rule": v.rule,
                "description": v.description,
                "severity": v.severity,
                "match": v.match
            }
            for v in violations
        ],
        "severity": "high" if high_severity else ("medium" if medium_severity else "low"),
        "violation_count": len(violations)
    }


def sanitize_text(text: str, violations: List[Dict[str, Any]]) -> str:
    """
    Attempt to sanitize text based on violations.
    
    Args:
        text: Original text
        violations: List of violations found
        
    Returns:
        Sanitized text
    """
    sanitized = text
    
    # Replacement patterns
    replacements = {
        "you should definitely": "you may consider",
        "you must sue": "you have the option to file a case",
        "you will definitely win": "the outcome depends on the case merits",
        "you will lose": "outcomes depend on various factors",
        "guaranteed": "possible",
        "i advise you to": "one option is to",
        "i recommend you to": "you might consider",
        "you have no choice": "you have several options",
    }
    
    for old, new in replacements.items():
        sanitized = re.sub(old, new, sanitized, flags=re.IGNORECASE)
    
    return sanitized


def is_out_of_scope(text: str) -> bool:
    """
    Check if the query is out of scope for legal aid.
    
    Args:
        text: User query
        
    Returns:
        True if out of scope
    """
    out_of_scope_patterns = [
        r"(recipe|cooking|food|restaurant)",
        r"(movie|film|entertainment|music)",
        r"(sports|game|play|cricket|football)",
        r"(weather|temperature|forecast)",
        r"(joke|funny|humor)",
        r"(dating|relationship advice)",
    ]
    
    text_lower = text.lower()
    
    for pattern in out_of_scope_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False