import random
from typing import List, Optional, Sequence, Any


def random_upload_offset(max_minutes: int = 5) -> int:
    """Return a random minute offset between -max_minutes and +max_minutes."""
    return random.randint(-max_minutes, max_minutes)


def format_time_with_offset(time_str: str, offset_minutes: int) -> str:
    """Add an offset to an HH:MM string and return a new HH:MM string."""
    hour, minute = [int(part) for part in time_str.split(":")]
    total_minutes = hour * 60 + minute + offset_minutes
    total_minutes %= 24 * 60
    new_hour = total_minutes // 60
    new_minute = total_minutes % 60
    return f"{new_hour:02d}:{new_minute:02d}"


def randomize_tag_order(tags: List[str]) -> List[str]:
    """Return a shuffled copy of tags to avoid repeated order patterns."""
    shuffled = list(tags)
    random.shuffle(shuffled)
    return shuffled


def randomize_description_blocks(description: str) -> str:
    """Randomize paragraph blocks inside a description."""
    blocks = [block.strip() for block in description.split("\n\n") if block.strip()]
    if len(blocks) <= 1:
        return description
    random.shuffle(blocks)
    return "\n\n".join(blocks)


def random_thumbnail_variations(config: Optional[Any] = None) -> Any:
    """Apply small random visual variations to thumbnail settings."""
    if config is None:
        from modules.thumbnail_generator import ThumbnailConfig
        config = ThumbnailConfig()

    choices = [0, 5, 8, 10]
    config.border_width = random.choice(choices)
    text_color_options = [(255, 255, 255), (240, 240, 240), (230, 230, 255)]
    config.text_color = random.choice(text_color_options)
    return config
