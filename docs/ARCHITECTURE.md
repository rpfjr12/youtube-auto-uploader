# Architecture & Design

Complete architecture documentation for the YouTube Auto Uploader system.

---

## System Design Principles

### 1. **Modularity**
- Each feature is an independent module
- Modules can be enabled/disabled via configuration
- No hard dependencies between optimization modules

### 2. **Speed**
- Optimized for GitHub Actions' 6-hour runner limit
- Single video per run completes in 10-25 minutes
- One-shot execution mode, not daemon-based

### 3. **Reliability**
- Timeout protection on all long-running operations
- Graceful error handling and recovery
- Comprehensive logging for debugging

### 4. **Extensibility**
- Easy to add new modules
- Standard module interface for all optimizers
- Configuration-driven feature flags

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ENTRY POINT                             │
│                       main.py                                │
│                                                               │
│  • Parse arguments (--github-actions, --test, etc.)        │
│  • System check (credentials, API, folders)                │
│  • Create scheduler                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    SCHEDULER                                 │
│                    scheduler.py                              │
│                                                               │
│  • Orchestrates complete workflow                           │
│  • One-shot mode (--github-actions) or daemon mode         │
│  • Manages upload job execution                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
            ┌──────────┼──────────┬──────────┐
            ▼          ▼          ▼          ▼
   ┌──────────────┐ ┌──────────────────┐ ┌─────────────┐
   │ GENERATORS   │ │ OPTIMIZERS       │ │ DISCOVERY   │
   ├──────────────┤ ├──────────────────┤ ├─────────────┤
   │ • Script     │ │ • Title          │ │ • Trending  │
   │ • Video      │ │ • Description    │ │ • Frequency │
   │ • Metadata   │ │ • Tags           │ │ • Affiliate │
   │              │ │ • Thumbnail      │ │             │
   └──────────────┘ └──────────────────┘ └─────────────┘
            │          │          │         │
            └──────────┼──────────┴─────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     UPLOADER                                 │
│                     uploader.py                              │
│                                                               │
│  • YouTube API authentication                               │
│  • Upload with timeout protection (1 hour max)             │
│  • Error recovery and retry logic                          │
│  • Logging and status tracking                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
        ┌───────┐  ┌───────┐  ┌──────────┐
        │ LOGS  │  │UPLOADS│  │METADATA  │
        └───────┘  └───────┘  └──────────┘
```

---

## Data Flow

### Single Video Workflow

```
Start
  │
  ├─→ System Check (30s)
  │    ├─→ Verify credentials
  │    ├─→ Test YouTube API
  │    └─→ Check folders
  │
  ├─→ Generate Script (10-15s)
  │    └─→ script_generator.py
  │
  ├─→ Generate Video (2-5 min)
  │    ├─→ MoviePy or fallback
  │    └─→ Writes to uploads/
  │
  ├─→ Generate Metadata (10s)
  │    ├─→ Title Optimizer
  │    ├─→ Description Optimizer
  │    ├─→ Tag Generator
  │    └─→ Thumbnail Generator
  │
  ├─→ Upload to YouTube (5-10 min)
  │    ├─→ MediaFileUpload
  │    ├─→ Chunk by chunk
  │    ├─→ Timeout protection (3600s)
  │    └─→ Status tracking
  │
  └─→ Record Upload & Exit (5s)
     ├─→ Log video ID
     ├─→ Update channel state
     └─→ Clean exit (exit code 0)

Total: ~10-25 minutes (well under 6-hour limit)
```

---

## Module Architecture

### Independent Modules (No Hard Dependencies)

```
title_optimizer.py
  ├─→ analyze_title_quality()
  ├─→ optimize_title()
  ├─→ generate_title_variants()
  └─→ Power words, numbers, length validation

description_optimizer.py
  ├─→ optimize_description()
  ├─→ add_affiliate_links()
  ├─→ add_related_videos()
  └─→ Timestamps, keywords, CTAs

tag_generator.py
  ├─→ generate_tags()
  ├─→ categorize_tags()
  ├─→ validate_tags()
  └─→ Keyword extraction, compliance

thumbnail_generator.py
  ├─→ generate_thumbnail()
  ├─→ get_emoji_for_topic()
  └─→ PIL-based image generation

affiliate_link_generator.py
  ├─→ generate_affiliate_links()
  ├─→ extract_product_mentions()
  └─→ Supports multiple networks

trending_topic_discovery.py
  ├─→ get_trending_topics()
  ├─→ get_seasonal_topics()
  ├─→ get_recommended_topics()
  └─→ Topic database + relevance scoring

frequency_scaler.py
  ├─→ calculate_optimal_frequency()
  ├─→ get_burnout_risk_score()
  ├─→ get_frequency_recommendation()
  └─→ Performance-based recommendations

multi_channel_support.py
  ├─→ MultiChannelScheduler
  ├─→ ChannelConfig
  ├─→ sync_upload_across_channels()
  └─→ Configuration persistence
