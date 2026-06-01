# YouTube Auto Uploader - System Documentation

## Overview

This is a complete YouTube automation system that generates scripts, creates videos, generates metadata, and uploads them to YouTube automatically - all without manual work.

**Current Status: PRODUCTION READY** ✓

## System Architecture

### Components

1. **script_generator.py** - Generates short-form video scripts
   - Supports topics: money, motivation, psychology, side-hustles
   - Creates engaging hooks, bodies, and CTAs
   - Returns structured data: title, description, tags, script text

2. **video_generator.py** - Generates 1080x1920 (vertical) videos
   - Creates text-based short-form videos
   - Auto-saves to `/uploads` folder
   - Supports both MoviePy (primary) and PIL+ffmpeg (fallback)

3. **metadata.py** - Auto-generates YouTube metadata
   - Titles with A/B testing variants
   - Descriptions with CTAs
   - SEO-optimized tags
   - Hashtags for trending

4. **scheduler.py** - Orchestrates the complete workflow
   - Generates scripts daily
   - Creates videos automatically
   - Uploads to YouTube on schedule
   - Tracks upload limits per day

5. **channel_manager.py** - Multi-channel support
   - Currently supports 1 channel (easily expandable)
   - Loads credentials from .env
   - Manages upload limits per channel

6. **uploader.py** - Uploads videos to YouTube
   - Uses YouTube API v3
   - Supports resumable uploads
   - Handles metadata, tags, privacy settings

7. **main.py** - Main controller
   - Entry point for the system
   - System checks and verification
   - CLI arguments for custom configuration

## Multi-Channel Architecture

### Current Setup (Single Channel)

```
.env:
  CLIENT_ID=...
  CLIENT_SECRET=...
  REFRESH_TOKEN_DOUGHVINCI=...
```

The system uses `ChannelManager()` which defaults to the single channel.

### Expanding to Multiple Channels

To add Channel 2:

```
.env:
  CLIENT_ID=...
  CLIENT_SECRET=...
  REFRESH_TOKEN_DOUGHVINCI=...
  REFRESH_TOKEN_CHANNEL2=...
```

Then configure in your code:

```python
channels_config = [
    {"name": "doughvinci", "refresh_token_env": "REFRESH_TOKEN_DOUGHVINCI"},
    {"name": "channel2", "refresh_token_env": "REFRESH_TOKEN_CHANNEL2"}
]
mgr = ChannelManager(channels_config=channels_config)
```

### Adding Channel 3, 4, 5+

Just repeat the pattern:
1. Add `REFRESH_TOKEN_<NAME>` to .env
2. Add to channels_config list
3. Restart scheduler

**The system scales to unlimited channels!**

## Daily Workflow

1. **09:00** - Scheduler triggers
   - Generates script (random topic)
   - Creates video from script
   - Generates metadata
   - Uploads to YouTube

2. **14:00** - Second upload

3. **20:00** - Third upload

Maximum 3 uploads per day (configurable per channel).

## Usage

### System Check Only

```bash
python3 main.py --check
```

### Single Test Upload

```bash
python3 main.py --test
```

### Run with Custom Configuration

```bash
python3 main.py \
  --times "08:00,14:00,20:00" \
  --topics "money,psychology,motivation" \
  --channel doughvinci
```

### Run Automated Scheduler

```bash
python3 main.py
```

(Runs forever, checking schedule every minute. Press Ctrl+C to stop)

## Configuration

### Environment Variables (.env)

```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REFRESH_TOKEN_DOUGHVINCI=your_refresh_token
```

### Upload Times

Edit in scheduler initialization or via CLI:

```bash
--times "08:00,14:00,20:00"
```

### Topics

Available topics (extensible in script_generator.py):

- `money` - Finance tips, investing, wealth
- `motivation` - Success, mindset, habits
- `psychology` - Human behavior, cognitive biases
- `side-hustles` - Additional income streams

Add custom via CLI:

```bash
--topics "money,psychology,motivation,side-hustles"
```

## API Rate Limits

YouTube API quota: 10,000 units/day

- `videos.insert`: 1600 units per upload
- Safe max: 4-5 uploads/day
- Currently configured: 3/day (safe)

## Folders

- `/uploads` - Generated videos waiting for upload or uploaded
- `/logs` - Upload logs and system events
- `/` - Configuration and module files

## File Structure

```
youtube-auto-uploader/
├── main.py                 # Main entry point
├── scheduler.py            # Daily scheduler
├── channel_manager.py      # Multi-channel support
├── script_generator.py     # Script generation
├── video_generator.py      # Video creation
├── metadata.py            # Metadata generation
├── uploader.py            # YouTube upload
├── logger.py              # Logging
├── analytics.py           # Analytics tracking
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # Credentials
├── uploads/               # Generated videos
├── logs/                  # System logs
└── README.md              # This file
```

## Verification Checklist

✓ All modules import correctly
✓ .env credentials loaded
✓ YouTube API authentication works
✓ Script generator produces valid scripts
✓ Metadata generator works
✓ Video generator set up
✓ Scheduler initialized and ready
✓ Multi-channel architecture ready
✓ Upload limits configured
✓ Logs and uploads folders created

## Troubleshooting

### YouTube API Error
- Verify CLIENT_ID, CLIENT_SECRET in .env
- Check REFRESH_TOKEN_DOUGHVINCI is valid
- Refresh token expires after 6+ months of inactivity

### Video Generation Fails
- MoviePy requires ffmpeg: `sudo apt-get install ffmpeg`
- Fallback uses PIL + ffmpeg
- Check disk space in uploads/

### Permission Denied
- Ensure YouTube OAuth consent screen is set up
- Grant "YouTube Data API v3" permissions
- Refresh tokens with latest OAuth flow

## Expanding the System

### Add New Topic

Edit `script_generator.py`:

```python
TOPICS = {
    "your_topic": {
        "hooks": [...],
        "bodies": [...],
        "ctas": [...]
    },
    # existing topics...
}
```

### Add New Channel

1. Get refresh token for new channel (OAuth flow)
2. Add to .env: `REFRESH_TOKEN_CHANNEL2=...`
3. Update scheduler to use multi-channel config

### Customize Video Style

Edit `video_generator.py`:
- Change colors: `colors = [(R, G, B), ...]`
- Change font size: `fontsize=48`
- Change duration: `duration_seconds=45`

## Next Steps

1. Run system check: `python3 main.py --check`
2. Test single upload: `python3 main.py --test`
3. Review generated files in `/uploads` and `/logs`
4. Schedule for production: `python3 main.py` in screen/tmux/docker
5. Add more channels as needed

## Support

All modules are self-documenting with docstrings and comments. Check individual files for implementation details.

---

**SYSTEM: READY FOR PRODUCTION** ✓
