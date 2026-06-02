# YouTube Auto Uploader - Feature Documentation

Complete documentation for all features and modules in the YouTube automation system.

---

## Table of Contents

1. [Affiliate Link Generator](#affiliate-link-generator)
2. [Thumbnail Generator](#thumbnail-generator)
3. [Title Optimizer](#title-optimizer)
4. [Description Optimizer](#description-optimizer)
5. [Tag Generator](#tag-generator)
6. [Trending Topic Discovery](#trending-topic-discovery)
7. [Frequency Scaler](#frequency-scaler)
8. [Multi-Channel Support](#multi-channel-support)

---

## Affiliate Link Generator

**Module:** `modules/affiliate_link_generator.py`

### Purpose
Automatically generates affiliate links for products mentioned in video scripts. Helps monetize content without manual link management.

### Features
- ✅ Product mention extraction from scripts
- ✅ Multiple affiliate network support
- ✅ Amazon Associate integration
- ✅ Link formatting for descriptions
- ✅ Performance tracking

### Environment Variables
```env
ENABLE_AFFILIATE_AMAZON=true
AMAZON_ASSOCIATE_ID=your-associate-id
```

### Usage

```python
from modules.affiliate_link_generator import (
    AffiliateConfig,
    generate_affiliate_links,
    format_affiliate_links_for_description
)

# Create configuration
config = AffiliateConfig()
config.enable_amazon = True
config.amazon_associate_id = "myassociate-20"

# Generate links from script
script = "Check out this amazing book and course..."
links = generate_affiliate_links(script, topic="money", affiliate_config=config)

# Format for description
description_section = format_affiliate_links_for_description(links)
print(description_section)
# Output:
# 📦 Resources mentioned:
# • Book: https://amazon.com/s?k=book&tag=myassociate-20
# • Course: https://teachable.com/...
```

### Detected Product Categories
- `book` - Books, ebooks, guides
- `course` - Online courses, training
- `tool` - Software, applications, utilities
- `app` - Mobile or web applications
- `software` - Commercial software

### API Reference

#### `extract_product_mentions(script_text: str) -> List[Dict]`
Extracts product mentions from script text.

**Returns:** List of dicts with `product`, `category`, and `count` keys

#### `generate_affiliate_links(script_text, topic, affiliate_config) -> Dict[str, str]`
Generates affiliate links for products in script.

**Returns:** Dict mapping products to affiliate URLs

#### `format_affiliate_links_for_description(links: Dict) -> str`
Formats links for inclusion in video description.

**Returns:** Formatted markdown string

---

## Thumbnail Generator

**Module:** `modules/thumbnail_generator.py`

### Purpose
Creates eye-catching video thumbnails automatically with topic-specific colors and emoji.

### Features
- ✅ Automatic thumbnail generation
- ✅ Topic-based color palette
- ✅ Emoji integration
- ✅ Text sizing optimization
- ✅ Border styling

### Environment Variables
```env
ENABLE_THUMBNAILS=true
```

### Usage

```python
from modules.thumbnail_generator import (
    ThumbnailConfig,
    generate_thumbnail,
    get_emoji_for_topic
)

# Configuration
config = ThumbnailConfig()
config.enable_thumbnails = True

# Generate thumbnail
title = "How to Make Money Online"
emoji = get_emoji_for_topic("money")  # Returns "💰"

thumbnail_path = generate_thumbnail(
    title=title,
    topic="money",
    emoji=emoji,
    output_dir="uploads",
    config=config
)

print(f"Thumbnail saved to: {thumbnail_path}")
```

### Topic-Color Mapping
- `money` → Gold (255, 193, 7)
- `motivation` → Green (76, 175, 80)
- `psychology` → Purple (103, 58, 183)
- `technology` → Blue (33, 150, 243)
- `general` → Red (244, 67, 54)

### Topic-Emoji Mapping
- `money` → 💰
- `motivation` → 🚀
- `psychology` → 🧠
- `technology` → 💻
- `fitness` → 💪
- `cooking` → 🍳
- `travel` → ✈️
- `business` → 📊

### API Reference

#### `generate_thumbnail(title, topic, emoji, output_dir, config) -> str`
Generates a 1280x720 thumbnail image.

**Parameters:**
- `title` (str): Video title (max 20 chars, auto-truncated)
- `topic` (str): Video topic (determines color)
- `emoji` (str, optional): Emoji to include
- `output_dir` (str): Directory for output files
- `config` (ThumbnailConfig, optional): Configuration

**Returns:** Path to generated thumbnail PNG file

#### `get_emoji_for_topic(topic: str) -> str`
Gets recommended emoji for a topic.

**Returns:** Single emoji string

---

## Title Optimizer

**Module:** `modules/title_optimizer.py`

### Purpose
Optimizes video titles for SEO and click-through rate by adding power words and numbers.

### Features
- ✅ Power word injection
- ✅ Number hook addition
- ✅ Length validation
- ✅ A/B testing variants
- ✅ Quality metrics analysis

### Environment Variables
```env
ENABLE_TITLE_OPTIMIZATION=true
USE_POWER_WORDS=true
USE_NUMBERS=true
TITLE_MAX_LENGTH=60
```

### Usage

```python
from modules.title_optimizer import (
    TitleConfig,
    optimize_title,
    generate_title_variants,
    analyze_title_quality
)

# Configuration
config = TitleConfig()
config.enable_optimization = True

# Optimize title
base_title = "How to Make Money Online"
optimized = optimize_title(base_title, topic="money", config=config)
# Output: "5 Ways: Proven How to Make Money Online"

# Generate variants for A/B testing
variants = generate_title_variants(base_title, "money", count=3)
# Output: ["5 Ways: Proven How to Make Money Online",
#          "How to Make Money Online?",
#          "How to Make Money..."]

# Analyze quality
quality = analyze_title_quality(optimized)
print(quality)
# Output: {
#     "length": 41,
#     "word_count": 8,
#     "has_number": True,
#     "has_power_word": True,
#     "has_question": False,
#     "readability_score": 85.5
# }
```

### Power Words by Topic
- **money** - Proven, Guaranteed, Simple
- **motivation** - Incredible, Amazing, Ultimate
- **psychology** - Shocking, Surprising, Secret
- **technology** - Viral, Essential, Must-See

### API Reference

#### `optimize_title(base_title, topic, config) -> str`
Optimizes a title for SEO and CTR.

#### `generate_title_variants(base_title, topic, count) -> List[str]`
Generates multiple title variants for A/B testing.

#### `analyze_title_quality(title) -> Dict`
Analyzes title quality and returns metrics.

---

## Description Optimizer

**Module:** `modules/description_optimizer.py`

### Purpose
Auto-generates optimized video descriptions with timestamps, keywords, CTAs, and affiliate links.

### Features
- ✅ Auto-timestamp generation
- ✅ SEO keyword insertion
- ✅ CTA (Call-to-Action) injection
- ✅ Affiliate link integration
- ✅ Related videos section

### Environment Variables
```env
ENABLE_DESCRIPTION_OPTIMIZATION=true
ADD_TIMESTAMPS=true
ADD_KEYWORDS=true
ADD_CTA=true
DESCRIPTION_MAX_LENGTH=5000
```

### Usage

```python
from modules.description_optimizer import (
    DescriptionConfig,
    optimize_description,
    add_affiliate_links,
    add_related_videos
)

# Configuration
config = DescriptionConfig()
config.enable_optimization = True

# Generate optimized description
base_desc = "Learn about passive income strategies"
optimized = optimize_description(
    base_desc,
    topic="money",
    video_duration=45,
    config=config
)

# Add affiliate links
affiliate_links = {
    "book": "https://amazon.com/book",
    "course": "https://example.com/course"
}
with_links = add_affiliate_links(optimized, affiliate_links)

# Add related videos
related = ["Video 1", "Video 2", "Video 3"]
final = add_related_videos(with_links, related)

print(final)
```

### Auto-Generated Sections
1. **Timestamps** - Chapter markers with 🕐 emoji
2. **Keywords** - SEO keywords with 🔍 emoji
3. **CTA** - Call-to-action with 👍 emoji
4. **Resources** - Affiliate links (if provided)
5. **Related Videos** - Links to related content
6. **Disclaimer** - Legal footer

### API Reference

#### `optimize_description(base_description, topic, video_duration, config) -> str`
Optimizes description with all sections.

#### `add_affiliate_links(description, affiliate_links) -> str`
Adds affiliate links section.

#### `add_related_videos(description, related_videos) -> str`
Adds related videos section.

#### `generate_timestamps(video_duration) -> List[str]`
Generates chapter timestamps.

---

## Tag Generator

**Module:** `modules/tag_generator.py`

### Purpose
Intelligently generates YouTube tags from title and script content with SEO optimization.

### Features
- ✅ Title keyword extraction
- ✅ Script keyword extraction
- ✅ Topic-specific tag database
- ✅ Trending tag inclusion
- ✅ YouTube compliance (max 30 tags)

### Environment Variables
```env
ENABLE_TAG_GENERATION=true
USE_BROAD_TAGS=true
USE_NICHE_TAGS=true
MAX_TAGS=30
MIN_TAGS=8
```

### Usage

```python
from modules.tag_generator import (
    TagConfig,
    generate_tags,
    categorize_tags,
    validate_tags
)

# Configuration
config = TagConfig()
config.enable_generation = True

# Generate tags
title = "5 Secret Ways to Make Money Online"
topic = "money"
script = "Learn passive income strategies and side hustles..."

tags = generate_tags(title, topic, script, config=config)
print(f"Generated {len(tags)} tags:")
print(tags)
# Output: ['money', 'make money', 'passive income', 'side hustle', ...]

# Categorize by length
categories = categorize_tags(tags)
print(categories)
# Output: {
#     'short': ['ai', 'money'],
#     'medium': ['income', 'passive'],
#     'long': ['passive income', 'make money online']
# }

# Validate for YouTube
validation = validate_tags(tags)
print(validation)
# Output: {
#     'total_count': 28,
#     'within_limit': True,
#     'all_non_empty': True,
#     'all_strings': True,
#     'issues': []
# }
```

### Topic Tag Categories
Each topic has three tag categories:
- **Broad** - General topic tags
- **Niche** - Specific sub-topics
- **Trending** - Currently trending tags

### API Reference

#### `generate_tags(title, topic, script_text, config) -> List[str]`
Generates optimized tag list.

#### `categorize_tags(tags) -> Dict`
Categorizes tags by length (short/medium/long).

#### `validate_tags(tags) -> Dict`
Validates tags for YouTube requirements.

---

## Trending Topic Discovery

**Module:** `modules/trending_topic_discovery.py`

### Purpose
Discovers trending topics in your niche to keep content relevant and timely.

### Features
- ✅ Trending topic database
- ✅ Seasonal content suggestions
- ✅ Topic relevance scoring
- ✅ Channel-specific recommendations
- ✅ Growth trend indicators

### Environment Variables
```env
ENABLE_TRENDING_DISCOVERY=true
TRENDING_CACHE_HOURS=24
MIN_TREND_SCORE=0.5
```

### Usage

```python
from modules.trending_topic_discovery import (
    TrendingConfig,
    get_trending_topics,
    get_seasonal_topics,
    get_recommended_topics
)

# Configuration
config = TrendingConfig()
config.enable_discovery = True

# Get trending topics for niche
trending = get_trending_topics(
    niche="personal finance",
    region="US",
    limit=10,
    config=config
)

for topic in trending[:5]:
    print(f"{topic['topic']}: {topic['score']:.2f} ({topic['growth']})")

# Get seasonal topics
seasonal = get_seasonal_topics("personal finance")
print(f"Seasonal topics: {seasonal}")

# Get recommendations for your channel
current_topics = ["passive income", "side hustle"]
recommendations = get_recommended_topics(
    "personal finance",
    current_topics,
    limit=5
)
print(f"Recommended next topics: {recommendations}")
```

### Topic Data Structure
Each topic includes:
- `topic` (str) - Topic name
- `score` (float) - Trend score (0-1)
- `growth` (str) - Growth rate (high/medium/steady/volatile)

### Growth Indicators
- **viral** - Exploding growth
- **high** - Strong growth trend
- **medium** - Moderate growth
- **steady** - Consistent interest
- **volatile** - Unpredictable changes

### API Reference

#### `get_trending_topics(niche, region, limit, config) -> List[Dict]`
Gets trending topics for a niche.

#### `get_seasonal_topics(niche) -> List[str]`
Gets seasonal topics based on current month.

#### `get_recommended_topics(niche, current_topics, limit) -> List[str]`
Gets topic recommendations based on current content.

---

## Frequency Scaler

**Module:** `modules/frequency_scaler.py`

### Purpose
Automatically adjusts posting frequency based on channel performance to optimize growth and prevent burnout.

### Features
- ✅ Performance-based frequency scaling
- ✅ Burnout risk calculation
- ✅ Engagement tracking
- ✅ Watch time analysis
- ✅ Sustainability recommendations

### Environment Variables
```env
ENABLE_FREQUENCY_SCALING=true
MIN_UPLOAD_FREQUENCY=1
MAX_UPLOAD_FREQUENCY=5
ENGAGEMENT_THRESHOLD=0.05
MIN_VIEWS_PER_VIDEO=100
```

### Usage

```python
from modules.frequency_scaler import (
    FrequencyScalerConfig,
    calculate_optimal_frequency,
    get_burnout_risk_score,
    get_frequency_recommendation
)

# Configuration
config = FrequencyScalerConfig()
config.enable_scaling = True

# Channel stats
stats = {
    "avg_views": 5000,
    "avg_engagement": 0.08,  # 8%
    "avg_watch_time": 20  # minutes
}

# Calculate optimal frequency
optimal = calculate_optimal_frequency(
    stats,
    current_frequency=3,
    config=config
)
print(f"Optimal frequency: {optimal} videos/day")

# Calculate burnout risk
risk = get_burnout_risk_score(
    upload_frequency=3,
    days_active=60
)
print(f"Burnout risk: {risk:.2f} (0=safe, 1=high)")

# Get recommendation
recommendation = get_frequency_recommendation(3, risk)
print(f"Recommendation: {recommendation['recommended']} videos/day")
print(f"Risk level: {recommendation['risk_level']}")
for reason in recommendation['reasoning']:
    print(f"  - {reason}")
```

### Risk Levels
- **very_low** (< 0.3) - Very safe, can increase frequency
- **low** (0.3-0.5) - Safe, maintain current frequency
- **moderate** (0.5-0.7) - Consider reducing frequency
- **high** (> 0.7) - Reduce frequency to prevent burnout

### API Reference

#### `calculate_optimal_frequency(channel_stats, current_frequency, config) -> int`
Calculates recommended upload frequency.

#### `get_burnout_risk_score(upload_frequency, days_active) -> float`
Calculates burnout risk (0-1).

#### `get_frequency_recommendation(current_frequency, burnout_risk) -> Dict`
Gets frequency recommendation with reasoning.

---

## Multi-Channel Support

**Module:** `modules/multi_channel_support.py`

### Purpose
Manage and upload to multiple YouTube channels from a single configuration.

### Features
- ✅ Multi-channel configuration management
- ✅ Per-channel upload schedules
- ✅ Synced uploads to multiple channels
- ✅ Persistent configuration storage
- ✅ Channel enable/disable toggling

### Usage

```python
from modules.multi_channel_support import (
    ChannelConfig,
    MultiChannelScheduler,
    sync_upload_across_channels,
    batch_upload
)

# Create scheduler
scheduler = MultiChannelScheduler("channel_config.json")

# Add channels
scheduler.add_channel(
    name="Main Channel",
    channel_id="UCmain123",
    upload_times=["09:00", "14:00"],
    max_per_day=2,
    topics=["money", "motivation"]
)

scheduler.add_channel(
    name="Backup Channel",
    channel_id="UCbackup456",
    upload_times=["20:00"],
    max_per_day=1,
    topics=["psychology"]
)

# Enable/disable channels
scheduler.disable_channel("Backup Channel")
scheduler.enable_channel("Backup Channel")

# Get active channels
active = scheduler.get_active_channels()
print(f"Active channels: {len(active)}")

# Get scheduler status
status = scheduler.get_status()
print(status)
# Output: {
#     'total_channels': 2,
#     'active_channels': 2,
#     'channels': [...],
#     'stats': {...}
# }

# Sync upload to multiple channels
videos = [
    {
        "path": "video1.mp4",
        "title": "Video 1",
        "description": "Desc 1",
        "tags": ["tag1"]
    }
]

results = batch_upload(scheduler, videos)
print(results)
# Output: {
#     'total_videos': 1,
#     'total_channels': 2,
#     'uploads': [{...}]
# }
```

### Configuration File Format

```json
{
  "channels": [
    {
      "name": "Main Channel",
      "channel_id": "UCmain123",
      "upload_times": ["09:00", "14:00"],
      "max_per_day": 2,
      "topics": ["money", "motivation"],
      "enabled": true
    },
    {
      "name": "Backup Channel",
      "channel_id": "UCbackup456",
      "upload_times": ["20:00"],
      "max_per_day": 1,
      "topics": ["psychology"],
      "enabled": true
    }
  ]
}
```

### API Reference

#### `ChannelConfig(name, channel_id, upload_times, max_per_day, topics, enabled)`
Configuration for a single YouTube channel.

#### `MultiChannelScheduler(config_file) -> scheduler`
Main scheduler for managing multiple channels.

Methods:
- `add_channel()` - Add a new channel
- `remove_channel()` - Remove a channel
- `enable_channel()` - Enable a channel
- `disable_channel()` - Disable a channel
- `get_active_channels()` - Get enabled channels
- `get_status()` - Get full status

#### `sync_upload_across_channels(channels, video_path, title, description, tags) -> Dict`
Upload same video to multiple channels.

#### `batch_upload(scheduler, videos) -> Dict`
Upload multiple videos to multiple channels.

---

**Last Updated:** June 2, 2026  
**Version:** 2.0.0
