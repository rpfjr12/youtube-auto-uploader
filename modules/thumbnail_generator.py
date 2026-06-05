"""
Automatic Thumbnail Generator Module

Generates eye-catching video thumbnails automatically based on video topic and metadata.
Uses PIL/Pillow for fast image generation.

Usage:
    from modules.thumbnail_generator import generate_thumbnail
    
    thumbnail_path = generate_thumbnail(
        title="How to Make Money",
        topic="money",
        emoji="💰"
    )
"""

import logging
import os
import random
from pathlib import Path
from typing import Optional, Tuple

from modules.randomization_engine import random_thumbnail_variations
from modules.reuse_protection import hash_file, is_duplicate, register_asset

logger = logging.getLogger(__name__)


class ThumbnailConfig:
    """Configuration for thumbnail generation."""
    
    def __init__(self):
        """Initialize thumbnail configuration."""
        self.width = 1280
        self.height = 720
        self.bg_colors = {
            "money": (255, 193, 7),      # Gold
            "motivation": (76, 175, 80),  # Green
            "psychology": (103, 58, 183),  # Purple
            "technology": (33, 150, 243),  # Blue
            "general": (244, 67, 54),      # Red
        }
        self.text_color = (255, 255, 255)  # White
        self.enable_thumbnails = os.getenv("ENABLE_THUMBNAILS", "false").lower() == "true"


def get_color_for_topic(topic: str, config: Optional[ThumbnailConfig] = None) -> Tuple[int, int, int]:
    """Get background color for topic."""
    if config is None:
        config = ThumbnailConfig()
    
    return config.bg_colors.get(topic, config.bg_colors["general"])


def generate_thumbnail(
    title: str,
    topic: str = "general",
    emoji: Optional[str] = None,
    output_dir: str = "uploads",
    config: Optional[ThumbnailConfig] = None
) -> str:
    """
    Generate a thumbnail image for a video.
    
    Args:
        title: Video title (will be used in thumbnail)
        topic: Video topic (determines colors)
        emoji: Optional emoji to include
        output_dir: Directory to save thumbnail
        config: Optional ThumbnailConfig
        
    Returns:
        Path to generated thumbnail file
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logger.error("PIL/Pillow not installed. Install with: pip install Pillow")
        raise ImportError("Pillow is required for thumbnail generation")
    
    if config is None:
        config = ThumbnailConfig()

    config = random_thumbnail_variations(config)
    
    if not config.enable_thumbnails:
        logger.debug("Thumbnails disabled in configuration")
        return ""
    
    logger.info(f"Generating thumbnail for: {title[:50]}")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Create image
    bg_color = get_color_for_topic(topic, config)
    img = Image.new("RGB", (config.width, config.height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold font, fallback to default
    try:
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80
        )
    except:
        title_font = ImageFont.load_default()
    
    # Truncate title if too long
    max_title_length = 20
    display_title = title[:max_title_length]
    if len(title) > max_title_length:
        display_title += "..."
    
    # Add emoji if provided
    if emoji:
        display_title = f"{emoji} {display_title}"
    
    # Draw text centered
    bbox = draw.textbbox((0, 0), display_title, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (config.width - text_width) // 2
    y = (config.height - text_height) // 2
    
    draw.text(
        (x, y),
        display_title,
        fill=config.text_color,
        font=title_font
    )
    
    # Add border for visual appeal
    border_width = 8
    border_color = tuple(max(0, c - 50) for c in bg_color)
    draw.rectangle(
        [(0, 0), (config.width - 1, config.height - 1)],
        outline=border_color,
        width=border_width
    )
    
    # Save thumbnail
    output_path = Path(output_dir) / f"thumbnail_{topic}_{Path(title).stem}.png"
    img.save(str(output_path))
    
    fingerprint = hash_file(str(output_path))
    if is_duplicate("thumbnail", fingerprint):
        backup_output_path = Path(output_dir) / f"thumbnail_{topic}_{Path(title).stem}_{random.randint(100,999)}.png"
        config = random_thumbnail_variations(config)
        img = Image.new("RGB", (config.width, config.height), color=get_color_for_topic(topic, config))
        draw = ImageDraw.Draw(img)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80) if hasattr(ImageFont, 'truetype') else ImageFont.load_default()
        display_title = title[:max_title_length]
        if len(title) > max_title_length:
            display_title += "..."
        if emoji:
            display_title = f"{emoji} {display_title}"
        bbox = draw.textbbox((0, 0), display_title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (config.width - text_width) // 2
        y = (config.height - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), display_title, fill=config.text_color, font=title_font)
        border_color = tuple(max(0, c - 50) for c in get_color_for_topic(topic, config))
        draw.rectangle(
            [(0, 0), (config.width - 1, config.height - 1)],
            outline=border_color,
            width=config.border_width
        )
        img.save(str(backup_output_path))
        output_path = backup_output_path
        fingerprint = hash_file(str(output_path))

    register_asset("thumbnail", fingerprint, {"topic": topic})
    logger.info(f"Thumbnail saved: {output_path}")
    return str(output_path)


def get_emoji_for_topic(topic: str) -> str:
    """Get emoji for topic."""
    emoji_map = {
        "money": "💰",
        "motivation": "🚀",
        "psychology": "🧠",
        "technology": "💻",
        "fitness": "💪",
        "cooking": "🍳",
        "travel": "✈️",
        "business": "📊",
    }
    return emoji_map.get(topic, "⭐")


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    config = ThumbnailConfig()
    config.enable_thumbnails = True
    
    title = "How to Make Money Online"
    topic = "money"
    emoji = get_emoji_for_topic(topic)
    
    try:
        path = generate_thumbnail(title, topic, emoji, config=config)
        print(f"Generated thumbnail: {path}")
    except Exception as e:
        print(f"Error: {e}")
