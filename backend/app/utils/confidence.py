"""
Confidence Scoring
Utilities for calculating and managing confidence scores.
"""

from typing import Dict, Any, List, Optional


def calculate_confidence(
    classification_confidence: float,
    retrieval_score: float,
    context_relevance: float,
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate overall confidence score.
    
    Args:
        classification_confidence: Confidence from classifier (0-1)
        retrieval_score: Average retrieval similarity (0-1)
        context_relevance: Context relevance score (0-1)
        weights: Optional custom weights
        
    Returns:
        Weighted confidence score (0-1)
    """
    if weights is None:
        weights = {
            "classification": 0.4,
            "retrieval": 0.35,
            "context": 0.25
        }
    
    score = (
        classification_confidence * weights.get("classification", 0.4) +
        retrieval_score * weights.get("retrieval", 0.35) +
        context_relevance * weights.get("context", 0.25)
    )
    
    # Clamp to 0-1
    return max(0.0, min(1.0, score))


def should_clarify(
    confidence: float,
    threshold: float = 0.7,
    clarification_count: int = 0,
    max_clarifications: int = 3
) -> bool:
    """
    Determine if clarification is needed.
    
    Args:
        confidence: Current confidence score
        threshold: Minimum confidence threshold
        clarification_count: Number of clarifications already asked
        max_clarifications: Maximum clarifications allowed
        
    Returns:
        True if clarification is needed
    """
    if clarification_count >= max_clarifications:
        return False
    
    return confidence < threshold


def confidence_to_level(confidence: float) -> str:
    """
    Convert confidence score to a human-readable level.
    
    Args:
        confidence: Confidence score (0-1)
        
    Returns:
        Confidence level string
    """
    if confidence >= 0.9:
        return "very_high"
    elif confidence >= 0.7:
        return "high"
    elif confidence >= 0.5:
        return "medium"
    elif confidence >= 0.3:
        return "low"
    else:
        return "very_low"


def aggregate_document_scores(documents: List[Dict[str, Any]]) -> float:
    """
    Aggregate scores from retrieved documents.
    
    Args:
        documents: List of documents with scores
        
    Returns:
        Aggregated score
    """
    if not documents:
        return 0.0
    
    scores = [doc.get("score", 0.0) for doc in documents]
    
    # Use weighted average favoring top scores
    weights = [1.0 / (i + 1) for i in range(len(scores))]
    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    total_weight = sum(weights)
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0


def missing_fields_penalty(missing_fields: List[str]) -> float:
    """
    Calculate confidence penalty for missing fields.
    
    Args:
        missing_fields: List of missing field names
        
    Returns:
        Penalty to subtract from confidence (0-0.5)
    """
    if not missing_fields:
        return 0.0
    
    # Penalty increases with more missing fields
    penalty = min(0.5, len(missing_fields) * 0.1)
    
    # Critical fields have higher penalty
    critical_fields = ["date", "location", "amount", "party"]
    critical_count = sum(1 for f in missing_fields if any(c in f.lower() for c in critical_fields))
    
    penalty += critical_count * 0.05
    
    return min(0.5, penalty)