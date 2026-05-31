# logger.py
import os
from datetime import datetime

LOG_PATH = "logs"
LOG_FILE = os.path.join(LOG_PATH, "uploader.log")

def ensure_log_folder():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

def log_line(line):
    ensure_log_folder()
    ts = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {line}\n")
    print(line)
