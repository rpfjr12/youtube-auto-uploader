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
        self.name = cfg["name"]
        self.env_path = cfg["env"]
        self.uploads_today = 0
        self.last_reset = datetime.date.today()
        self.ramp_start = datetime.date.today()

    def reset_daily_if_needed(self):
        if datetime.date.today() != self.last_reset:
            self.uploads_today = 0
            self.last_reset = datetime.date.today()

    def allowed_today(self):
        days = (datetime.date.today() - self.ramp_start).days
        ramp_days = self.cfg.get("ramp_days", 7)
        ramp = min(days, ramp_days)
        min_u = self.cfg.get("min_uploads_per_day", 1)
        max_u = self.cfg.get("max_uploads_per_day", 3)
        if ramp_days <= 1:
            return max_u
        allowed = int(min_u + (max_u - min_u) * (ramp / ramp_days))
        return max(1, allowed)

    def record_upload(self):
        self.uploads_today += 1

class ChannelManager:
    def __init__(self, channels_cfg):
        self.channels_cfg = channels_cfg
        self.states = {c["name"]: ChannelState(c) for c in channels_cfg}

    def load_env_for_channel(self, env_path):
        load_dotenv(env_path, override=True)

    def get_youtube_for_channel(self, channel_cfg):
        # load env for that channel
        self.load_env_for_channel(channel_cfg["env"])
        creds = Credentials(
            None,
            refresh_token=os.getenv("REFRESH_TOKEN"),
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token"
        )
        youtube = build("youtube", "v3", credentials=creds)
        # also build analytics client
        try:
            analytics = build("youtubeAnalytics", "v2", credentials=creds)
            youtube.analytics = lambda : analytics
        except Exception:
            log_line("Analytics client not available for channel " + channel_cfg["name"])
        return youtube

    def get_state(self, name):
        return self.states[name]

    def record_upload(self, name):
        self.states[name].record_upload()

    def find_thumbnail_for(self, file_path):
        base = os.path.splitext(file_path)[0]
        for ext in (".jpg", ".png", ".webp"):
            p = base + ext
            if os.path.exists(p):
                return p
        return None
