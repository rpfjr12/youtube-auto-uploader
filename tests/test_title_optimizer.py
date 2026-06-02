"""
Unit tests for title_optimizer module.
"""

import pytest
import logging
from modules.title_optimizer import (
    TitleConfig,
    optimize_title,
    generate_title_variants,
    analyze_title_quality,
    get_power_word_for_topic,
    add_number_hook,
)


logger = logging.getLogger(__name__)


class TestTitleConfig:
    """Tests for TitleConfig class."""
    
    def test_init(self):
        """Test TitleConfig initialization."""
        config = TitleConfig()
        assert config.max_length > 0
        assert isinstance(config.enable_optimization, bool)
        assert isinstance(config.use_power_words, bool)
        assert isinstance(config.use_numbers, bool)


class TestGetPowerWord:
    """Tests for power word selection."""
    
    def test_get_word_for_money(self):
        """Test power word for money topic."""
        word = get_power_word_for_topic("money")
        assert word in ["Proven", "Guaranteed", "Simple"]
    
    def test_get_word_for_motivation(self):
        """Test power word for motivation topic."""
        word = get_power_word_for_topic("motivation")
        assert word in ["Incredible", "Amazing", "Ultimate"]
    
    def test_get_word_for_psychology(self):
        """Test power word for psychology topic."""
        word = get_power_word_for_topic("psychology")
        assert word in ["Shocking", "Surprising", "Secret"]
    
    def test_get_word_default(self):
        """Test power word for unknown topic."""
        word = get_power_word_for_topic("unknown_topic")
        assert len(word) > 0


class TestAddNumberHook:
    """Tests for number hook addition."""
    
    def test_add_number_to_title_without_number(self):
        """Test adding number to title without one."""
        title = "How to Make Money"
        result = add_number_hook(title)
        assert result.startswith("3 Ways:")
        assert "How to Make Money" in result
    
    def test_preserve_number_if_exists(self):
        """Test that existing numbers are preserved."""
        title = "5 Ways to Make Money"
        result = add_number_hook(title)
        assert result == title
    
    def test_number_in_middle_adds_prefix(self):
        """Test title with number in middle."""
        title = "How to Make 100 Dollars"
        result = add_number_hook(title)
        assert result.startswith("3 Ways:")


class TestOptimizeTitle:
    """Tests for title optimization."""
    
    def test_optimize_basic_title(self):
        """Test basic title optimization."""
        config = TitleConfig()
        config.enable_optimization = True
        
        title = "How to Make Money"
        optimized = optimize_title(title, "money", config)
        
        assert len(optimized) > 0
        assert len(optimized) <= config.max_length
    
    def test_optimize_disabled(self):
        """Test when optimization is disabled."""
        config = TitleConfig()
        config.enable_optimization = False
        
        title = "How to Make Money"
        result = optimize_title(title, "money", config)
        assert result == title
    
    def test_optimize_truncates_long_title(self):
        """Test that very long titles are truncated."""
        config = TitleConfig()
        config.enable_optimization = True
        config.max_length = 30
        
        long_title = "This is an extremely long title that should be truncated"
        optimized = optimize_title(long_title, "money", config)
        
        assert len(optimized) <= config.max_length
    
    def test_optimize_with_power_words(self):
        """Test optimization includes power words."""
        config = TitleConfig()
        config.enable_optimization = True
        config.use_power_words = True
        
        title = "How to Make Money"
        optimized = optimize_title(title, "money", config)
        
        # Should contain a power word
        power_words = ["Proven", "Guaranteed", "Simple"]
        assert any(word in optimized for word in power_words)
    
    def test_optimize_with_numbers(self):
        """Test optimization includes numbers."""
        config = TitleConfig()
        config.enable_optimization = True
        config.use_numbers = True
        
        title = "How to Make Money"
        optimized = optimize_title(title, "money", config)
        
        # Should contain a number
        assert any(char.isdigit() for char in optimized)


class TestGenerateTitleVariants:
    """Tests for title variant generation."""
    
    def test_generate_variants_count(self):
        """Test correct number of variants generated."""
        title = "How to Make Money Online"
        variants = generate_title_variants(title, "money", count=3)
        
        assert len(variants) <= 3
        assert len(variants) > 0
    
    def test_generate_variants_uniqueness(self):
        """Test that variants are reasonably different."""
        title = "How to Make Money"
        variants = generate_title_variants(title, "money", count=5)
        
        # Should have multiple different variants
        unique_variants = set(variants)
        assert len(unique_variants) > 1
    
    def test_generate_variants_question_format(self):
        """Test question format variant generation."""
        title = "Make Money Online"
        variants = generate_title_variants(title, "money", count=5)
        
        # At least one should be question format
        question_variants = [v for v in variants if "?" in v]
        assert len(question_variants) > 0


class TestAnalyzeTitleQuality:
    """Tests for title quality analysis."""
    
    def test_analyze_quality_metrics(self):
        """Test quality analysis returns all metrics."""
        title = "5 Ways: How to Make Money Online"
        quality = analyze_title_quality(title)
        
        assert "length" in quality
        assert "word_count" in quality
        assert "has_number" in quality
        assert "has_power_word" in quality
        assert "has_question" in quality
        assert "readability_score" in quality
    
    def test_analyze_detects_numbers(self):
        """Test detection of numbers."""
        title = "5 Ways to Make Money"
        quality = analyze_title_quality(title)
        assert quality["has_number"] is True
    
    def test_analyze_detects_questions(self):
        """Test detection of questions."""
        title = "How to Make Money?"
        quality = analyze_title_quality(title)
        assert quality["has_question"] is True
    
    def test_analyze_readability_score(self):
        """Test readability score is in valid range."""
        title = "How to Make Money"
        quality = analyze_title_quality(title)
        assert 0 <= quality["readability_score"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
