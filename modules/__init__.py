"""
YouTube Auto Uploader Modules

This package contains modular, optional features for the YouTube automation system:
- affiliate_link_generator: Generate affiliate links
- thumbnail_generator: Create video thumbnails
- title_optimizer: Optimize video titles
- description_optimizer: Optimize video descriptions
- tag_generator: Generate relevant tags
- trending_topic_discovery: Discover trending topics
- frequency_scaler: Scale posting frequency based on performance
- multi_channel_support: Enhanced multi-channel features

Each module is independent and can be enabled/disabled via configuration.
"""

__version__ = "1.0.0"
__all__ = [
    "affiliate_link_generator",
    "thumbnail_generator",
    "title_optimizer",
    "description_optimizer",
    "tag_generator",
    "trending_topic_discovery",
    "frequency_scaler",
    "multi_channel_support",
]
