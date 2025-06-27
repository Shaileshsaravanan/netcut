import platform, sys
from . import mac, scheduler, process

def require_mac():
    if platform.system() != "Darwin":
        print("netcut only supports macos.")
        sys.exit(1)

def block_app(app_name_or_path, duration=None):
    require_mac()
    try:
        pid = process.find_pid(app_name_or_path)
        uid = process.get_uid_from_pid(pid)
    except Exception as e:
        print(f"failed to find process '{app_name_or_path}': {e}")
        return
    print(f"blocking internet for '{app_name_or_path}' (pid: {pid}, uid: {uid})")
    try:
        mac.block(uid)
    except Exception as e:
        print(f"failed to block: {e}")
        return
    if duration:
        scheduler.schedule_unblock(uid, mac, duration)

def unblock_app(app_name_or_path):
    require_mac()
    try:
        pid = process.find_pid(app_name_or_path)
        uid = process.get_uid_from_pid(pid)
    except Exception as e:
        print(f"failed to find process '{app_name_or_path}': {e}")
        return
    print(f"unblocking internet for '{app_name_or_path}' (pid: {pid}, uid: {uid})")
    try:
        mac.unblock(uid)
    except Exception as e:
        print(f"failed to unblock: {e}")

def list_network_apps():
    apps = process.list_network_processes()
    if not apps:
        print("no active network processes found.")
        return
    print("network-active processes:")
    seen = set()
    for proc in apps:
        key = (proc["pid"], proc["name"])
        if key not in seen:
            print(f" - {proc['name']} (pid: {proc['pid']})")
            seen.add(key)