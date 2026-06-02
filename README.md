# YouTube Auto Uploader

**Fast, modular YouTube automation system optimized for GitHub Actions.**

Automatically generate, optimize, and upload YouTube videos with zero human intervention. Designed for speed (<6 hours per video cycle) and compatibility with GitHub Actions' 6-hour runner limit.

---

## ⚡ Key Features

### Core Automation
- ✅ **One-shot execution mode** - Uploads single video then exits (perfect for GitHub Actions)
- ✅ **Fast video generation** - Generates 45-second videos in 2-5 minutes
- ✅ **Automated uploads** - Handles YouTube API authentication and uploads
- ✅ **Timeout protection** - 1-hour max per upload with error recovery
- ✅ **Clean exit handling** - No infinite loops or daemon processes

### 🆕 Advanced Features (8 New Modules)

#### 1. **Affiliate Link Generator** (`modules/affiliate_link_generator.py`)
- Automatically extracts product mentions from video scripts
- Generates affiliate links for Amazon, teaching platforms, and other networks
- Formats links for video descriptions
- Tracks affiliate performance metrics

```python
from modules.affiliate_link_generator import generate_affiliate_links
links = generate_affiliate_links("Check out this amazing book...", "money")
```

#### 2. **Thumbnail Generator** (`modules/thumbnail_generator.py`)
- Creates eye-catching thumbnails automatically
- Topic-based color selection
- Emoji integration for visual appeal
- Customizable text size and border styling

```python
from modules.thumbnail_generator import generate_thumbnail
path = generate_thumbnail("How to Make Money", "money", emoji="💰")
```

#### 3. **Title Optimizer** (`modules/title_optimizer.py`)
- SEO optimization with power words
- Number hooks for increased CTR
- Length validation
- A/B testing variant generation

```python
from modules.title_optimizer import optimize_title
optimized = optimize_title("How to Make Money", "money")
# Output: "5 Ways: Proven How to Make Money"
```

#### 4. **Description Optimizer** (`modules/description_optimizer.py`)
- Auto-generates timestamps for video chapters
- Keyword insertion for SEO
- CTA injection
- Affiliate link integration
- Related video suggestions

```python
from modules.description_optimizer import optimize_description
desc = optimize_description("Learn about passive income", "money", 45)
```

#### 5. **Tag Generator** (`modules/tag_generator.py`)
- Intelligent tag creation from title and script
- Topic-specific tag databases
- Trending tag inclusion
- YouTube compliance validation (max 30 tags)

```python
from modules.tag_generator import generate_tags
tags = generate_tags("How to Make Money", "money", script_text)
```

#### 6. **Trending Topic Discovery** (`modules/trending_topic_discovery.py`)
- Discovers trending topics in your niche
- Seasonal content suggestions
- Topic relevance scoring
- Channel-specific recommendations

```python
from modules.trending_topic_discovery import get_trending_topics
topics = get_trending_topics("personal finance", limit=5)
```

#### 7. **Frequency Scaler** (`modules/frequency_scaler.py`)
- Auto-adjusts upload frequency based on engagement
- Burnout risk scoring
- Sustainable growth optimization
- Performance-based recommendations

```python
from modules.frequency_scaler import calculate_optimal_frequency
freq = calculate_optimal_frequency(channel_stats, current=3)
```

#### 8. **Multi-Channel Support** (`modules/multi_channel_support.py`)
- Manage multiple YouTube channels from one config
- Per-channel upload schedules
- Synced uploads to multiple channels
- Persistent configuration management

```python
from modules.multi_channel_support import MultiChannelScheduler
scheduler = MultiChannelScheduler()
scheduler.add_channel("Main", "UCxxxxx", upload_times=["09:00"])
```

---

## 📋 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/youtube-auto-uploader.git
cd youtube-auto-uploader

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your YouTube API credentials
```

### Basic Usage

#### Single Upload (GitHub Actions Mode)
```bash
python3 main.py --github-actions
```

#### Test Mode
```bash
python3 main.py --test
```

#### Daemon Mode (continuous scheduling)
```bash
python3 main.py --times "09:00,14:00,20:00" --topics "money,motivation"
```

---

## 🔧 Configuration

### Environment Variables

```env
# YouTube API Credentials
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REFRESH_TOKEN_DOUGHVINCI=your_refresh_token

# Feature Flags
ENABLE_THUMBNAILS=true
ENABLE_TITLE_OPTIMIZATION=true
ENABLE_DESCRIPTION_OPTIMIZATION=true
ENABLE_TAG_GENERATION=true
ENABLE_AFFILIATE_AMAZON=true
ENABLE_TRENDING_DISCOVERY=true
ENABLE_FREQUENCY_SCALING=true

# Affiliate Marketing
AMAZON_ASSOCIATE_ID=your_associate_id

# Upload Limits
MAX_UPLOAD_FREQUENCY=5
MIN_UPLOAD_FREQUENCY=1
UPLOAD_TIMEOUT_SECONDS=3600
```

---

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_title_optimizer.py -v

# Run only fast tests (skip slow tests)
pytest -m "not slow"

# Run with coverage
pytest --cov=modules --cov-report=html
```

### Test Structure
- `tests/conftest.py` - Shared fixtures and configuration
- `tests/test_*.py` - Unit tests for each module
- Full coverage of core functionality, edge cases, and error handling

---

## 📁 Project Structure

