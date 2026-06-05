# channel_manager.py
import os
import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from logger import log_line

class ChannelState:
    def __init__(self, cfg):
        self.cfg = cfg
        self.name = cfg.get("name", "default_channel")
        self.env_path = cfg.get("env_path", ".env")
        self.uploads_today = 0
        self.last_reset = datetime.date.today()
        self.ramp_start = cfg.get("ramp_start", datetime.date.today())
        self.max_uploads_per_day = cfg.get("max_uploads_per_day", 3)

    def reset_daily_if_needed(self):
        if datetime.date.today() != self.last_reset:
            self.uploads_today = 0
            self.last_reset = datetime.date.today()

    def can_upload(self):
        self.reset_daily_if_needed()
        return self.uploads_today < self.max_uploads_per_day

    def record_upload(self):
        self.uploads_today += 1

    def uploads_remaining(self):
        self.reset_daily_if_needed()
        return self.max_uploads_per_day - self.uploads_today

class ChannelManager:
    """
    Multi-channel manager that loads credentials from .env or channel configs.
    Designed for easy expansion: add REFRESH_TOKEN_<NAME> to .env to add channels.
    
    Usage:
        # Single channel from .env (default)
        mgr = ChannelManager()
        youtube = mgr.get_youtube_for_channel("doughvinci")
        
        # Or multi-channel from config
        channels = [{"name": "ch1", "refresh_token_env": "REFRESH_TOKEN_CH1"}, ...]
        mgr = ChannelManager(channels_config=channels)
    """
    
    def __init__(self, channels_config=None):
        """
        Initialize channel manager.
        
        Args:
            channels_config: List of channel dicts with 'name' and 'refresh_token_env' keys.
                           If None, will use single default channel from .env.
        """
        load_dotenv()  # Load .env automatically
        
        if channels_config is None:
            self.channels_config = []
            for env_name, env_value in os.environ.items():
                if not env_name.startswith("REFRESH_TOKEN_"):
                    continue
                channel_name = env_name.replace("REFRESH_TOKEN_", "").lower()
                if not channel_name:
                    continue
                preferred_niche = os.getenv(f"PREFERRED_NICHE_{channel_name.upper()}")
                self.channels_config.append({
                    "name": channel_name,
                    "refresh_token_env": env_name,
                    "preferred_niche": preferred_niche
                })
            if not self.channels_config:
                # Single-channel default fallback
                self.channels_config = [
                    {
                        "name": "doughvinci",
                        "refresh_token_env": "REFRESH_TOKEN_DOUGHVINCI",
                        "preferred_niche": "personal finance"
                    }
                ]
        else:
            self.channels_config = channels_config
        
        self.states = {}
        for ch in self.channels_config:
            name = ch["name"]
            self.states[name] = ChannelState(ch)
    
    def get_youtube_for_channel(self, channel_name=None):
        """
        Build and return YouTube client for a channel.
        
        Args:
            channel_name: Name of channel. If None, uses first channel.
        
        Returns:
            Authenticated youtube resource object.
        """
        if channel_name is None:
            channel_name = self.channels_config[0]["name"]
        
        # Find channel config
        channel_cfg = None
        for ch in self.channels_config:
            if ch["name"] == channel_name:
                channel_cfg = ch
                break
        
        if channel_cfg is None:
            raise ValueError(f"Channel '{channel_name}' not found in config")
        
        # Load refresh token from environment
        refresh_token_env_var = channel_cfg.get("refresh_token_env", "REFRESH_TOKEN")
        refresh_token = os.getenv(refresh_token_env_var)
        
        if not refresh_token:
            raise ValueError(f"Environment variable {refresh_token_env_var} not set for channel {channel_name}")
        
        # Build credentials
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token"
        )
        
        # Build YouTube client
        youtube = build("youtube", "v3", credentials=creds)
        
        # Attach analytics client if available
        try:
            analytics = build("youtubeAnalytics", "v2", credentials=creds)
            youtube.analytics = analytics
        except Exception:
            log_line(f"Analytics client not available for channel {channel_name}")
        
        return youtube
    
    def get_state(self, channel_name=None):
        """Get channel state."""
        if channel_name is None:
            channel_name = self.channels_config[0]["name"]
        return self.states.get(channel_name)
    
    def record_upload(self, channel_name=None):
        """Record an upload for a channel."""
        if channel_name is None:
            channel_name = self.channels_config[0]["name"]
        state = self.get_state(channel_name)
        if state:
            state.record_upload()
    
    def get_all_channels(self):
        """Return list of all configured channels."""
        return [ch["name"] for ch in self.channels_config]
    
    def find_thumbnail_for(self, file_path):
        """Find thumbnail file matching video file."""
        base = os.path.splitext(file_path)[0]
        for ext in (".jpg", ".png", ".webp"):
            p = base + ext
            if os.path.exists(p):
                return p
        return None
