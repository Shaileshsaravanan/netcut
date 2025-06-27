import os
import toml

DEFAULT_CONFIG = {
    "groups": {
        "browsers": ["chrome", "safari", "firefox"],
        "meetings": ["zoom", "teams"]
    },
    "allowlist": ["system preferences", "finder"],
    "defaults": {
        "block_duration": "10m",
        "persistent_block": False
    }
}

CONFIG_PATH = os.path.expanduser("~/.netcut/config.toml")

def ensure_config():
    if not os.path.exists(CONFIG_PATH):
        save(DEFAULT_CONFIG)

def load():
    ensure_config()
    with open(CONFIG_PATH) as f:
        return toml.load(f)

def save(data):
    with open(CONFIG_PATH, "w") as f:
        toml.dump(data, f)

def get_group(name):
    cfg = load()
    return cfg.get("groups", {}).get(name.lower(), [])

def is_allowed(app_name):
    cfg = load()
    allowed = [a.lower() for a in cfg.get("allowlist", [])]
    return app_name.lower() in allowed

def get_default(key):
    cfg = load()
    return cfg.get("defaults", {}).get(key)