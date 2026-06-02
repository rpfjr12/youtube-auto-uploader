"""
Affiliate Link Generator Module

Automatically generates affiliate links for relevant products mentioned in video scripts.
Supports multiple affiliate networks and tracks performance.

Usage:
    from modules.affiliate_link_generator import generate_affiliate_links
    
    links = generate_affiliate_links(
        script_text="Check out this product...",
        topic="money",
        affiliate_config=config
    )
"""

import os
import logging
from typing import Dict, List, Optional
from urllib.parse import urlencode, quote

logger = logging.getLogger(__name__)


class AffiliateConfig:
    """Configuration for affiliate link generation."""
    
    def __init__(self):
        """Initialize affiliate configuration from environment or defaults."""
        self.amazon_associate_id = os.getenv("AMAZON_ASSOCIATE_ID", "")
        self.enable_amazon = os.getenv("ENABLE_AFFILIATE_AMAZON", "false").lower() == "true"
        self.enable_other = os.getenv("ENABLE_AFFILIATE_OTHER", "false").lower() == "true"
        
        # Mapping of product keywords to affiliate networks
        self.product_patterns = {
            "book": "amazon",
            "course": "teachable",
            "tool": "amazon",
            "software": "affiliate_network",
            "app": "appstore",
        }


def extract_product_mentions(script_text: str) -> List[Dict[str, str]]:
    """
    Extract product mentions from script text.
    
    Args:
        script_text: The video script text
        
    Returns:
        List of dicts with 'product' and 'category' keys
    """
    products = []
    keywords = {
        "book": ["book", "ebook", "guide"],
        "course": ["course", "training", "class"],
        "tool": ["tool", "software", "app"],
    }
    
    script_lower = script_text.lower()
    
    for category, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in script_lower:
                products.append({
                    "product": keyword,
                    "category": category,
                    "count": script_lower.count(keyword)
                })
    
    return products


def generate_affiliate_links(
    script_text: str,
    topic: str = "general",
    affiliate_config: Optional[AffiliateConfig] = None
) -> Dict[str, str]:
    """
    Generate affiliate links for products mentioned in script.
    
    Args:
        script_text: The video script text
        topic: The video topic
        affiliate_config: Optional AffiliateConfig instance
        
    Returns:
        Dictionary mapping products to affiliate links
    """
    if affiliate_config is None:
        affiliate_config = AffiliateConfig()
    
    logger.info(f"Generating affiliate links for topic: {topic}")
    
    if not affiliate_config.enable_amazon and not affiliate_config.enable_other:
        logger.debug("Affiliate links disabled in configuration")
        return {}
    
    products = extract_product_mentions(script_text)
    if not products:
        logger.debug("No product mentions found in script")
        return {}
    
    affiliate_links = {}
    
    for product in products:
        if affiliate_config.enable_amazon:
            # Generate Amazon affiliate link (placeholder format)
            search_query = quote(f"{product['product']} {topic}")
            affiliate_links[product['product']] = (
                f"https://amazon.com/s?k={search_query}&tag={affiliate_config.amazon_associate_id}"
            )
            logger.info(f"Generated Amazon link for: {product['product']}")
    
    return affiliate_links


def format_affiliate_links_for_description(links: Dict[str, str]) -> str:
    """
    Format affiliate links for video description.
    
    Args:
        links: Dictionary of affiliate links
        
    Returns:
        Formatted string ready for video description
    """
    if not links:
        return ""
    
    formatted = "\n📦 Resources mentioned:\n"
    for product, link in links.items():
        formatted += f"• {product.title()}: {link}\n"
    
    return formatted


def get_affiliate_stats() -> Dict[str, int]:
    """Get affiliate link statistics (placeholder)."""
    return {
        "total_links_generated": 0,
        "click_through_rate": 0,
        "conversion_rate": 0,
    }


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    sample_script = """
    In this video, we discuss money management using a popular book on finance.
    I recommend taking a course on investing. Check out this amazing tool for tracking expenses.
    """
    
    config = AffiliateConfig()
    config.amazon_associate_id = "test-affiliate-id"
    config.enable_amazon = True
    
    links = generate_affiliate_links(sample_script, "money", config)
    print("Generated Links:")
    print(format_affiliate_links_for_description(links))
