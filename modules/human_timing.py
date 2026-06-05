import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

HISTORY_FILE = Path("uploads/human_timing_history.json")
DEFAULT_SLEEP_WINDOWS = [(0, 4)]


class HumanTiming:
    """Human-like upload timing helper."""

    def __init__(self, sleep_windows: Optional[List[Tuple[int, int]]] = None):
        self.sleep_windows = sleep_windows or DEFAULT_SLEEP_WINDOWS
        self.history = self._load_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try:
                return json.loads(HISTORY_FILE.read_text())
            except Exception:
                return {}
        return {}

    def _save_history(self):
        HISTORY_FILE.parent.mkdir(exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(self.history or {}, indent=2))

    def randomize_schedule_time(self, time_str: str, max_offset: int = 5) -> str:
        """Return a schedule time with a small offset and avoid repeated exact patterns."""
        offset = random.randint(-max_offset, max_offset)
        from modules.randomization_engine import format_time_with_offset

        candidate = format_time_with_offset(time_str, offset)
        past_times = self.history.get("scheduled_times", [])

        if candidate in past_times:
            offset = random.randint(-max_offset, max_offset)
            candidate = format_time_with_offset(time_str, offset)

        self.history.setdefault("scheduled_times", []).append(candidate)
        self.history["scheduled_times"] = self.history["scheduled_times"][-20:]
        self._save_history()
        return candidate

    def random_upload_delay(self, max_seconds: int = 180) -> int:
        """Return a small delay in seconds to introduce upload jitter."""
        delay = random.randint(0, max_seconds)
        self.history.setdefault("last_delay", 0)
        self.history["last_delay"] = delay
        self._save_history()
        return delay

    def in_sleep_window(self, now: Optional[datetime] = None) -> bool:
        """Return True when the current time is within a configured sleep window."""
        now = now or datetime.now()
        hour = now.hour
        for start, end in self.sleep_windows:
            if start <= hour < end:
                return True
        return False

    def seconds_until_window_end(self, now: Optional[datetime] = None) -> int:
        """Return seconds until the current sleep window ends."""
        now = now or datetime.now()
        hour = now.hour
        minute = now.minute
        for start, end in self.sleep_windows:
            if start <= hour < end:
                end_time = now.replace(hour=end, minute=0, second=0, microsecond=0)
                if end <= hour:
                    end_time += timedelta(days=1)
                delta = end_time - now
                return int(delta.total_seconds())
        return 0

    def avoid_pattern(self, candidate_time: str) -> str:
        """Avoid repeating exact scheduled times from history."""
        past_times = self.history.get("scheduled_times", [])
        if candidate_time in past_times:
            return self.randomize_schedule_time(candidate_time)
        return candidate_time
