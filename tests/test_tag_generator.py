"""
Unit tests for tag_generator module.
"""

import pytest
import logging
from modules.tag_generator import (
    TagConfig,
    generate_tags,
    extract_keywords_from_title,
    extract_keywords_from_script,
    categorize_tags,
    validate_tags,
)


logger = logging.getLogger(__name__)


class TestTagConfig:
    """Tests for TagConfig class."""
    
    def test_init(self):
        """Test TagConfig initialization."""
        config = TagConfig()
        assert config.max_tags > 0
        assert config.min_tags > 0
        assert config.max_tags >= config.min_tags


class TestExtractKeywordsFromTitle:
    """Tests for keyword extraction from title."""
    
    def test_extract_from_simple_title(self):
        """Test keyword extraction from simple title."""
        title = "How to Make Money Online"
        keywords = extract_keywords_from_title(title)
        
        assert "make" in keywords
        assert "money" in keywords
        assert "online" in keywords
    
    def test_extract_filters_short_words(self):
        """Test that short words are filtered."""
        title = "a way to make money"
        keywords = extract_keywords_from_title(title)
        
        # Short words should be filtered
        assert all(len(k) > 3 for k in keywords)
    
    def test_extract_empty_title(self):
        """Test extraction from empty title."""
        keywords = extract_keywords_from_title("")
        assert keywords == set()


class TestExtractKeywordsFromScript:
    """Tests for keyword extraction from script."""
    
    def test_extract_from_script(self):
        """Test keyword extraction from script."""
        script = """
        Money is important. Making money is the goal.
        Learn about money management and investments.
        """
        keywords = extract_keywords_from_script(script, max_keywords=5)
        
        assert "money" in keywords or "making" in keywords
        assert len(keywords) <= 5
    
    def test_extract_ignores_stopwords(self):
        """Test that stopwords are ignored."""
        script = "the a is and or to of in that this"
        keywords = extract_keywords_from_script(script)
        
        # Should be mostly empty after stopword removal
        assert "the" not in keywords
        assert "and" not in keywords
    
    def test_extract_respects_max_limit(self):
        """Test that max keywords limit is respected."""
        script = "word1 word1 word2 word2 word3 word3 word4 word4 word5 word5"
        keywords = extract_keywords_from_script(script, max_keywords=3)
        
        assert len(keywords) <= 3


class TestGenerateTags:
    """Tests for tag generation."""
    
    def test_generate_tags_basic(self):
        """Test basic tag generation."""
        config = TagConfig()
        config.enable_generation = True
        
        tags = generate_tags("How to Make Money", "money", config=config)
        
        assert len(tags) > 0
        assert len(tags) <= config.max_tags
        assert "money" in tags or any("money" in tag.lower() for tag in tags)
    
    def test_generate_tags_disabled(self):
        """Test when tag generation is disabled."""
        config = TagConfig()
        config.enable_generation = False
        
        tags = generate_tags("How to Make Money", "money", config=config)
        assert tags == []
    
    def test_generate_tags_with_script(self):
        """Test tag generation with script text."""
        config = TagConfig()
        config.enable_generation = True
        
        tags = generate_tags(
            "Make Money",
            "money",
            "Learn about passive income and side hustles.",
            config=config
        )
        
        assert len(tags) > 0
        # Should include keywords from script
        tag_text = " ".join(tags).lower()
        assert any(word in tag_text for word in ["passive", "side", "hustle"])
    
    def test_generate_respects_max_tags(self):
        """Test that max tags limit is respected."""
        config = TagConfig()
        config.enable_generation = True
        config.max_tags = 10
        
        tags = generate_tags("How to Make Money Online Fast Now", "money", config=config)
        assert len(tags) <= config.max_tags
    
    def test_generate_includes_youtube_tag(self):
        """Test that YouTube tag is always included."""
        config = TagConfig()
        config.enable_generation = True
        
        tags = generate_tags("Any Title", "money", config=config)
        assert "youtube" in tags


class TestCategorizeTags:
    """Tests for tag categorization."""
    
    def test_categorize_tags(self):
        """Test tag categorization by length."""
        tags = ["ai", "money", "online business", "personal finance"]
        categories = categorize_tags(tags)
        
        assert "short" in categories
        assert "medium" in categories
        assert "long" in categories
        
        assert "ai" in categories["short"]
        assert "money" in categories["medium"]
    
    def test_categorize_all_categories(self):
        """Test that all category types are returned."""
        tags = ["a", "med", "medium word", "very long tag name"]
        categories = categorize_tags(tags)
        
        for category_type in ["short", "medium", "long"]:
            assert category_type in categories


class TestValidateTags:
    """Tests for tag validation."""
    
    def test_validate_valid_tags(self):
        """Test validation of valid tags."""
        tags = ["money", "online", "business"]
        validation = validate_tags(tags)
        
        assert validation["within_limit"] is True
        assert validation["all_non_empty"] is True
        assert validation["all_strings"] is True
        assert len(validation["issues"]) == 0
    
    def test_validate_too_many_tags(self):
        """Test validation with too many tags."""
        tags = [f"tag{i}" for i in range(35)]
        validation = validate_tags(tags)
        
        assert validation["within_limit"] is False
        assert len(validation["issues"]) > 0
    
    def test_validate_empty_tags(self):
        """Test validation with empty tags."""
        tags = ["valid", "", "another"]
        validation = validate_tags(tags)
        
        assert validation["all_non_empty"] is False
        assert len(validation["issues"]) > 0
    
    def test_validate_count(self):
        """Test that validation counts tags correctly."""
        tags = ["tag1", "tag2", "tag3"]
        validation = validate_tags(tags)
        
        assert validation["total_count"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
