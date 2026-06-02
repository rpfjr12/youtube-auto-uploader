"""
Title Optimizer Module

Automatically optimizes video titles for SEO and click-through rate.
Adds power words, numbers, and engaging language to increase views.

Usage:
    from modules.title_optimizer import optimize_title
    
    optimized = optimize_title(
        base_title="How to Make Money",
        topic="money"
    )
"""

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class TitleConfig:
    """Configuration for title optimization."""
    
    def __init__(self):
        """Initialize title configuration."""
        self.enable_optimization = os.getenv("ENABLE_TITLE_OPTIMIZATION", "true").lower() == "true"
        self.max_length = int(os.getenv("TITLE_MAX_LENGTH", "60"))
        self.use_power_words = os.getenv("USE_POWER_WORDS", "true").lower() == "true"
        self.use_numbers = os.getenv("USE_NUMBERS", "true").lower() == "true"


# Power words that increase CTR
POWER_WORDS = [
    "Secret", "Proven", "Guaranteed", "Simple", "Easy", "Surprising",
    "Incredible", "Amazing", "Shocking", "Viral", "Ultimate", "Best",
    "Top", "Essential", "Critical", "Must-See", "Never-Before-Seen"
]

# Trending patterns
TRENDING_PATTERNS = [
    "{power_word}: {base_title}",
    "{base_title} - {power_word} Method",
    "{base_title} | {power_word} Results",
    "The {power_word} Guide to {base_title}",
]


def get_power_word_for_topic(topic: str) -> str:
    """Get an appropriate power word for the topic."""
    topic_power_words = {
        "money": ["Proven", "Guaranteed", "Simple"],
        "motivation": ["Incredible", "Amazing", "Ultimate"],
        "psychology": ["Shocking", "Surprising", "Secret"],
        "technology": ["Viral", "Essential", "Must-See"],
        "fitness": ["Incredible", "Simple", "Easy"],
    }
    
    words = topic_power_words.get(topic, POWER_WORDS)
    return words[0]


def add_number_hook(title: str) -> str:
    """Add a number to the beginning of the title if it doesn't have one."""
    if any(char.isdigit() for char in title[:5]):
        return title  # Already has a number
    
    numbers = ["3", "5", "7", "10", "15"]
    return f"{numbers[0]} Ways: {title}"


def optimize_title(
    base_title: str,
    topic: str = "general",
    config: Optional[TitleConfig] = None
) -> str:
    """
    Optimize a video title for SEO and CTR.
    
    Args:
        base_title: Original title
        topic: Video topic
        config: Optional TitleConfig
        
    Returns:
        Optimized title
    """
    if config is None:
        config = TitleConfig()
    
    if not config.enable_optimization:
        logger.debug("Title optimization disabled")
        return base_title
    
    logger.info(f"Optimizing title: {base_title}")
    
    optimized = base_title
    
    # Add number hook
    if config.use_numbers:
        optimized = add_number_hook(optimized)
        logger.debug(f"Added number hook: {optimized}")
    
    # Add power word
    if config.use_power_words:
        power_word = get_power_word_for_topic(topic)
        optimized = f"{power_word}: {optimized}"
        logger.debug(f"Added power word: {optimized}")
    
    # Truncate if too long
    if len(optimized) > config.max_length:
        optimized = optimized[:config.max_length - 3] + "..."
        logger.debug(f"Truncated to {config.max_length} characters")
    
    logger.info(f"Optimized title: {optimized}")
    return optimized


def generate_title_variants(
    base_title: str,
    topic: str = "general",
    count: int = 3
) -> List[str]:
    """
    Generate multiple title variants for A/B testing.
    
    Args:
        base_title: Original title
        topic: Video topic
        count: Number of variants to generate
        
    Returns:
        List of title variants
    """
    logger.info(f"Generating {count} title variants")
    
    variants = [base_title]
    config = TitleConfig()
    
    # Variant 1: With optimization
    if config.enable_optimization:
        variants.append(optimize_title(base_title, topic, config))
    
    # Variant 2: With question format
    if "?" not in base_title:
        variants.append(f"How to {base_title}?")
    
    # Variant 3: Shortened version
    if len(base_title) > 40:
        shortened = base_title[:40].rsplit(" ", 1)[0]
        variants.append(f"{shortened}...")
    
    return variants[:count]


def analyze_title_quality(title: str) -> dict:
    """Analyze title quality and return metrics."""
    return {
        "length": len(title),
        "word_count": len(title.split()),
        "has_number": any(char.isdigit() for char in title),
        "has_power_word": any(word in title for word in POWER_WORDS),
        "has_question": "?" in title,
        "readability_score": min(100, (60 - len(title)) * 1.67),  # 0-100
    }


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    base_title = "How to Make Money Online"
    topic = "money"
    
    optimized = optimize_title(base_title, topic)
    print(f"Original: {base_title}")
    print(f"Optimized: {optimized}")
    
    variants = generate_title_variants(base_title, topic, 3)
    print(f"\nVariants:")
    for i, variant in enumerate(variants, 1):
        print(f"  {i}. {variant}")
    
    quality = analyze_title_quality(optimized)
    print(f"\nQuality Metrics: {quality}")
