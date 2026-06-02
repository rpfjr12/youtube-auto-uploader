"""
Unit tests for description_optimizer module.
"""

import pytest
import logging
from modules.description_optimizer import (
    DescriptionConfig,
    optimize_description,
    generate_timestamps,
    get_keywords_for_topic,
    add_affiliate_links,
    add_related_videos,
)


logger = logging.getLogger(__name__)


class TestDescriptionConfig:
    """Tests for DescriptionConfig class."""
    
    def test_init(self):
        """Test DescriptionConfig initialization."""
        config = DescriptionConfig()
        assert config.max_length > 0
        assert isinstance(config.enable_optimization, bool)
        assert isinstance(config.add_timestamps, bool)


class TestGenerateTimestamps:
    """Tests for timestamp generation."""
    
    def test_generate_short_video(self):
        """Test timestamps for short video."""
        timestamps = generate_timestamps(45)
        assert len(timestamps) > 0
        assert "Introduction" in timestamps[0]
    
    def test_generate_long_video(self):
        """Test timestamps for longer video."""
        timestamps = generate_timestamps(600)
        assert len(timestamps) >= 4
        assert any("Intro" in ts or "intro" in ts for ts in timestamps)


class TestGetKeywordsForTopic:
    """Tests for keyword retrieval by topic."""
    
    def test_get_keywords_money(self):
        """Test keyword retrieval for money topic."""
        keywords = get_keywords_for_topic("money")
        assert len(keywords) > 0
        assert any("money" in k.lower() or "income" in k.lower() for k in keywords)
    
    def test_get_keywords_motivation(self):
        """Test keyword retrieval for motivation topic."""
        keywords = get_keywords_for_topic("motivation")
        assert len(keywords) > 0
        assert any("motiv" in k.lower() for k in keywords)
    
    def test_get_keywords_default(self):
        """Test keyword retrieval for unknown topic."""
        keywords = get_keywords_for_topic("unknown")
        assert len(keywords) > 0  # Should return default


class TestOptimizeDescription:
    """Tests for description optimization."""
    
    def test_optimize_basic(self):
        """Test basic description optimization."""
        config = DescriptionConfig()
        config.enable_optimization = True
        
        base = "This is a basic description"
        optimized = optimize_description(base, "money", 45, config)
        
        assert len(optimized) > len(base)
        assert base in optimized or "This" in optimized
    
    def test_optimize_disabled(self):
        """Test when optimization is disabled."""
        config = DescriptionConfig()
        config.enable_optimization = False
        
        base = "This is a basic description"
        optimized = optimize_description(base, "money", 45, config)
        
        assert optimized == base
    
    def test_optimize_includes_timestamps(self):
        """Test that optimization includes timestamps."""
        config = DescriptionConfig()
        config.enable_optimization = True
        config.add_timestamps = True
        
        base = "Description"
        optimized = optimize_description(base, "money", 60, config)
        
        assert "⏱️" in optimized or "TIMESTAMPS" in optimized.upper()
    
    def test_optimize_includes_keywords(self):
        """Test that optimization includes keywords."""
        config = DescriptionConfig()
        config.enable_optimization = True
        config.add_keywords = True
        
        base = "Description"
        optimized = optimize_description(base, "money", 45, config)
        
        assert "🔍" in optimized or "KEYWORDS" in optimized.upper()
    
    def test_optimize_includes_cta(self):
        """Test that optimization includes CTA."""
        config = DescriptionConfig()
        config.enable_optimization = True
        config.add_cta = True
        
        base = "Description"
        optimized = optimize_description(base, "money", 45, config)
        
        assert "👍" in optimized or "subscribe" in optimized.lower()
    
    def test_optimize_respects_max_length(self):
        """Test that optimization respects max length."""
        config = DescriptionConfig()
        config.enable_optimization = True
        config.max_length = 100
        
        base = "A" * 50
        optimized = optimize_description(base, "money", 45, config)
        
        assert len(optimized) <= config.max_length


class TestAddAffiliateLinks:
    """Tests for adding affiliate links to description."""
    
    def test_add_empty_links(self):
        """Test adding empty links dict."""
        desc = "Original description"
        result = add_affiliate_links(desc, {})
        assert result == desc
    
    def test_add_affiliate_links(self):
        """Test adding affiliate links."""
        desc = "Original description"
        links = {
            "book": "https://amazon.com/book",
            "course": "https://example.com/course"
        }
        result = add_affiliate_links(desc, links)
        
        assert "Resources" in result or "resources" in result.lower()
        assert "https://amazon.com/book" in result
        assert "https://example.com/course" in result


class TestAddRelatedVideos:
    """Tests for adding related videos to description."""
    
    def test_add_empty_videos(self):
        """Test adding empty videos list."""
        desc = "Original description"
        result = add_related_videos(desc, [])
        assert result == desc
    
    def test_add_related_videos(self):
        """Test adding related videos."""
        desc = "Original description"
        videos = ["Video 1", "Video 2", "Video 3"]
        result = add_related_videos(desc, videos)
        
        assert "Video 1" in result
        assert "Video 2" in result
        assert "Video 3" in result
    
    def test_add_videos_max_limit(self):
        """Test that only max 5 videos are added."""
        desc = "Description"
        videos = [f"Video {i}" for i in range(10)]
        result = add_related_videos(desc, videos)
        
        # Should only include first 5
        assert "Video 5" in result
        assert "Video 6" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
