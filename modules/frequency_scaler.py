"""
Safe Posting Frequency Scaler Module

Automatically adjusts posting frequency based on performance metrics.
Prevents channel burnout and optimizes for sustainable growth.

Usage:
    from modules.frequency_scaler import calculate_optimal_frequency
    
    freq = calculate_optimal_frequency(
        channel_stats={"avg_views": 5000, "engagement_rate": 0.08},
        current_frequency=3  # 3 videos per day
    )
"""

import logging
import os
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FrequencyScalerConfig:
    """Configuration for frequency scaling."""
    
    def __init__(self):
        """Initialize frequency scaler configuration."""
        self.enable_scaling = os.getenv("ENABLE_FREQUENCY_SCALING", "false").lower() == "true"
        self.min_frequency = int(os.getenv("MIN_UPLOAD_FREQUENCY", "1"))  # Min 1 per day
        self.max_frequency = int(os.getenv("MAX_UPLOAD_FREQUENCY", "5"))  # Max 5 per day
        self.engagement_threshold = float(os.getenv("ENGAGEMENT_THRESHOLD", "0.05"))  # 5%
        self.min_views_per_video = int(os.getenv("MIN_VIEWS_PER_VIDEO", "100"))


def calculate_engagement_rate(video_stats: Dict) -> float:
    """
    Calculate engagement rate from video statistics.
    Engagement = (likes + comments + shares) / views
    
    Args:
        video_stats: Dict with views, likes, comments, shares
        
    Returns:
        Engagement rate as decimal (0.0-1.0)
    """
    views = max(1, video_stats.get("views", 1))
    engagements = (
        video_stats.get("likes", 0) +
        video_stats.get("comments", 0) +
        video_stats.get("shares", 0)
    )
    
    return engagements / views


def calculate_average_performance(
    video_history: list
) -> Dict:
    """
    Calculate average performance from video history.
    
    Args:
        video_history: List of video stat dicts
        
    Returns:
        Dict with average metrics
    """
    if not video_history:
        return {
            "avg_views": 0,
            "avg_engagement": 0,
            "avg_watch_time": 0,
            "video_count": 0
        }
    
    total_views = sum(v.get("views", 0) for v in video_history)
    total_engagement = sum(calculate_engagement_rate(v) for v in video_history)
    total_watch_time = sum(v.get("watch_time_minutes", 0) for v in video_history)
    
    count = len(video_history)
    
    return {
        "avg_views": total_views / count,
        "avg_engagement": total_engagement / count,
        "avg_watch_time": total_watch_time / count,
        "video_count": count
    }


def calculate_optimal_frequency(
    channel_stats: Dict,
    current_frequency: int = 3,
    config: Optional[FrequencyScalerConfig] = None
) -> int:
    """
    Calculate optimal upload frequency based on channel performance.
    
    Args:
        channel_stats: Dict with performance metrics
        current_frequency: Current uploads per day
        config: Optional FrequencyScalerConfig
        
    Returns:
        Recommended frequency (uploads per day)
    """
    if config is None:
        config = FrequencyScalerConfig()
    
    if not config.enable_scaling:
        logger.debug("Frequency scaling disabled")
        return current_frequency
    
    logger.info(f"Calculating optimal frequency for current: {current_frequency}/day")
    
    avg_views = channel_stats.get("avg_views", 0)
    avg_engagement = channel_stats.get("avg_engagement", 0)
    avg_watch_time = channel_stats.get("avg_watch_time", 0)
    
    # Start with current frequency
    optimal = current_frequency
    
    # If average engagement is high, can increase frequency
    if avg_engagement > config.engagement_threshold * 2:
        optimal = min(config.max_frequency, current_frequency + 1)
        logger.info(f"High engagement detected, increasing to {optimal}/day")
    
    # If average views are low, should decrease frequency
    elif avg_views < config.min_views_per_video:
        optimal = max(config.min_frequency, current_frequency - 1)
        logger.info(f"Low views detected, decreasing to {optimal}/day")
    
    # If watch time is good, maintain or slightly increase
    elif avg_watch_time > 15:
        if avg_engagement > config.engagement_threshold:
            optimal = current_frequency  # Keep steady
        else:
            optimal = max(config.min_frequency, current_frequency - 1)
    
    # Enforce limits
    optimal = max(config.min_frequency, min(config.max_frequency, optimal))
    
    logger.info(f"Optimal frequency: {optimal}/day")
    return optimal


def get_burnout_risk_score(
    upload_frequency: int,
    days_active: int,
    platform: str = "youtube"
) -> float:
    """
    Calculate burnout risk score (0-1).
    
    Args:
        upload_frequency: Uploads per day
        days_active: Days channel has been active
        platform: Platform name
        
    Returns:
        Risk score 0.0 (safe) to 1.0 (high risk)
    """
    risk = 0.0
    
    # Frequency risk
    if upload_frequency >= 5:
        risk += 0.4
    elif upload_frequency >= 3:
        risk += 0.2
    
    # Sustainability risk (no time to build audience)
    if days_active < 30:
        risk += 0.3
    elif days_active < 90:
        risk += 0.1
    
    # Consistency penalty
    if upload_frequency > 3:
        risk += 0.1
    
    return min(1.0, risk)


def get_frequency_recommendation(
    current_frequency: int,
    burnout_risk: float
) -> Dict:
    """
    Get frequency recommendation with reasoning.
    
    Args:
        current_frequency: Current frequency
        burnout_risk: Burnout risk score
        
    Returns:
        Dict with recommendation and reasoning
    """
    recommendation = {
        "current": current_frequency,
        "recommended": current_frequency,
        "reasoning": [],
        "risk_level": "safe"
    }
    
    if burnout_risk >= 0.7:
        recommendation["risk_level"] = "high"
        recommendation["recommended"] = max(1, current_frequency - 2)
        recommendation["reasoning"].append("High burnout risk detected")
        recommendation["reasoning"].append("Recommend reducing frequency")
    elif burnout_risk >= 0.5:
        recommendation["risk_level"] = "moderate"
        recommendation["recommended"] = max(1, current_frequency - 1)
        recommendation["reasoning"].append("Moderate burnout risk")
        recommendation["reasoning"].append("Consider reducing by 1 video/day")
    elif burnout_risk >= 0.3:
        recommendation["risk_level"] = "low"
        recommendation["reasoning"].append("Low burnout risk")
        recommendation["reasoning"].append("Current frequency is sustainable")
    else:
        recommendation["risk_level"] = "very_low"
        recommendation["reasoning"].append("Very low burnout risk")
        recommendation["reasoning"].append("Can potentially increase frequency")
    
    return recommendation


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    # Example channel stats
    stats = {
        "avg_views": 5000,
        "avg_engagement": 0.08,  # 8%
        "avg_watch_time": 20,
    }
    
    current_freq = 3
    optimal = calculate_optimal_frequency(stats, current_freq)
    print(f"Current frequency: {current_freq}/day")
    print(f"Optimal frequency: {optimal}/day")
    
    # Calculate burnout risk
    risk = get_burnout_risk_score(current_freq, days_active=60)
    print(f"\nBurnout risk score: {risk:.2f}")
    
    recommendation = get_frequency_recommendation(current_freq, risk)
    print(f"Recommendation: {recommendation['recommended']}/day")
    print(f"Risk level: {recommendation['risk_level']}")
    for reason in recommendation['reasoning']:
        print(f"  - {reason}")
