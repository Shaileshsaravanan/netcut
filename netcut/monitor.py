import subprocess
import time
import re
from netcut import process

def parse_nettop(app_name):
    try:
        result = subprocess.run(
            ["nettop", "-J", "-P", "-x", "-l", "1", "-t", "wifi", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=3
        )
        lines = result.stdout.decode().splitlines()
    except Exception:
        return None

    app_name = app_name.lower()
    rx = re.compile(r"(?P<proc>.+?)\s+\[\d+\].+?in:(?P<in>\d+).+?out:(?P<out>\d+)", re.I)

    total_in = 0
    total_out = 0
    for line in lines:
        match = rx.search(line)
        if match:
            proc = match.group("proc").lower()
            if app_name in proc:
                total_in += int(match.group("in"))
                total_out += int(match.group("out"))

    return total_in, total_out

def format_speed(bytes_in, bytes_out, interval):
    kb_in = (bytes_in / 1024) / interval
    kb_out = (bytes_out / 1024) / interval
    return f"in: {kb_in:.1f} kbps | out: {kb_out:.1f} kbps"

def monitor_app(app_name, interval=1, once=False):
    print(f"monitoring {app_name}")
    last_in, last_out = parse_nettop(app_name)
    if last_in is None:
        print("app not found or no network data")
        return

    while True:
        time.sleep(interval)
        new_in, new_out = parse_nettop(app_name)
        if new_in is None:
            print("lost track of app")
            break

        delta_in = new_in - last_in
        delta_out = new_out - last_out
        last_in, last_out = new_in, new_out

        print(format_speed(delta_in, delta_out, interval))

        if once:
            break