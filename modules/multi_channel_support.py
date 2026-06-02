"""
Multi-Channel Support Module

Enhanced support for managing and uploading to multiple YouTube channels.
Handles channel switching, configuration per channel, and synchronized uploads.

Usage:
    from modules.multi_channel_support import ChannelScheduler
    
    scheduler = ChannelScheduler()
    scheduler.add_channel("main_channel", upload_times=["09:00"])
    scheduler.add_channel("backup_channel", upload_times=["14:00"])
    scheduler.run()
"""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ChannelConfig:
    """Configuration for a single YouTube channel."""
    
    def __init__(
        self,
        name: str,
        channel_id: str,
        upload_times: List[str] = None,
        max_per_day: int = 3,
        topics: List[str] = None,
        enabled: bool = True
    ):
        """
        Initialize channel configuration.
        
        Args:
            name: Channel name
            channel_id: YouTube channel ID
            upload_times: List of upload times (e.g., ["09:00", "14:00"])
            max_per_day: Max uploads per day
            topics: Topics for this channel
            enabled: Whether channel is enabled
        """
        self.name = name
        self.channel_id = channel_id
        self.upload_times = upload_times or ["09:00", "14:00", "20:00"]
        self.max_per_day = max_per_day
        self.topics = topics or ["money", "motivation", "psychology"]
        self.enabled = enabled
        self.created_at = datetime.now()


class MultiChannelScheduler:
    """Manage uploads to multiple channels."""
    
    def __init__(self, config_file: str = "channel_config.json"):
        """
        Initialize multi-channel scheduler.
        
        Args:
            config_file: Path to channel configuration file
        """
        self.channels: Dict[str, ChannelConfig] = {}
        self.config_file = config_file
        self.stats = {
            "total_uploads": 0,
            "total_channels": 0,
            "last_upload": None,
        }
        
        logger.info("Multi-channel scheduler initialized")
        self._load_config()
    
    def add_channel(
        self,
        name: str,
        channel_id: str,
        upload_times: List[str] = None,
        max_per_day: int = 3,
        topics: List[str] = None
    ):
        """
        Add a channel to the scheduler.
        
        Args:
            name: Channel name
            channel_id: YouTube channel ID
            upload_times: Upload times for this channel
            max_per_day: Max uploads per day
            topics: Topics for this channel
        """
        config = ChannelConfig(
            name=name,
            channel_id=channel_id,
            upload_times=upload_times,
            max_per_day=max_per_day,
            topics=topics
        )
        self.channels[name] = config
        logger.info(f"Added channel: {name} ({channel_id})")
        
        # Save config
        self._save_config()
    
    def remove_channel(self, name: str):
        """Remove a channel from scheduler."""
        if name in self.channels:
            del self.channels[name]
            logger.info(f"Removed channel: {name}")
            self._save_config()
    
    def enable_channel(self, name: str):
        """Enable a channel."""
        if name in self.channels:
            self.channels[name].enabled = True
            logger.info(f"Enabled channel: {name}")
    
    def disable_channel(self, name: str):
        """Disable a channel."""
        if name in self.channels:
            self.channels[name].enabled = False
            logger.info(f"Disabled channel: {name}")
    
    def get_active_channels(self) -> List[ChannelConfig]:
        """Get all active channels."""
        return [c for c in self.channels.values() if c.enabled]
    
    def get_channel_schedule(self, name: str) -> Optional[ChannelConfig]:
        """Get schedule for a specific channel."""
        return self.channels.get(name)
    
    def _save_config(self):
        """Save channel configuration to file."""
        try:
            config_data = {
                "channels": [
                    {
                        "name": c.name,
                        "channel_id": c.channel_id,
                        "upload_times": c.upload_times,
                        "max_per_day": c.max_per_day,
                        "topics": c.topics,
                        "enabled": c.enabled,
                    }
                    for c in self.channels.values()
                ]
            }
            
            Path(self.config_file).parent.mkdir(exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)
            
            logger.debug(f"Saved channel config to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def _load_config(self):
        """Load channel configuration from file."""
        try:
            if not Path(self.config_file).exists():
                logger.debug(f"No existing config file: {self.config_file}")
                return
            
            with open(self.config_file, "r") as f:
                config_data = json.load(f)
            
            for ch in config_data.get("channels", []):
                self.add_channel(
                    name=ch["name"],
                    channel_id=ch["channel_id"],
                    upload_times=ch.get("upload_times"),
                    max_per_day=ch.get("max_per_day", 3),
                    topics=ch.get("topics")
                )
            
            logger.info(f"Loaded {len(self.channels)} channels from config")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    
    def get_status(self) -> Dict:
        """Get status of all channels."""
        return {
            "total_channels": len(self.channels),
            "active_channels": len(self.get_active_channels()),
            "channels": [
                {
                    "name": c.name,
                    "channel_id": c.channel_id,
                    "enabled": c.enabled,
                    "upload_times": c.upload_times,
                    "topics": c.topics,
                }
                for c in self.channels.values()
            ],
            "stats": self.stats
        }


def sync_upload_across_channels(
    channels: List[ChannelConfig],
    video_path: str,
    title: str,
    description: str,
    tags: List[str]
) -> Dict[str, bool]:
    """
    Upload the same video to multiple channels.
    
    Args:
        channels: List of channels to upload to
        video_path: Path to video file
        title: Video title
        description: Video description
        tags: Video tags
        
    Returns:
        Dict mapping channel names to success status
    """
    results = {}
    
    for channel in channels:
        try:
            if not channel.enabled:
                logger.info(f"Skipping disabled channel: {channel.name}")
                results[channel.name] = False
                continue
            
            logger.info(f"Uploading to channel: {channel.name}")
            # Actual upload would happen here via YouTube API
            # For now, this is a placeholder
            results[channel.name] = True
            
        except Exception as e:
            logger.error(f"Failed to upload to {channel.name}: {e}")
            results[channel.name] = False
    
    return results


def batch_upload(
    scheduler: MultiChannelScheduler,
    videos: List[Dict]
) -> Dict:
    """
    Upload multiple videos to multiple channels.
    
    Args:
        scheduler: MultiChannelScheduler instance
        videos: List of video dicts with metadata
        
    Returns:
        Results dict
    """
    results = {
        "total_videos": len(videos),
        "total_channels": len(scheduler.get_active_channels()),
        "uploads": []
    }
    
    for video in videos:
        upload_result = sync_upload_across_channels(
            scheduler.get_active_channels(),
            video["path"],
            video["title"],
            video["description"],
            video["tags"]
        )
        results["uploads"].append(upload_result)
    
    return results


if __name__ == "__main__":
    # Test example
    logging.basicConfig(level=logging.INFO)
    
    scheduler = MultiChannelScheduler()
    
    # Add some channels
    scheduler.add_channel(
        "Main Channel",
        "UCxxxxxxxxxxxxxx",
        upload_times=["09:00", "14:00"],
        topics=["money", "motivation"]
    )
    
    scheduler.add_channel(
        "Backup Channel",
        "UCyyyyyyyyyyyyyyyy",
        upload_times=["20:00"],
        topics=["psychology"]
    )
    
    # Get status
    status = scheduler.get_status()
    print("Scheduler Status:")
    print(json.dumps(status, indent=2, default=str))
    
    # Get active channels
    active = scheduler.get_active_channels()
    print(f"\nActive channels: {len(active)}")
    for ch in active:
        print(f"  - {ch.name}: {ch.upload_times}")
