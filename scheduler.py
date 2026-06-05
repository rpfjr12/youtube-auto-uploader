# scheduler.py
"""
Daily Scheduler for YouTube automation.

This module orchestrates the complete workflow:
1. Generate a script
2. Generate a video from the script
3. Generate metadata
4. Upload the video

Can handle multiple channels with configurable upload limits per day.
"""

import os
import schedule
import time
import random
import threading
from datetime import datetime
from pathlib import Path
from logger import log_line
from channel_manager import ChannelManager
from modules.human_timing import HumanTiming
from modules.trending_topic_discovery import get_recommended_topics
from script_generator import generate_script
from video_generator import generate_video, generate_simple_video
from metadata import generate_metadata_from_script
from uploader import upload_video

UPLOADS_FOLDER = "uploads"

class YouTubeScheduler:
    """
    Main scheduler for daily video generation and uploads.
    
    Usage:
        scheduler = YouTubeScheduler(
            upload_times=["09:00", "14:00", "20:00"],  # 3 videos per day
            topics=["money", "motivation", "psychology"]
        )
        scheduler.run()  # Blocks and runs forever
    """
    
    def __init__(self, upload_times=None, topics=None, channel_name=None):
        """
        Initialize scheduler.
        
        Args:
            upload_times: List of times to upload (e.g., ["09:00", "14:00"]).
                         If None, uploads ~3 times per day at random times.
            topics: List of topics to generate scripts from.
                   If None, uses default: ["money", "motivation", "psychology", "side-hustles"]
            channel_name: Name of channel to upload to. If None, uses default.
        """
        self.upload_times = upload_times or ["09:00", "14:00", "20:00"]
        self.topics = topics or ["money", "motivation", "psychology", "side-hustles"]
        self.channel_name = channel_name
        self.channel_mgr = ChannelManager()
        self.lock = threading.Lock()
        self.human_timing = HumanTiming()
        self.preferred_niche = self.channel_mgr.get_state(channel_name).cfg.get("preferred_niche") if self.channel_mgr.get_state(channel_name) else None

        # Ensure uploads folder exists
        Path(UPLOADS_FOLDER).mkdir(exist_ok=True)

        # Apply human-like jitter to scheduled times
        self.upload_times = [
            self.human_timing.randomize_schedule_time(upload_time)
            for upload_time in self.upload_times
        ]
        
        # Schedule jobs
        self._schedule_jobs()
        
        log_line("YouTubeScheduler initialized")
        log_line(f"Upload times: {self.upload_times}")
        log_line(f"Topics: {self.topics}")
        if self.preferred_niche:
            log_line(f"Preferred niche: {self.preferred_niche}")
    
    def _schedule_jobs(self):
        """Schedule upload jobs for each time."""
        schedule.clear()  # Clear any existing jobs
        for upload_time in self.upload_times:
            upload_time = self.human_timing.avoid_pattern(upload_time)
            schedule.every().day.at(upload_time).do(self._run_upload_job)
            log_line(f"Scheduled upload at {upload_time}")
    
    def _run_upload_job(self):
        """Single upload job: generate, create video, upload."""
        try:
            log_line("=" * 60)
            log_line("Starting upload job")
            
            # Check if we can upload today
            state = self.channel_mgr.get_state(self.channel_name)
            remaining = state.uploads_remaining() if state else 3
            if remaining <= 0:
                log_line(f"Upload limit reached for today. Remaining: {remaining}")
                return
            
            # Step 1: Delay upload slightly to feel human-like and check sleep windows
            if self.human_timing.in_sleep_window():
                delay_sec = self.human_timing.seconds_until_window_end()
                log_line(f"In sleep window; delaying upload by {delay_sec} seconds")
                time.sleep(delay_sec)
            else:
                delay_sec = self.human_timing.random_upload_delay()
                if delay_sec > 0:
                    log_line(f"Applying upload jitter delay: {delay_sec} seconds")
                    time.sleep(delay_sec)

            # Step 1: Generate script
            log_line("Step 1: Generating script...")
            topic = random.choice(self.topics)
            if self.preferred_niche:
                recommended = get_recommended_topics(
                    niche=self.preferred_niche,
                    current_topics=self.topics,
                    limit=8
                )
                if recommended:
                    topic = random.choice(recommended)
            script_dict = generate_script(topic=topic, duration_seconds=45)
            log_line(f"Script generated: {script_dict['topic']}")
            
            # Step 2: Generate video
            log_line("Step 2: Generating video...")
            video_path = None
            try:
                video_path = generate_video(
                    script_dict['script_text'],
                    script_dict['title'],
                    topic=topic,
                    duration_seconds=45
                )
                log_line(f"Video generated: {video_path}")
            except Exception as e:
                log_line(f"MoviePy failed, trying fallback: {e}")
                try:
                    video_path = generate_simple_video(
                        script_dict['script_text'],
                        script_dict['title'],
                        topic=topic,
                        duration_seconds=45
                    )
                    log_line(f"Fallback video generated: {video_path}")
                except Exception as e2:
                    log_line(f"Both video generators failed: {e2}")
                    raise
            
            # Step 3: Generate metadata
            log_line("Step 3: Generating metadata...")
            title, description, tags, hashtags = generate_metadata_from_script(
                script_dict,
                channel_name=self.channel_name or "MyChannel"
            )
            description += f"\n\n{hashtags}"
            log_line(f"Metadata generated: {title[:50]}...")
            
            # Step 4: Upload video
            log_line("Step 4: Uploading video...")
            youtube = self.channel_mgr.get_youtube_for_channel(self.channel_name)
            video_id = upload_video(
                youtube,
                video_path,
                title,
                description,
                tags,
                channel_name=self.channel_name or "default"
            )
            log_line(f"Video uploaded successfully! ID: {video_id}")
            
            # Record the upload
            self.channel_mgr.record_upload(self.channel_name)
            state = self.channel_mgr.get_state(self.channel_name)
            remaining = state.uploads_remaining() if state else 0
            log_line(f"Uploads remaining today: {remaining}")
            log_line("=" * 60)
            
        except Exception as e:
            log_line(f"ERROR in upload job: {e}")
            import traceback
            log_line(traceback.format_exc())
    
    def run_once(self):
        """
        Run upload job once (for testing).
        Useful for manual dry-runs without scheduling.
        """
        self._run_upload_job()
    
    def run(self, once_only=False):
        """
        Start the scheduler loop.
        
        Args:
            once_only: If True, run once and exit (for GitHub Actions).
                      If False, run forever in daemon mode.
        """
        if once_only:
            log_line("Running single upload job (GitHub Actions mode - will exit after)")
            self._run_upload_job()
            log_line("Upload job completed, exiting cleanly")
            return
        
        log_line("Starting scheduler loop. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            log_line("Scheduler stopped by user")
    
    def get_status(self):
        """Return current status."""
        state = self.channel_mgr.get_state(self.channel_name)
        if state:
            state.reset_daily_if_needed()
            return {
                "channel": self.channel_name or "default",
                "uploads_today": state.uploads_today,
                "max_per_day": state.max_uploads_per_day,
                "remaining": state.uploads_remaining(),
                "scheduled_times": self.upload_times
            }
        return {}


# Legacy functions for backward compatibility
def file_hash(path):
    """Compute SHA256 hash of a file."""
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    # Test: run once
    print("Testing scheduler (single run)...")
    scheduler = YouTubeScheduler()
    scheduler.run_once()

