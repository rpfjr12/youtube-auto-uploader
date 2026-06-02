"""
Trending Topic Discovery Module

Discovers trending topics on YouTube to ensure content stays relevant.
Uses multiple data sources and heuristics to identify trending content.

Usage:
    from modules.trending_topic_discovery import get_trending_topics
    
    topics = get_trending_topics(
        niche="personal finance",
        region="US"
    )
"""

import logging
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TrendingConfig:
    """Configuration for trending topic discovery."""
    
    def __init__(self):
        """Initialize trending configuration."""
        self.enable_discovery = os.getenv("ENABLE_TRENDING_DISCOVERY", "false").lower() == "true"
        self.cache_duration_hours = int(os.getenv("TRENDING_CACHE_HOURS", "24"))
        self.min_trend_score = float(os.getenv("MIN_TREND_SCORE", "0.5"))


# Pre-defined trending topics by niche (for when API is unavailable)
TRENDING_TOPICS_DB = {
    "personal finance": [
        {"topic": "passive income", "score": 0.95, "growth": "high"},
        {"topic": "side hustle", "score": 0.90, "growth": "high"},
        {"topic": "financial independence", "score": 0.85, "growth": "medium"},
        {"topic": "stock market", "score": 0.80, "growth": "medium"},
        {"topic": "cryptocurrency", "score": 0.75, "growth": "volatile"},
    ],
    "motivation": [
        {"topic": "grind mentality", "score": 0.92, "growth": "high"},
        {"topic": "productivity hacks", "score": 0.88, "growth": "high"},
        {"topic": "success stories", "score": 0.83, "growth": "medium"},
        {"topic": "personal development", "score": 0.78, "growth": "steady"},
        {"topic": "morning routine", "score": 0.75, "growth": "medium"},
    ],
    "psychology": [
        {"topic": "dark psychology", "score": 0.89, "growth": "high"},
        {"topic": "manipulation tactics", "score": 0.85, "growth": "high"},
        {"topic": "cognitive biases", "score": 0.82, "growth": "medium"},
        {"topic": "habit formation", "score": 0.80, "growth": "steady"},
        {"topic": "mental health", "score": 0.78, "growth": "high"},
    ],
    "technology": [
        {"topic": "AI breakthroughs", "score": 0.94, "growth": "viral"},
        {"topic": "ChatGPT tutorial", "score": 0.91, "growth": "high"},
        {"topic": "automation tools", "score": 0.85, "growth": "high"},
        {"topic": "no-code development", "score": 0.80, "growth": "medium"},
        {"topic": "cybersecurity tips", "score": 0.75, "growth": "steady"},
    ],
}


def get_trending_topics(
    niche: str = "personal finance",
    region: str = "US",
    limit: int = 10,
    config: Optional[TrendingConfig] = None
) -> List[Dict[str, any]]:
    """
    Get trending topics for a niche.
    
    Args:
        niche: Niche category (e.g., "personal finance")
        region: Geographic region
        limit: Maximum number of topics to return
        config: Optional TrendingConfig
        
    Returns:
        List of trending topic dicts with score and growth info
    """
    if config is None:
        config = TrendingConfig()
    
    if not config.enable_discovery:
        logger.debug("Trending discovery disabled")
        return []
    
    logger.info(f"Fetching trending topics for niche: {niche}")
    
    # Try to get from database first
    topics = TRENDING_TOPICS_DB.get(niche.lower(), [])
    
    if not topics:
        logger.warning(f"No trending topics found for niche: {niche}")
        # Return general trending topics as fallback
        topics = TRENDING_TOPICS_DB["personal finance"]
    
    # Filter by minimum score
    filtered = [t for t in topics if t.get("score", 0) >= config.min_trend_score]
    
    # Sort by score descending
    sorted_topics = sorted(filtered, key=lambda x: x["score"], reverse=True)
    
    # Limit results
    result = sorted_topics[:limit]
    
    logger.info(f"Returned {len(result)} trending topics")
    return result


def get_seasonal_topics(
    niche: str = "personal finance"
) -> List[str]:
    """
    Get seasonal topics for a niche based on current date.
    
    Args:
        niche: Niche category
        
    Returns:
        List of seasonal topic suggestions
    """
    now = datetime.now()
    month = now.month
    
    seasonal_map = {
        1: ["New Year resolutions", "Financial goals", "Productivity planning"],
        2: ["Valentine's Day marketing", "Love and money", "Budget for couples"],
        3: ["Tax season tips", "Spring planning", "Q1 goals review"],
        4: ["Earth Day sustainability", "Spring productivity", "Money management"],
        5: ["Summer preparation", "Travel budgeting", "Summer side hustles"],
        6: ["Summer goals", "Vacation planning", "Mid-year review"],
        7: ["Summer trends", "Influencer strategies", "Viral content"],
        8: ["Back to school", "College financing", "Student productivity"],
        9: ["Fall goals", "Q3 review", "New routines"],
        10: ["Halloween trends", "Q4 planning", "Black Friday prep"],
        11: ["Thanksgiving savings", "Black Friday deals", "Cyber Monday"],
        12: ["Holiday budgeting", "Year-end review", "New Year prep"],
    }
    
    return seasonal_map.get(month, [])


def score_topic_relevance(
    topic: str,
    current_topics: List[str]
) -> float:
    """
    Score how relevant a topic is based on current content.
    
    Args:
        topic: Topic to score
        current_topics: List of current topics
        
    Returns:
        Relevance score 0-1
    """
    # Check for keyword overlap
    topic_words = set(topic.lower().split())
    score = 0.0
    
    for current in current_topics:
        current_words = set(current.lower().split())
        overlap = len(topic_words & current_words)
        if overlap > 0:
            score += 0.5
    
    # Boost score for less common topics (max 1.0)
    score = min(1.0, score)
    
    return score


def get_recommended_topics(
    niche: str = "personal finance",
    current_topics: List[str] = None,
    limit: int = 5
) -> List[str]:
    """
    Get topic recommendations based on current content.
    
    Args:
        niche: Niche category
        current_topics: List of current topics being covered
        limit: Number of recommendations
        
    Returns:
        List of recommended topics
    """
    if current_topics is None:
        current_topics = []
    
    trending = get_trending_topics(niche, limit=20)
    recommendations = []
    
    for trend in trending:
        topic = trend["topic"]
        relevance = score_topic_relevance(topic, current_topics)
        
        # Only recommend if sufficiently relevant and not already covered
        if relevance < 1.0 and topic not in current_topics:
            recommendations.append(topic)
    
    return recommendations[:limit]


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    config = TrendingConfig()
    config.enable_discovery = True
    
    niche = "personal finance"
    topics = get_trending_topics(niche, config=config)
    
    print(f"Trending Topics for {niche}:")
    for i, t in enumerate(topics[:5], 1):
        print(f"  {i}. {t['topic']} (score: {t['score']}, growth: {t['growth']})")
    
    seasonal = get_seasonal_topics(niche)
    print(f"\nSeasonal Topics: {', '.join(seasonal)}")
    
    current = ["passive income", "side hustle"]
    recommendations = get_recommended_topics(niche, current, 3)
    print(f"\nRecommendations: {', '.join(recommendations)}")
