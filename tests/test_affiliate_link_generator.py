"""
Unit tests for affiliate_link_generator module.
"""

import pytest
import logging
from modules.affiliate_link_generator import (
    AffiliateConfig,
    extract_product_mentions,
    generate_affiliate_links,
    format_affiliate_links_for_description,
)


logger = logging.getLogger(__name__)


class TestAffiliateConfig:
    """Tests for AffiliateConfig class."""
    
    def test_init(self):
        """Test AffiliateConfig initialization."""
        config = AffiliateConfig()
        assert config.amazon_associate_id is not None
        assert isinstance(config.enable_amazon, bool)
        assert isinstance(config.enable_other, bool)
    
    def test_product_patterns(self):
        """Test product pattern mapping."""
        config = AffiliateConfig()
        assert "book" in config.product_patterns
        assert config.product_patterns["book"] == "amazon"


class TestExtractProductMentions:
    """Tests for product mention extraction."""
    
    def test_extract_no_mentions(self):
        """Test script with no product mentions."""
        script = "This is a generic script about motivation."
        products = extract_product_mentions(script)
        assert products == []
    
    def test_extract_book_mention(self):
        """Test extraction of book mentions."""
        script = "I recommend this amazing book for learning."
        products = extract_product_mentions(script)
        assert any(p["category"] == "book" for p in products)
    
    def test_extract_course_mention(self):
        """Test extraction of course mentions."""
        script = "Take this online course to master the topic."
        products = extract_product_mentions(script)
        assert any(p["category"] == "course" for p in products)
    
    def test_extract_tool_mention(self):
        """Test extraction of tool mentions."""
        script = "Use this great tool for productivity."
        products = extract_product_mentions(script)
        assert any(p["category"] == "tool" for p in products)
    
    def test_multiple_mentions(self):
        """Test extraction of multiple mentions."""
        script = "Read the book, take the course, and use the tool."
        products = extract_product_mentions(script)
        assert len(products) >= 3


class TestGenerateAffiliateLinks:
    """Tests for affiliate link generation."""
    
    def test_generate_disabled(self):
        """Test when affiliate generation is disabled."""
        config = AffiliateConfig()
        config.enable_amazon = False
        config.enable_other = False
        
        links = generate_affiliate_links("Check out this book", "money", config)
        assert links == {}
    
    def test_generate_amazon_links(self):
        """Test Amazon affiliate link generation."""
        config = AffiliateConfig()
        config.enable_amazon = True
        config.amazon_associate_id = "test-id"
        
        script = "This book is amazing"
        links = generate_affiliate_links(script, "money", config)
        
        assert len(links) > 0
        for link in links.values():
            assert "amazon.com" in link
            assert "test-id" in link
    
    def test_generate_no_products(self):
        """Test with script containing no products."""
        config = AffiliateConfig()
        config.enable_amazon = True
        
        script = "Just a random script about life."
        links = generate_affiliate_links(script, "money", config)
        assert links == {}


class TestFormatAffiliateLinks:
    """Tests for formatting affiliate links."""
    
    def test_format_empty_links(self):
        """Test formatting empty links dict."""
        result = format_affiliate_links_for_description({})
        assert result == ""
    
    def test_format_with_links(self):
        """Test formatting with actual links."""
        links = {
            "book": "https://amazon.com/book",
            "course": "https://example.com/course"
        }
        result = format_affiliate_links_for_description(links)
        
        assert "Resources mentioned" in result
        assert "book" in result.lower()
        assert "course" in result.lower()
        assert "https://amazon.com/book" in result
    
    def test_format_includes_emoji(self):
        """Test that format includes emoji."""
        links = {"book": "https://example.com"}
        result = format_affiliate_links_for_description(links)
        assert "📦" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
