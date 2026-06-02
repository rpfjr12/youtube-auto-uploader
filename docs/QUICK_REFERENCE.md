# Quick Reference Guide

**Quick API reference for all YouTube Auto Uploader modules.**

---

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
export CLIENT_ID=your_client_id
export CLIENT_SECRET=your_client_secret
export REFRESH_TOKEN_DOUGHVINCI=your_refresh_token
```

---

## Running the System

### GitHub Actions (One-Shot)
```bash
python3 main.py --github-actions
```

### Test Mode
```bash
python3 main.py --test
```

### Custom Configuration
```bash
python3 main.py \
  --times "09:00,14:00,20:00" \
  --topics "money,motivation,psychology" \
  --channel "main_channel"
```

---

## Module Quick Start

### Title Optimizer
```python
from modules.title_optimizer import optimize_title

title = optimize_title("How to Make Money", "money")
# → "5 Ways: Proven How to Make Money"
```

### Description Optimizer
```python
from modules.description_optimizer import optimize_description

desc = optimize_description("Learn passive income", "money", 45)
# → Includes timestamps, keywords, CTA, footer
```

### Tag Generator
```python
from modules.tag_generator import generate_tags

tags = generate_tags("Make Money Online", "money", script_text)
# → ['money', 'passive income', 'side hustle', ...]
```

### Thumbnail Generator
```python
from modules.thumbnail_generator import generate_thumbnail

path = generate_thumbnail("How to Make Money", "money", emoji="💰")
# → "uploads/thumbnail_money_xxxxx.png"
```

### Affiliate Link Generator
```python
from modules.affiliate_link_generator import generate_affiliate_links

links = generate_affiliate_links("Check out this book...", "money")
# → {'book': 'https://amazon.com/s?k=book&tag=xxx'}
```

### Trending Topic Discovery
```python
from modules.trending_topic_discovery import get_trending_topics

topics = get_trending_topics("personal finance", limit=5)
# → [{'topic': 'passive income', 'score': 0.95, ...}, ...]
```

### Frequency Scaler
```python
from modules.frequency_scaler import calculate_optimal_frequency

freq = calculate_optimal_frequency(
    {"avg_views": 5000, "avg_engagement": 0.08},
    current_frequency=3
)
# → 3 (or adjusted based on performance)
```

### Multi-Channel Support
```python
from modules.multi_channel_support import MultiChannelScheduler

scheduler = MultiChannelScheduler()
scheduler.add_channel("Main", "UCxxx", upload_times=["09:00"])
scheduler.add_channel("Backup", "UCyyy", upload_times=["14:00"])

status = scheduler.get_status()
```

---

## Testing

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_title_optimizer.py -v

# Run with coverage
pytest --cov=modules

# Run only fast tests
pytest -m "not slow"
```

---

## Environment Variables

### Core Configuration
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REFRESH_TOKEN_DOUGHVINCI=your_refresh_token
```

### Feature Flags
```env
ENABLE_THUMBNAILS=true
ENABLE_TITLE_OPTIMIZATION=true
ENABLE_DESCRIPTION_OPTIMIZATION=true
ENABLE_TAG_GENERATION=true
ENABLE_AFFILIATE_AMAZON=true
ENABLE_TRENDING_DISCOVERY=true
ENABLE_FREQUENCY_SCALING=true
```

### Feature Configuration
```env
AMAZON_ASSOCIATE_ID=your-associate-id
MAX_UPLOAD_FREQUENCY=5
MIN_UPLOAD_FREQUENCY=1
UPLOAD_TIMEOUT_SECONDS=3600
TITLE_MAX_LENGTH=60
DESCRIPTION_MAX_LENGTH=5000
MAX_TAGS=30
```

---

## Common Tasks

### Generate Complete Metadata
```python
from modules.title_optimizer import optimize_title
from modules.description_optimizer import optimize_description
from modules.tag_generator import generate_tags
from modules.thumbnail_generator import generate_thumbnail

title = optimize_title(base_title, topic="money")
description = optimize_description(base_desc, "money", 45)
tags = generate_tags(title, "money", script)
thumbnail = generate_thumbnail(title, "money")
```

### Find What to Upload Next
```python
from modules.trending_topic_discovery import get_recommended_topics
from modules.frequency_scaler import calculate_optimal_frequency

current_topics = ["passive income", "side hustle"]
recommendations = get_recommended_topics("money", current_topics, 3)

optimal_freq = calculate_optimal_frequency(channel_stats, current=3)
```

### Upload to Multiple Channels
```python
from modules.multi_channel_support import MultiChannelScheduler, batch_upload

scheduler = MultiChannelScheduler()
# Add channels...

videos = [
    {
        "path": "video1.mp4",
        "title": "Title",
        "description": "Desc",
        "tags": ["tag1"]
    }
]

results = batch_upload(scheduler, videos)
```

---

## File Locations

- **Modules:** `modules/*.py`
- **Tests:** `tests/test_*.py`
- **Logs:** `logs/`
- **Videos:** `uploads/`
- **Config:** `channel_config.json`
- **Documentation:** `docs/`
- **Architecture:** `architecture/`

---

## Return Value Quick Reference

| Function | Returns | Type |
|----------|---------|------|
| `optimize_title()` | Optimized title | str |
| `optimize_description()` | Full description | str |
| `generate_tags()` | Tag list | List[str] |
| `generate_thumbnail()` | File path | str |
| `generate_affiliate_links()` | URL dict | Dict[str, str] |
| `get_trending_topics()` | Topic list | List[Dict] |
| `calculate_optimal_frequency()` | Frequency | int |
| `get_frequency_recommendation()` | Recommendation | Dict |

---

## Troubleshooting

### Thumbnails not generating
```
Check: ENABLE_THUMBNAILS=true
Check: Pillow installed (pip install Pillow)
Check: write permissions on uploads/ folder
```

### Tags not generating
```
Check: ENABLE_TAG_GENERATION=true
Check: Script text is not empty
Check: Topic is valid
```

### Upload timeout
```
Check: UPLOAD_TIMEOUT_SECONDS (default 3600 = 1 hour)
Check: Internet connection
Check: Video file size (YouTube limit: 128 GB)
```

### Multi-channel issues
```
Check: channel_config.json exists
Check: YouTube client credentials for each channel
Check: Channel IDs are valid (UCxxx format)
```

---

## Performance Tips

1. **Enable only needed features** - Disable unused modules via env vars
2. **Optimize video generation** - Keep videos 30-60 seconds for speed
3. **Batch uploads** - Use `batch_upload()` for multiple channels
4. **Check logs** - All actions logged to `logs/` for debugging

---

**Last Updated:** June 2, 2026  
**Version:** 2.0.0