```

---

## Configuration System

### Feature Flags (Environment Variables)

```
Enabled → Feature runs automatically
Disabled → Feature skipped during execution
Falls back to defaults → No error
```

### Configuration Hierarchy

```
1. Environment Variables (highest priority)
2. Config File (channel_config.json)
3. Module Defaults (hardcoded fallbacks)
```

### Example

```python
# User sets
export ENABLE_TITLES_OPTIMIZATION=true

# System loads
from modules.title_optimizer import TitleConfig
config = TitleConfig()  # Reads env var

# Uses or skips
if config.enable_optimization:
    title = optimize_title(...)
else:
    title = base_title  # Skip optimization
```

---

## Multi-Channel Architecture

### Per-Channel Configuration

```json
{
  "channels": [
    {
      "name": "Main Channel",
      "channel_id": "UCmain123",
      "upload_times": ["09:00", "14:00", "20:00"],
      "max_per_day": 3,
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

### Multi-Channel Workflow

```
MultiChannelScheduler
  │
  ├─→ Load channel_config.json
  │
  ├─→ Get Active Channels
  │   ├─→ Main Channel (enabled)
  │   └─→ Backup Channel (enabled)
  │
  ├─→ For Each Active Channel:
  │   ├─→ Generate video (if needed)
  │   ├─→ Optimize metadata (per-channel)
  │   └─→ Upload to channel
  │
  └─→ Update Config & Log Results
```

---

## Testing Architecture

### Test Structure

```
tests/
├── conftest.py                    # Shared fixtures
├── test_affiliate_link_generator.py  # Affiliate tests
├── test_description_optimizer.py  # Description tests
├── test_frequency_scaler.py       # Frequency tests
├── test_tag_generator.py          # Tag tests
├── test_thumbnail_generator.py    # Thumbnail tests
├── test_title_optimizer.py        # Title tests
└── test_trending_topic_discovery.py  # Trending tests
```

### Test Coverage Areas

1. **Unit Tests** - Individual function behavior
2. **Integration Tests** - Module interactions
3. **Edge Cases** - Boundary conditions
4. **Error Handling** - Exception scenarios

### Running Tests

```bash
pytest                           # All tests
pytest -m "not slow"            # Fast tests only
pytest tests/test_title_optimizer.py  # Specific module
pytest --cov=modules            # With coverage
```

---

## Error Handling

### Timeout Protection

```python
# uploads.py - Upload protection
UPLOAD_TIMEOUT_SECONDS = 3600  # 1 hour

while response is None:
    elapsed = time.time() - start_time
    if elapsed > UPLOAD_TIMEOUT_SECONDS:
        raise TimeoutError(f"Upload exceeded {UPLOAD_TIMEOUT_SECONDS}s")
    status, response = request.next_chunk()
```

### Graceful Degradation

```python
# scheduler.py - Fallback video generation
try:
    video_path = generate_video(...)
except Exception as e:
    try:
        video_path = generate_simple_video(...)  # Fallback
    except Exception as e2:
        log_line(f"ERROR: Both generators failed")
        raise
```

### Feature Flag Safety

```python
# All modules check enable flag before running
if not config.enable_feature:
    logger.debug("Feature disabled")
    return default_value
```

---

## Performance Optimization

### Video Generation (2-5 minutes)
- MoviePy with optimized settings
- 1080x1920 vertical format
- 45-second duration
- 24 FPS encoding

### Upload Optimization (5-10 minutes)
- Resumable upload with chunking
- Adaptive chunk size
- Retry logic for network errors
- Progress tracking

### Metadata Generation (<1 minute)
- Parallel keyword extraction
- Efficient regex-based parsing
- Minimal API calls

### System Efficiency
- No infinite loops
- Clean exit after completion
- Proper resource cleanup
- Minimal memory footprint

---

## Security Considerations

### Credentials
- Stored in `.env` file (not committed)
- Loaded via `python-dotenv`
- Never logged or exposed

### API Rate Limiting
- YouTube API quota awareness
- Proper error handling for quota exceeded
- Exponential backoff for retries

### File Permissions
- Temporary files in system temp directory
- Output files in designated folders
- Proper cleanup on exit

---

## Deployment Strategy

### GitHub Actions
```yaml
- Scheduled runs (cron job)
- Environment variables from secrets
- Single run execution (--github-actions)
- Clean failure handling
```

### Local Development
```bash
python3 main.py --test              # Single test run
python3 main.py                     # Daemon mode (manual)
pytest                              # Run tests
```

### Production Environment
```
Run daily via cron or CI/CD
Secrets in environment
Logs persisted to cloud
Monitoring and alerts configured
```

---

## Future Architecture Improvements

- [ ] **API Integration** - Direct trend APIs instead of database
- [ ] **Analytics Dashboard** - Real-time performance tracking
- [ ] **Advanced Editing** - Scene transitions and effects
- [ ] **Webhook Notifications** - Status updates via webhooks
- [ ] **Distributed Processing** - Process multiple videos in parallel
- [ ] **Database Backend** - SQLite for persistent analytics

---

**Last Updated:** June 2, 2026  
**Version:** 2.0.0
