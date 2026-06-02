"""
Unit tests for multi_channel_support module.
"""

import pytest
import logging
import json
import tempfile
from pathlib import Path
from modules.multi_channel_support import (
    ChannelConfig,
    MultiChannelScheduler,
    sync_upload_across_channels,
    batch_upload,
)


logger = logging.getLogger(__name__)


class TestChannelConfig:
    """Tests for ChannelConfig class."""
    
    def test_init_required_fields(self):
        """Test ChannelConfig with required fields."""
        config = ChannelConfig("Test Channel", "UCxxxx")
        
        assert config.name == "Test Channel"
        assert config.channel_id == "UCxxxx"
        assert config.enabled is True
    
    def test_init_with_all_fields(self):
        """Test ChannelConfig with all fields."""
        config = ChannelConfig(
            name="Test",
            channel_id="UCxxxx",
            upload_times=["09:00", "14:00"],
            max_per_day=2,
            topics=["money"],
            enabled=False
        )
        
        assert config.upload_times == ["09:00", "14:00"]
        assert config.max_per_day == 2
        assert config.topics == ["money"]
        assert config.enabled is False
    
    def test_default_values(self):
        """Test default values for optional fields."""
        config = ChannelConfig("Test", "UCxxxx")
        
        assert len(config.upload_times) == 3
        assert config.max_per_day == 3
        assert len(config.topics) > 0


class TestMultiChannelScheduler:
    """Tests for MultiChannelScheduler class."""
    
    def test_init(self):
        """Test scheduler initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            assert len(scheduler.channels) == 0
            assert scheduler.stats["total_uploads"] == 0
    
    def test_add_channel(self):
        """Test adding a channel."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Main", "UCmain", upload_times=["09:00"])
            
            assert "Main" in scheduler.channels
            assert scheduler.channels["Main"].channel_id == "UCmain"
    
    def test_remove_channel(self):
        """Test removing a channel."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Test", "UCtest")
            scheduler.remove_channel("Test")
            
            assert "Test" not in scheduler.channels
    
    def test_enable_disable_channel(self):
        """Test enabling and disabling channels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Test", "UCtest")
            assert scheduler.channels["Test"].enabled is True
            
            scheduler.disable_channel("Test")
            assert scheduler.channels["Test"].enabled is False
            
            scheduler.enable_channel("Test")
            assert scheduler.channels["Test"].enabled is True
    
    def test_get_active_channels(self):
        """Test retrieving active channels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Active1", "UC1")
            scheduler.add_channel("Active2", "UC2")
            scheduler.add_channel("Inactive", "UC3")
            scheduler.disable_channel("Inactive")
            
            active = scheduler.get_active_channels()
            assert len(active) == 2
            active_names = [c.name for c in active]
            assert "Active1" in active_names
            assert "Active2" in active_names
            assert "Inactive" not in active_names
    
    def test_get_channel_schedule(self):
        """Test retrieving specific channel schedule."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Test", "UCtest", upload_times=["10:00", "15:00"])
            
            config = scheduler.get_channel_schedule("Test")
            assert config is not None
            assert config.upload_times == ["10:00", "15:00"]
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            
            # Create and save config
            scheduler1 = MultiChannelScheduler(str(config_file))
            scheduler1.add_channel("Test1", "UC1", upload_times=["09:00"])
            scheduler1.add_channel("Test2", "UC2", upload_times=["14:00"])
            
            # Load in new instance
            scheduler2 = MultiChannelScheduler(str(config_file))
            
            assert len(scheduler2.channels) == 2
            assert "Test1" in scheduler2.channels
            assert "Test2" in scheduler2.channels
    
    def test_get_status(self):
        """Test getting scheduler status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Main", "UCmain")
            scheduler.add_channel("Backup", "UCbackup")
            scheduler.disable_channel("Backup")
            
            status = scheduler.get_status()
            
            assert status["total_channels"] == 2
            assert status["active_channels"] == 1
            assert len(status["channels"]) == 2


class TestSyncUploadAcrossChannels:
    """Tests for synced uploads."""
    
    def test_sync_upload_basic(self):
        """Test basic sync upload."""
        channels = [
            ChannelConfig("Channel1", "UC1"),
            ChannelConfig("Channel2", "UC2"),
        ]
        
        results = sync_upload_across_channels(
            channels,
            "video.mp4",
            "Test Title",
            "Test Description",
            ["tag1", "tag2"]
        )
        
        assert len(results) == 2
        assert all(isinstance(v, bool) for v in results.values())
    
    def test_sync_upload_skips_disabled(self):
        """Test that disabled channels are skipped."""
        channels = [
            ChannelConfig("Active", "UC1", enabled=True),
            ChannelConfig("Inactive", "UC2", enabled=False),
        ]
        
        results = sync_upload_across_channels(
            channels,
            "video.mp4",
            "Title",
            "Description",
            []
        )
        
        assert results["Active"] is True
        assert results["Inactive"] is False


class TestBatchUpload:
    """Tests for batch uploads."""
    
    def test_batch_upload(self):
        """Test batch upload to multiple channels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            scheduler = MultiChannelScheduler(str(config_file))
            
            scheduler.add_channel("Channel1", "UC1")
            scheduler.add_channel("Channel2", "UC2")
            
            videos = [
                {
                    "path": "video1.mp4",
                    "title": "Video 1",
                    "description": "Desc 1",
                    "tags": ["tag1"]
                },
                {
                    "path": "video2.mp4",
                    "title": "Video 2",
                    "description": "Desc 2",
                    "tags": ["tag2"]
                }
            ]
            
            results = batch_upload(scheduler, videos)
            
            assert results["total_videos"] == 2
            assert results["total_channels"] == 2
            assert len(results["uploads"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
