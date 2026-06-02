#!/usr/bin/env python3
"""
YouTube Auto Uploader - Main Controller

This is the main entry point for the YouTube automation system.

Usage:
    # Run the automated scheduler
    python3 main.py

    # Run a single test upload
    python3 main.py --test

    # Run with custom upload times
    python3 main.py --times "08:00,14:00,20:00" --topics "money,psychology"
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from logger import log_line
from scheduler import YouTubeScheduler

# Load .env automatically
load_dotenv()


def get_youtube(channel_name=None):
    """
    Build and return an authenticated YouTube client.
    
    Args:
        channel_name: Channel name (uses default if None)
    
    Returns:
        Authenticated youtube resource object
    """
    from channel_manager import ChannelManager
    
    mgr = ChannelManager()
    return mgr.get_youtube_for_channel(channel_name)


def verify_credentials():
    """Verify that credentials are properly loaded from .env"""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN_DOUGHVINCI")
    
    if not all([client_id, client_secret, refresh_token]):
        log_line("ERROR: Missing credentials in .env file")
        return False
    
    log_line("✓ Credentials loaded from .env")
    return True


def test_youtube_connection():
    """Test YouTube API connection"""
    try:
        youtube = get_youtube()
        resp = youtube.channels().list(part='id,snippet', mine=True).execute()
        if resp.get('items'):
            channel_id = resp['items'][0]['id']
            channel_title = resp['items'][0]['snippet']['title']
            log_line(f"✓ YouTube connection successful")
            log_line(f"  Channel: {channel_title} ({channel_id})")
            return True
        else:
            log_line("ERROR: No channels found")
            return False
    except Exception as e:
        log_line(f"ERROR: YouTube connection failed: {e}")
        return False


def test_uploads_folder():
    """Ensure uploads folder exists"""
    from pathlib import Path
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    log_line(f"✓ Uploads folder ready: {uploads_dir.absolute()}")
    return True


def run_system_check():
    """Run full system check before starting"""
    log_line("=" * 60)
    log_line("SYSTEM CHECK")
    log_line("=" * 60)
    
    checks = [
        ("Credentials", verify_credentials),
        ("YouTube API", test_youtube_connection),
        ("Uploads Folder", test_uploads_folder),
    ]
    
    results = []
    for check_name, check_func in checks:
        log_line(f"Checking {check_name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            log_line(f"  ERROR: {e}")
            results.append(False)
    
    log_line("=" * 60)
    if all(results):
        log_line("✓ ALL CHECKS PASSED - System is ready")
        log_line("=" * 60)
        return True
    else:
        log_line("✗ SOME CHECKS FAILED - Please fix before running")
        log_line("=" * 60)
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="YouTube Auto Uploader - Automated video generation and uploading"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a single test upload (no scheduling)"
    )
    parser.add_argument(
        "--github-actions",
        action="store_true",
        help="Run in GitHub Actions mode: one upload then exit cleanly"
    )
    parser.add_argument(
        "--times",
        type=str,
        default="09:00,14:00,20:00",
        help="Upload times as comma-separated list (e.g., '08:00,14:00,20:00')"
    )
    parser.add_argument(
        "--topics",
        type=str,
        default="money,motivation,psychology,side-hustles",
        help="Topics for script generation (comma-separated)"
    )
    parser.add_argument(
        "--channel",
        type=str,
        default=None,
        help="Channel name (uses default if not specified)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run system check only"
    )
    
    args = parser.parse_args()
    
    # Run system check
    if not run_system_check():
        sys.exit(1)
    
    if args.check:
        log_line("System check completed successfully")
        return
    
    # Parse upload times and topics
    upload_times = [t.strip() for t in args.times.split(",")]
    topics = [t.strip() for t in args.topics.split(",")]
    
    log_line(f"Configuration:")
    log_line(f"  Upload times: {upload_times}")
    log_line(f"  Topics: {topics}")
    log_line(f"  Channel: {args.channel or 'default'}")
    
    # Create scheduler
    scheduler = YouTubeScheduler(
        upload_times=upload_times,
        topics=topics,
        channel_name=args.channel
    )
    
    if args.test or args.github_actions:
        log_line("Running single upload job...")
        try:
            scheduler.run_once()
            log_line("✓ Upload completed successfully")
            sys.exit(0)
        except Exception as e:
            log_line(f"✗ Upload failed: {e}")
            sys.exit(1)
    else:
        log_line("Starting automated scheduler...")
        log_line("(Press Ctrl+C to stop)")
        try:
            scheduler.run(once_only=False)
        except KeyboardInterrupt:
            log_line("Scheduler stopped")
            sys.exit(0)
        except Exception as e:
            log_line(f"ERROR: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

