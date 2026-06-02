"""
Tag Generator Module

Automatically generates relevant tags for videos based on topic and content.
Optimizes tags for discoverability on YouTube.

Usage:
    from modules.tag_generator import generate_tags
    
    tags = generate_tags(
        title="How to Make Money Online",
        topic="money",
        script_text="..."
    )
"""

import logging
import os
from typing import List, Optional, Set

logger = logging.getLogger(__name__)


class TagConfig:
    """Configuration for tag generation."""
    
    def __init__(self):
        """Initialize tag configuration."""
        self.enable_generation = os.getenv("ENABLE_TAG_GENERATION", "true").lower() == "true"
        self.max_tags = int(os.getenv("MAX_TAGS", "30"))
        self.min_tags = int(os.getenv("MIN_TAGS", "8"))
        self.use_broad_tags = os.getenv("USE_BROAD_TAGS", "true").lower() == "true"
        self.use_niche_tags = os.getenv("USE_NICHE_TAGS", "true").lower() == "true"


# Topic-specific tag sets
TOPIC_TAGS = {
    "money": {
        "broad": ["money", "earn money", "make money online", "passive income"],
        "niche": ["side hustle", "freelance", "gig economy", "dropshipping", "affiliate marketing"],
        "trending": ["financial freedom", "wealth building", "financial independence"]
    },
    "motivation": {
        "broad": ["motivation", "motivation video", "inspirational", "success"],
        "niche": ["personal development", "self-improvement", "mindset", "goals"],
        "trending": ["grind mentality", "level up", "transformation"]
    },
    "psychology": {
        "broad": ["psychology", "psychology explained", "human behavior", "mind"],
        "niche": ["cognitive psychology", "behavioral psychology", "habits"],
        "trending": ["dark psychology", "mindset hacks", "mental health"]
    },
    "technology": {
        "broad": ["technology", "tech tutorial", "how to", "tech tips"],
        "niche": ["programming", "coding", "software", "app development"],
        "trending": ["AI", "machine learning", "automation", "productivity"]
    },
}


def extract_keywords_from_title(title: str) -> Set[str]:
    """Extract keywords from video title."""
    # Split title and filter short words
    keywords = set()
    words = title.lower().split()
    for word in words:
        # Filter out common stop words
        if len(word) > 3 and word not in ["that", "this", "from", "with", "how", "the"]:
            keywords.add(word.strip(".,!?"))
    return keywords


def extract_keywords_from_script(script_text: str, max_keywords: int = 5) -> Set[str]:
    """Extract important keywords from script."""
    words = script_text.lower().split()
    word_freq = {}
    
    # Count word frequency
    stop_words = {"the", "a", "is", "and", "or", "to", "of", "in", "that", "this", "at", "by"}
    for word in words:
        clean_word = word.strip(".,!?;:")
        if len(clean_word) > 4 and clean_word not in stop_words:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Sort by frequency and get top keywords
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return set(k[0] for k in keywords[:max_keywords])


def generate_tags(
    title: str,
    topic: str = "general",
    script_text: str = "",
    config: Optional[TagConfig] = None
) -> List[str]:
    """
    Generate tags for a video.
    
    Args:
        title: Video title
        topic: Video topic
        script_text: Video script (optional, for keyword extraction)
        config: Optional TagConfig
        
    Returns:
        List of tags
    """
    if config is None:
        config = TagConfig()
    
    if not config.enable_generation:
        logger.debug("Tag generation disabled")
        return []
    
    logger.info(f"Generating tags for topic: {topic}")
    
    tags = set()
    
    # Get topic tags
    if topic in TOPIC_TAGS:
        topic_data = TOPIC_TAGS[topic]
        
        if config.use_broad_tags:
            tags.update(topic_data.get("broad", []))
        
        if config.use_niche_tags:
            tags.update(topic_data.get("niche", []))
        
        # Add trending tags (always add)
        tags.update(topic_data.get("trending", []))
    
    # Extract and add keywords from title
    title_keywords = extract_keywords_from_title(title)
    tags.update(title_keywords)
    logger.debug(f"Added {len(title_keywords)} keywords from title")
    
    # Extract and add keywords from script
    if script_text:
        script_keywords = extract_keywords_from_script(script_text)
        tags.update(script_keywords)
        logger.debug(f"Added {len(script_keywords)} keywords from script")
    
    # Add common YouTube tags
    tags.add("youtube")
    tags.add("video")
    
    # Enforce tag limits
    tag_list = list(tags)[:config.max_tags]
    
    if len(tag_list) < config.min_tags:
        logger.warning(f"Generated {len(tag_list)} tags, below minimum {config.min_tags}")
    
    logger.info(f"Generated {len(tag_list)} tags")
    return tag_list


def categorize_tags(tags: List[str]) -> dict:
    """Categorize tags by type."""
    return {
        "short": [t for t in tags if len(t) <= 3],
        "medium": [t for t in tags if 4 <= len(t) <= 10],
        "long": [t for t in tags if len(t) > 10],
    }


def validate_tags(tags: List[str]) -> dict:
    """Validate tags for YouTube requirements."""
    validation = {
        "total_count": len(tags),
        "within_limit": len(tags) <= 30,
        "all_non_empty": all(t.strip() for t in tags),
        "all_strings": all(isinstance(t, str) for t in tags),
        "issues": []
    }
    
    if len(tags) > 30:
        validation["issues"].append(f"Too many tags: {len(tags)} > 30")
    
    if any(not t.strip() for t in tags):
        validation["issues"].append("Some tags are empty or whitespace-only")
    
    return validation


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    title = "5 Secret Ways to Make Money Online"
    topic = "money"
    script = """
    Learn five proven methods to generate passive income online.
    These strategies have helped thousands of people earn extra money.
    From freelancing to dropshipping, discover what works best for you.
    """
    
    tags = generate_tags(title, topic, script)
    print(f"Generated Tags ({len(tags)}):")
    print(", ".join(tags))
    
    categories = categorize_tags(tags)
    print(f"\nTag Categories: {categories}")
    
    validation = validate_tags(tags)
    print(f"\nValidation: {validation}")
