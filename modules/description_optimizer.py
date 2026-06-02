"""
Description Optimizer Module

Automatically optimizes video descriptions for SEO and engagement.
Adds keywords, timestamps, CTAs, and links.

Usage:
    from modules.description_optimizer import optimize_description
    
    optimized = optimize_description(
        base_description="Learn about making money",
        topic="money",
        video_duration=45
    )
"""

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class DescriptionConfig:
    """Configuration for description optimization."""
    
    def __init__(self):
        """Initialize description configuration."""
        self.enable_optimization = os.getenv("ENABLE_DESCRIPTION_OPTIMIZATION", "true").lower() == "true"
        self.add_timestamps = os.getenv("ADD_TIMESTAMPS", "true").lower() == "true"
        self.add_keywords = os.getenv("ADD_KEYWORDS", "true").lower() == "true"
        self.add_cta = os.getenv("ADD_CTA", "true").lower() == "true"
        self.max_length = int(os.getenv("DESCRIPTION_MAX_LENGTH", "5000"))


# SEO keywords by topic
TOPIC_KEYWORDS = {
    "money": [
        "make money", "passive income", "earn money", "side hustle",
        "freelancing", "online business", "wealth", "financial freedom"
    ],
    "motivation": [
        "motivation", "inspirational", "success", "goals", "mindset",
        "personal development", "self-help", "growth"
    ],
    "psychology": [
        "psychology", "human behavior", "mind", "mental health",
        "cognitive", "emotions", "habits", "habits"
    ],
    "technology": [
        "technology", "software", "coding", "programming", "tutorial",
        "how-to", "tech tips", "AI"
    ],
}

# Call-to-action templates
CTA_TEMPLATES = [
    "Subscribe for more videos like this!",
    "Like and subscribe for more content!",
    "Don't forget to hit the subscribe button!",
    "Subscribe to stay updated on new content!",
]


def generate_timestamps(video_duration: int = 45) -> List[str]:
    """
    Generate chapter timestamps for video description.
    
    Args:
        video_duration: Duration of video in seconds
        
    Returns:
        List of timestamp strings
    """
    if video_duration < 60:
        return ["0:00 - Introduction"]
    
    timestamps = [
        "0:00 - Introduction",
        f"{video_duration // 3}:{video_duration % 3 * 60:02d} - Main Content",
        f"{video_duration * 2 // 3}:{(video_duration * 2 // 3) % 60:02d} - Key Takeaways",
        f"{video_duration - 5}:00 - Outro",
    ]
    return timestamps


def get_keywords_for_topic(topic: str) -> List[str]:
    """Get SEO keywords for a topic."""
    return TOPIC_KEYWORDS.get(topic, TOPIC_KEYWORDS["technology"])


def optimize_description(
    base_description: str,
    topic: str = "general",
    video_duration: int = 45,
    config: Optional[DescriptionConfig] = None
) -> str:
    """
    Optimize a video description for SEO and engagement.
    
    Args:
        base_description: Original description
        topic: Video topic
        video_duration: Duration of video in seconds
        config: Optional DescriptionConfig
        
    Returns:
        Optimized description
    """
    if config is None:
        config = DescriptionConfig()
    
    if not config.enable_optimization:
        logger.debug("Description optimization disabled")
        return base_description
    
    logger.info(f"Optimizing description for topic: {topic}")
    
    optimized = base_description + "\n\n"
    
    # Add timestamps
    if config.add_timestamps and video_duration > 0:
        optimized += "⏱️ TIMESTAMPS:\n"
        for ts in generate_timestamps(video_duration):
            optimized += f"{ts}\n"
        optimized += "\n"
    
    # Add keywords
    if config.add_keywords:
        keywords = get_keywords_for_topic(topic)
        optimized += "🔍 KEYWORDS:\n"
        optimized += ", ".join(keywords) + "\n\n"
    
    # Add CTA
    if config.add_cta:
        cta = CTA_TEMPLATES[hash(topic) % len(CTA_TEMPLATES)]
        optimized += f"👍 {cta}\n\n"
    
    # Add disclaimer/footer
    optimized += "---\n"
    optimized += "This video is for educational purposes only.\n"
    optimized += "Always verify information before taking action.\n"
    
    # Truncate if too long
    if len(optimized) > config.max_length:
        optimized = optimized[:config.max_length - 100] + "\n\n[Description truncated for length]"
        logger.debug(f"Truncated to {config.max_length} characters")
    
    logger.info(f"Description optimized: {len(optimized)} characters")
    return optimized


def add_affiliate_links(
    description: str,
    affiliate_links: dict
) -> str:
    """
    Add affiliate links to description.
    
    Args:
        description: Base description
        affiliate_links: Dictionary of product -> link mappings
        
    Returns:
        Description with affiliate links
    """
    if not affiliate_links:
        return description
    
    description += "\n\n📦 RESOURCES & AFFILIATE LINKS:\n"
    for product, link in affiliate_links.items():
        description += f"• {product.title()}: {link}\n"
    
    return description


def add_related_videos(
    description: str,
    related_videos: List[str]
) -> str:
    """
    Add related videos to description.
    
    Args:
        description: Base description
        related_videos: List of video titles/IDs
        
    Returns:
        Description with related videos section
    """
    if not related_videos:
        return description
    
    description += "\n\n📹 RELATED VIDEOS:\n"
    for video in related_videos[:5]:  # Max 5 related videos
        description += f"• {video}\n"
    
    return description


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    base_desc = "In this video, we explore various methods to generate passive income online."
    topic = "money"
    duration = 45
    
    optimized = optimize_description(base_desc, topic, duration)
    print("Original Description:")
    print(base_desc)
    print("\n" + "=" * 60 + "\n")
    print("Optimized Description:")
    print(optimized)
