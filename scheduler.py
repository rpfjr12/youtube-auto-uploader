# scheduler.py
import os
import json
import random
import time
import threading
import hashlib
import datetime
from pathlib import Path
from dotenv import load_dotenv
from channel_manager import ChannelManager
from metadata import generate_metadata
from uploader import upload_video
from thumbnails import upload_thumbnail
from logger import log_line
from analytics import fetch_channel_metrics

CONFIG_PATH = "channels.json"
UPLOADS_FOLDER = "uploads"

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def pick_random_time_in_window(window):
    start = datetime.datetime.strptime(window[0], "%H:%M").time()
    end = datetime.datetime.strptime(window[1], "%H:%M").time()
    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, start)
    end_dt = datetime.datetime.combine(today, end)
    if end_dt <= start_dt:
        end_dt += datetime.timedelta(days=1)
    delta = (end_dt - start_dt).total_seconds()
    offset = random.randint(0, max(0, int(delta)))
    return start_dt + datetime.timedelta(seconds=offset)

class Scheduler:
    def __init__(self, config_path=CONFIG_PATH):
        self.config = self._load_config(config_path)
        self.channel_mgr = ChannelManager(self.config["channels"])
        self.global_cfg = self.config.get("global", {})
        self.max_concurrent = self.global_cfg.get("max_concurrent_uploads", 2)
        self.seen_hashes = set()
        self.lock = threading.Lock()
        self.active_uploads = 0

    def _load_config(self, path):
        with open(path) as f:
            return json.load(f)

    def _list_upload_files(self):
        p = Path(UPLOADS_FOLDER)
        if not p.exists():
            p.mkdir(parents=True)
        files = [str(x) for x in p.iterdir() if x.suffix.lower() in (".mp4", ".mov", ".mkv")]
        random.shuffle(files)
        return files

    def _can_start_upload(self):
        with self.lock:
            return self.active_uploads < self.max_concurrent

    def _start_upload_thread(self, channel, file_path):
        with self.lock:
            self.active_uploads += 1
        t = threading.Thread(target=self._process_upload, args=(channel, file_path))
        t.daemon = True
        t.start()

    def _process_upload(self, channel, file_path):
        try:
            # small randomized delay to avoid identical timing
            time.sleep(random.uniform(2, 30))
            # load channel credentials into env and build client
            youtube = self.channel_mgr.get_youtube_for_channel(channel)
            # generate metadata with channel-aware diversification
            title, description, tags = generate_metadata(file_path, channel["name"])
            vid_id = upload_video(youtube, file_path, title, description, tags)
            # optional thumbnail
            thumb = self.channel_mgr.find_thumbnail_for(file_path)
            if thumb:
                upload_thumbnail(youtube, vid_id, thumb)
            log_line(f"{datetime.datetime.utcnow().isoformat()} | {channel['name']} | {file_path} | SUCCESS | {vid_id}")
            # record seen hash for uniqueness
            h = file_hash(file_path)
            self.seen_hashes.add(h)
            self.channel_mgr.record_upload(channel["name"])
        except Exception as e:
            log_line(f"{datetime.datetime.utcnow().isoformat()} | {channel['name']} | {file_path} | ERROR | {e}")
            # simple retry logic: requeue file by leaving it in uploads folder
        finally:
            with self.lock:
                self.active_uploads -= 1

    def run_once(self):
        files = self._list_upload_files()
        if not files:
            return
        # fetch analytics to bias channel ordering
        perf = {}
        for ch in self.config["channels"]:
            try:
                self.channel_mgr.load_env_for_channel(ch["env"])
                perf[ch["name"]] = fetch_channel_metrics(self.channel_mgr.get_youtube_for_channel(ch))
            except Exception:
                perf[ch["name"]] = {"score": 0}
        # sort channels by performance descending so better channels get priority
        channels_sorted = sorted(self.config["channels"], key=lambda c: perf.get(c["name"], {}).get("score", 0), reverse=True)
        for file_path in files:
            h = file_hash(file_path)
            if h in self.seen_hashes:
                continue
            # try to assign to a channel that can accept uploads now
            random.shuffle(channels_sorted)
            for ch in channels_sorted:
                state = self.channel_mgr.get_state(ch["name"])
                state.reset_daily_if_needed()
                allowed_today = state.allowed_today()
                if state.uploads_today >= allowed_today:
                    continue
                # schedule immediate upload if concurrency allows
                if self._can_start_upload():
                    self._start_upload_thread(ch, file_path)
                    break
            # small pause between assignment attempts
            time.sleep(0.5)

    def loop(self):
        while True:
            try:
                self.run_once()
            except Exception as e:
                log_line(f"{datetime.datetime.utcnow().isoformat()} | SCHEDULER ERROR | {e}")
            time.sleep(30)

if __name__ == "__main__":
    s = Scheduler()
    s.loop()