```
youtube-auto-uploader/
├── main.py                           # Entry point
├── scheduler.py                      # Optimized scheduler (one-shot mode)
├── uploader.py                       # Upload with timeout protection
├── video_generator.py                # 2-5 min video generation
├── script_generator.py               # Script generation
├── metadata.py                       # Metadata generation
├── config.py                         # Configuration
├── logger.py                         # Logging setup
│
├── modules/                          # 🆕 NEW: Modular features
│   ├── __init__.py
│   ├── affiliate_link_generator.py   # Affiliate link management
│   ├── thumbnail_generator.py        # Auto thumbnail creation
│   ├── title_optimizer.py            # Title SEO optimization
│   ├── description_optimizer.py      # Description generation
│   ├── tag_generator.py              # Smart tag creation
│   ├── trending_topic_discovery.py   # Trending content discovery
│   ├── frequency_scaler.py           # Posting frequency optimization
│   └── multi_channel_support.py      # Multi-channel management
│
├── tests/                            # 🆕 NEW: Complete test suite
│   ├── conftest.py
│   ├── test_affiliate_link_generator.py
│   ├── test_thumbnail_generator.py
│   ├── test_title_optimizer.py
│   ├── test_description_optimizer.py
│   ├── test_tag_generator.py
│   ├── test_trending_topic_discovery.py
│   ├── test_frequency_scaler.py
│   └── test_multi_channel_support.py
│
├── docs/                             # 🆕 NEW: Documentation
│   ├── FEATURES.md                   # Detailed feature documentation
│   ├── MODULES.md                    # Module API reference
│   ├── ARCHITECTURE.md               # System architecture
│   └── QUICK_REFERENCE.md            # Quick API reference
│
├── architecture/                     # 🆕 NEW: Architecture diagrams
│   ├── system_architecture.mmd       # High-level architecture
│   ├── upload_pipeline.mmd           # Upload process flow
│   ├── module_dependencies.mmd       # Module relationships
│   └── multi_channel_flow.mmd        # Multi-channel workflow
│
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## 🎯 Optimization for GitHub Actions

### Single Run Under 6 Hours

The system is optimized to run a complete video cycle in under 6 hours:

1. **Video Generation** - 2-5 minutes
2. **Upload** - 5-10 minutes (depends on file size)
3. **Metadata Generation** - 10 seconds
4. **System Checks** - 30 seconds
5. **Total** - ~10-20 minutes per video

### Key Optimizations

- ✅ No infinite loops - Uses `--github-actions` flag for single run
- ✅ Timeout protection - 1 hour max per upload
- ✅ Clean exit - Properly exits after completion
- ✅ Error handling - Graceful failure with logging
- ✅ Fast video generation - Optimized for 45-second videos

### GitHub Actions Workflow

```yaml
name: Upload Video
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  workflow_dispatch:

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Upload video
        env:
          CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
          REFRESH_TOKEN_DOUGHVINCI: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
        run: python3 main.py --github-actions --topics "money,motivation"
```

---

## 📚 Module Documentation

### Using the Modules

All modules are designed to be independent and can be imported directly:

```python
# Example: Combining multiple modules
from modules.title_optimizer import optimize_title
from modules.tag_generator import generate_tags
from modules.description_optimizer import optimize_description
from modules.thumbnail_generator import generate_thumbnail

# Generate optimized metadata
title = optimize_title(base_title, topic="money")
tags = generate_tags(title, "money", script_text)
description = optimize_description(base_desc, "money", video_duration=45)
thumbnail = generate_thumbnail(title, "money")
```

### Configuration

Each module can be enabled/disabled via environment variables:

```env
ENABLE_THUMBNAILS=true
ENABLE_TITLE_OPTIMIZATION=true
ENABLE_DESCRIPTION_OPTIMIZATION=true
ENABLE_TAG_GENERATION=true
ENABLE_AFFILIATE_AMAZON=true
ENABLE_TRENDING_DISCOVERY=true
ENABLE_FREQUENCY_SCALING=true
```

---

## 🔍 Logging & Monitoring

All operations are logged to `logs/` directory:

```python
from logger import log_line

log_line("Video upload started")
log_line("✓ Upload completed: VIDEO_ID")
log_line("ERROR: Upload failed - timeout")
```

---

## ⚠️ Important Notes

- **No Daemon Mode in GitHub Actions** - Use `--github-actions` flag for single run
- **Timeout Protection** - 1-hour max per upload to prevent hanging
- **Feature Flags** - All new features are configurable and can be disabled
- **Backward Compatibility** - Existing functionality is preserved; new modules are additive
- **Test Coverage** - Run `pytest` before deployment

---

## 🚀 Roadmap

- [ ] Integration with trending APIs (Google Trends, YouTube Trends)
- [ ] Advanced analytics dashboard
- [ ] Automatic video editing with scene transitions
- [ ] AI-powered script generation improvements
- [ ] Webhook notifications for upload status
- [ ] Multi-provider affiliate support

---

## 📞 Support

For issues, feature requests, or questions, please refer to:
- `docs/FEATURES.md` - Detailed feature documentation
- `docs/MODULES.md` - Module API reference
- `architecture/` - System architecture diagrams

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- YouTube API for automation capabilities
- MoviePy for video generation
- Pillow for image processing

---

**Last Updated:** June 2, 2026  
**Version:** 2.0.0  
**Status:** Production Ready ✅
