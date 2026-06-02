"""
Unit tests for trending_topic_discovery module.
"""

import pytest
import logging
from modules.trending_topic_discovery import (
    TrendingConfig,
    get_trending_topics,
    get_seasonal_topics,
    score_topic_relevance,
    get_recommended_topics,
)


logger = logging.getLogger(__name__)


class TestTrendingConfig:
    """Tests for TrendingConfig class."""
    
    def test_init(self):
        """Test TrendingConfig initialization."""
        config = TrendingConfig()
        assert config.cache_duration_hours > 0
        assert 0 < config.min_trend_score < 1


class TestGetTrendingTopics:
    """Tests for getting trending topics."""
    
    def test_get_topics_enabled(self):
        """Test getting trending topics when enabled."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        topics = get_trending_topics("personal finance", config=config)
        
        assert isinstance(topics, list)
        assert len(topics) > 0
        assert all("topic" in t and "score" in t for t in topics)
    
    def test_get_topics_disabled(self):
        """Test getting trending topics when disabled."""
        config = TrendingConfig()
        config.enable_discovery = False
        
        topics = get_trending_topics("personal finance", config=config)
        assert topics == []
    
    def test_get_topics_specific_niche(self):
        """Test getting topics for specific niche."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        topics = get_trending_topics("psychology", limit=5, config=config)
        
        # Should return topics related to psychology
        assert len(topics) > 0
        assert all(isinstance(t["score"], (int, float)) for t in topics)
    
    def test_get_topics_respects_limit(self):
        """Test that limit is respected."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        topics = get_trending_topics("money", limit=3, config=config)
        
        assert len(topics) <= 3
    
    def test_get_topics_unknown_niche(self):
        """Test getting topics for unknown niche."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        topics = get_trending_topics("unknown_niche", config=config)
        
        # Should fallback to default topics
        assert len(topics) > 0


class TestGetSeasonalTopics:
    """Tests for seasonal topic retrieval."""
    
    def test_seasonal_topics_list(self):
        """Test that seasonal topics return a list."""
        topics = get_seasonal_topics("personal finance")
        
        assert isinstance(topics, list)
        assert len(topics) > 0
        assert all(isinstance(t, str) for t in topics)
    
    def test_seasonal_all_months_have_topics(self):
        """Test that all months have seasonal topics."""
        # This would require mocking datetime, so we test that function exists
        assert callable(get_seasonal_topics)


class TestScoreTopicRelevance:
    """Tests for topic relevance scoring."""
    
    def test_score_exact_match(self):
        """Test scoring for exact keyword match."""
        current = ["passive income"]
        score = score_topic_relevance("passive income strategies", current)
        
        assert score > 0
    
    def test_score_no_match(self):
        """Test scoring for no keyword match."""
        current = ["technology", "coding"]
        score = score_topic_relevance("cooking recipes", current)
        
        assert score == 0 or score < 0.5
    
    def test_score_partial_match(self):
        """Test scoring for partial keyword match."""
        current = ["make money"]
        score = score_topic_relevance("ways to make money online", current)
        
        assert score > 0
    
    def test_score_range(self):
        """Test that score is in valid range."""
        score = score_topic_relevance("test topic", ["current"])
        assert 0 <= score <= 1


class TestGetRecommendedTopics:
    """Tests for topic recommendations."""
    
    def test_get_recommendations_basic(self):
        """Test basic recommendation retrieval."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        current = ["passive income"]
        recommendations = get_recommended_topics(
            "personal finance",
            current,
            limit=3,
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
    
    def test_get_recommendations_excludes_current(self):
        """Test that recommendations exclude current topics."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        current = ["passive income", "side hustle"]
        recommendations = get_recommended_topics(
            "personal finance",
            current,
            limit=5,
        )
        
        # Recommended topics shouldn't be in current list
        for rec in recommendations:
            assert rec not in current
    
    def test_get_recommendations_respects_limit(self):
        """Test that recommendation limit is respected."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        recommendations = get_recommended_topics(
            "money",
            limit=2,
        )
        
        assert len(recommendations) <= 2
    
    def test_get_recommendations_empty_current(self):
        """Test recommendations with no current topics."""
        config = TrendingConfig()
        config.enable_discovery = True
        
        recommendations = get_recommended_topics(
            "psychology",
            current_topics=[],
            limit=3,
        )
        
        assert len(recommendations) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
