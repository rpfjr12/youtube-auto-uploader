"""
Unit tests for thumbnail_generator module.
"""

import pytest
import logging
from pathlib import Path
from modules.thumbnail_generator import (
    ThumbnailConfig,
    get_color_for_topic,
    get_emoji_for_topic,
    generate_thumbnail,
)


logger = logging.getLogger(__name__)


class TestThumbnailConfig:
    """Tests for ThumbnailConfig class."""
    
    def test_init(self):
        """Test ThumbnailConfig initialization."""
        config = ThumbnailConfig()
        assert config.width > 0
        assert config.height > 0
        assert len(config.bg_colors) > 0


class TestGetColorForTopic:
    """Tests for topic color selection."""
    
    def test_get_money_color(self):
        """Test color for money topic."""
        color = get_color_for_topic("money")
        assert isinstance(color, tuple)
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)
    
    def test_get_motivation_color(self):
        """Test color for motivation topic."""
        color = get_color_for_topic("motivation")
        assert isinstance(color, tuple)
        assert len(color) == 3
    
    def test_get_unknown_topic_color(self):
        """Test color for unknown topic (fallback)."""
        color = get_color_for_topic("unknown_topic")
        assert isinstance(color, tuple)
        assert len(color) == 3


class TestGetEmojiForTopic:
    """Tests for emoji selection."""
    
    def test_emoji_money(self):
        """Test emoji for money topic."""
        emoji = get_emoji_for_topic("money")
        assert emoji == "💰"
    
    def test_emoji_motivation(self):
        """Test emoji for motivation topic."""
        emoji = get_emoji_for_topic("motivation")
        assert emoji == "🚀"
    
    def test_emoji_psychology(self):
        """Test emoji for psychology topic."""
        emoji = get_emoji_for_topic("psychology")
        assert emoji == "🧠"
    
    def test_emoji_unknown(self):
        """Test emoji for unknown topic."""
        emoji = get_emoji_for_topic("unknown")
        assert emoji == "⭐"


class TestGenerateThumbnail:
    """Tests for thumbnail generation."""
    
    @pytest.mark.slow
    def test_generate_thumbnail_basic(self, temp_output_dir):
        """Test basic thumbnail generation."""
        config = ThumbnailConfig()
        config.enable_thumbnails = True
        
        try:
            output = generate_thumbnail(
                "Test Title",
                "money",
                "💰",
                temp_output_dir,
                config
            )
            
            # Should return a path
            assert output != ""
            assert "thumbnail" in output
        except ImportError:
            pytest.skip("Pillow not installed")
    
    def test_generate_thumbnail_disabled(self, temp_output_dir):
        """Test when thumbnail generation is disabled."""
        config = ThumbnailConfig()
        config.enable_thumbnails = False
        
        output = generate_thumbnail(
            "Test Title",
            "money",
            config=config
        )
        
        assert output == ""
    
    @pytest.mark.slow
    def test_generate_long_title_truncation(self, temp_output_dir):
        """Test that long titles are truncated."""
        config = ThumbnailConfig()
        config.enable_thumbnails = True
        
        try:
            long_title = "This is an extremely long title that should definitely be truncated"
            output = generate_thumbnail(
                long_title,
                "money",
                config=config
            )
            
            assert output != ""
        except ImportError:
            pytest.skip("Pillow not installed")
    
    @pytest.mark.slow
    def test_generate_with_emoji(self, temp_output_dir):
        """Test thumbnail generation with emoji."""
        config = ThumbnailConfig()
        config.enable_thumbnails = True
        
        try:
            output = generate_thumbnail(
                "Test",
                "money",
                emoji="💰",
                output_dir=temp_output_dir,
                config=config
            )
            
            assert output != ""
        except ImportError:
            pytest.skip("Pillow not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
