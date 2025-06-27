import os
from datetime import datetime

LOG_PATH = os.path.expanduser("~/.netcut/log.txt")

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def write(action, app=None, detail=None):
    ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{timestamp} | {action}"
    if app:
        msg += f" | {app}"
    if detail:
        msg += f" | {detail}"
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")

def read(limit=50):
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH) as f:
        lines = f.readlines()
    return lines[-limit:]

def clear():
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)