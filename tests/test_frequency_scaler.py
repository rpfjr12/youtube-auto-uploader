"""
Unit tests for frequency_scaler module.
"""

import pytest
import logging
from modules.frequency_scaler import (
    FrequencyScalerConfig,
    calculate_engagement_rate,
    calculate_average_performance,
    calculate_optimal_frequency,
    get_burnout_risk_score,
    get_frequency_recommendation,
)


logger = logging.getLogger(__name__)


class TestFrequencyScalerConfig:
    """Tests for FrequencyScalerConfig class."""
    
    def test_init(self):
        """Test FrequencyScalerConfig initialization."""
        config = FrequencyScalerConfig()
        assert config.min_frequency >= 1
        assert config.max_frequency >= config.min_frequency
        assert 0 < config.engagement_threshold < 1


class TestCalculateEngagementRate:
    """Tests for engagement rate calculation."""
    
    def test_calculate_rate_basic(self):
        """Test basic engagement rate calculation."""
        stats = {
            "views": 1000,
            "likes": 50,
            "comments": 20,
            "shares": 5,
        }
        rate = calculate_engagement_rate(stats)
        
        assert rate == 0.075  # (50 + 20 + 5) / 1000
    
    def test_calculate_rate_no_engagement(self):
        """Test engagement rate with no engagement."""
        stats = {
            "views": 1000,
            "likes": 0,
            "comments": 0,
            "shares": 0,
        }
        rate = calculate_engagement_rate(stats)
        assert rate == 0.0
    
    def test_calculate_rate_zero_views(self):
        """Test engagement rate with zero views."""
        stats = {
            "views": 0,
            "likes": 10,
        }
        rate = calculate_engagement_rate(stats)
        assert rate >= 0  # Should not crash


class TestCalculateAveragePerformance:
    """Tests for average performance calculation."""
    
    def test_average_empty_history(self):
        """Test with empty video history."""
        avg = calculate_average_performance([])
        
        assert avg["avg_views"] == 0
        assert avg["video_count"] == 0
    
    def test_average_single_video(self):
        """Test average with single video."""
        history = [
            {"views": 1000, "watch_time_minutes": 30}
        ]
        avg = calculate_average_performance(history)
        
        assert avg["avg_views"] == 1000
        assert avg["video_count"] == 1
    
    def test_average_multiple_videos(self):
        """Test average with multiple videos."""
        history = [
            {"views": 1000, "likes": 100, "watch_time_minutes": 30},
            {"views": 2000, "likes": 200, "watch_time_minutes": 40},
        ]
        avg = calculate_average_performance(history)
        
        assert avg["avg_views"] == 1500
        assert avg["video_count"] == 2


class TestCalculateOptimalFrequency:
    """Tests for optimal frequency calculation."""
    
    def test_optimal_high_engagement(self):
        """Test frequency increase with high engagement."""
        stats = {
            "avg_views": 10000,
            "avg_engagement": 0.12,  # 12%
            "avg_watch_time": 25,
        }
        config = FrequencyScalerConfig()
        config.enable_scaling = True
        
        optimal = calculate_optimal_frequency(stats, current_frequency=3, config=config)
        
        # High engagement should increase frequency
        assert optimal >= 3
    
    def test_optimal_low_views(self):
        """Test frequency decrease with low views."""
        stats = {
            "avg_views": 50,
            "avg_engagement": 0.02,
            "avg_watch_time": 5,
        }
        config = FrequencyScalerConfig()
        config.enable_scaling = True
        config.min_views_per_video = 100
        
        optimal = calculate_optimal_frequency(stats, current_frequency=3, config=config)
        
        # Low views should decrease frequency
        assert optimal <= 3
    
    def test_optimal_disabled(self):
        """Test when frequency scaling is disabled."""
        stats = {"avg_views": 100}
        config = FrequencyScalerConfig()
        config.enable_scaling = False
        
        optimal = calculate_optimal_frequency(stats, current_frequency=3, config=config)
        assert optimal == 3  # Should return current frequency
    
    def test_optimal_respects_limits(self):
        """Test that optimal respects min/max limits."""
        stats = {"avg_views": 10000, "avg_engagement": 0.5}
        config = FrequencyScalerConfig()
        config.enable_scaling = True
        config.min_frequency = 1
        config.max_frequency = 5
        
        optimal = calculate_optimal_frequency(stats, current_frequency=3, config=config)
        
        assert config.min_frequency <= optimal <= config.max_frequency


class TestGetBurnoutRiskScore:
    """Tests for burnout risk score calculation."""
    
    def test_risk_low_frequency(self):
        """Test low risk with low upload frequency."""
        risk = get_burnout_risk_score(upload_frequency=1, days_active=60)
        assert risk < 0.3
    
    def test_risk_high_frequency(self):
        """Test high risk with high upload frequency."""
        risk = get_burnout_risk_score(upload_frequency=5, days_active=7)
        assert risk > 0.5
    
    def test_risk_new_channel_high_frequency(self):
        """Test risk for new channel with high frequency."""
        risk = get_burnout_risk_score(upload_frequency=5, days_active=5)
        assert risk > 0.6
    
    def test_risk_established_channel(self):
        """Test risk for established channel."""
        risk = get_burnout_risk_score(upload_frequency=2, days_active=180)
        assert risk < 0.3
    
    def test_risk_score_range(self):
        """Test that risk score is in valid range."""
        risk = get_burnout_risk_score(upload_frequency=3, days_active=30)
        assert 0 <= risk <= 1


class TestGetFrequencyRecommendation:
    """Tests for frequency recommendation."""
    
    def test_recommendation_low_risk(self):
        """Test recommendation for low risk."""
        rec = get_frequency_recommendation(current_frequency=3, burnout_risk=0.2)
        
        assert rec["risk_level"] == "very_low"
        assert len(rec["reasoning"]) > 0
    
    def test_recommendation_high_risk(self):
        """Test recommendation for high risk."""
        rec = get_frequency_recommendation(current_frequency=5, burnout_risk=0.8)
        
        assert rec["risk_level"] == "high"
        assert rec["recommended"] < rec["current"]
    
    def test_recommendation_moderate_risk(self):
        """Test recommendation for moderate risk."""
        rec = get_frequency_recommendation(current_frequency=3, burnout_risk=0.5)
        
        assert rec["risk_level"] == "moderate"
        assert "reasoning" in rec
    
    def test_recommendation_has_all_fields(self):
        """Test that recommendation has all required fields."""
        rec = get_frequency_recommendation(3, 0.4)
        
        assert "current" in rec
        assert "recommended" in rec
        assert "reasoning" in rec
        assert "risk_level" in rec


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
