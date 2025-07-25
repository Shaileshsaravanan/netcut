import psutil
import subprocess
import os
import time
import shutil
from datetime import datetime, timedelta

ANCHOR_DIR = "/etc/pf.anchors/netcut"
MAIN_CONF = "/etc/pf.conf"
PERSIST_DIR = "/usr/local/etc/netcut/persistent"
SCHEDULE_FILE = "/tmp/netcut_schedule.txt"

def ensure_dirs():
    if os.path.exists(ANCHOR_DIR):
        if not os.path.isdir(ANCHOR_DIR):
            os.remove(ANCHOR_DIR)
    os.makedirs(ANCHOR_DIR, exist_ok=True)
    os.makedirs(PERSIST_DIR, exist_ok=True)

def get_ports_by_pid(pid):
    ports = set()
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.pid == pid and conn.status == psutil.CONN_ESTABLISHED:
                if conn.laddr and conn.laddr.port:
                    ports.add(conn.laddr.port)
    except Exception:
        pass
    return list(ports)

def pf_rule_lines(ports):
    rules = []
    for port in ports:
        rules.append(f"block drop out proto tcp from any port {port} to any")
        rules.append(f"block drop out proto udp from any port {port} to any")
    return rules

def write_pf_rules(app, ports, dry=False):
    ensure_dirs()
    rules = pf_rule_lines(ports)
    if dry:
        return "\n".join(rules)
    path = os.path.join(ANCHOR_DIR, f"{app}.conf")
    rule_text = "\n".join(rules) + "\n"
    cmd = f"echo '{rule_text}' | sudo tee {path} > /dev/null"
    subprocess.run(cmd, shell=True)

def load_pf():
    subprocess.run(["sudo", "pfctl", "-f", MAIN_CONF], check=False)
    subprocess.run(["sudo", "pfctl", "-e"], check=False)

def block_app(app, pid, dry=False):
    ports = get_ports_by_pid(pid)
    if not ports:
        print("no ports found, using fallback rule")
        try:
            uid = psutil.Process(pid).uids().real
        except Exception:
            uid = 0
        anchor_name = f"netcut_{app}"
        path = f"/etc/pf.anchors/{anchor_name}"
        rules = [f"block drop log out quick on en0 user {uid} to any"]
        if dry:
            return "\n".join(rules)
        ensure_dirs()
        rule_text = "\n".join(rules) + "\n"
        cmd = f"echo '{rule_text}' | sudo tee {path} > /dev/null"
        subprocess.run(cmd, shell=True)

        # Ensure anchor config is present in pf.conf
        with open(MAIN_CONF, "r") as f:
            pfconf = f.read()
        anchor_lines = [
            f'anchor "{anchor_name}"',
            f'load anchor "{anchor_name}" from "{path}"'
        ]
        needs_update = any(line not in pfconf for line in anchor_lines)
        if needs_update:
            anchor_text = "\n" + "\n".join(anchor_lines) + "\n"
            cmd = f"echo '{anchor_text}' | sudo tee -a {MAIN_CONF} > /dev/null"
            subprocess.run(cmd, shell=True)

        load_pf()
        print(f"blocked {app} with fallback rule")
        return

    rules = write_pf_rules(app, ports, dry=dry)
    if not dry:
        load_pf()
        print(f"blocked {app}")
    else:
        print(rules)

def unblock_app(app):
    path = os.path.join(ANCHOR_DIR, f"{app}.conf")
    if os.path.exists(path):
        os.remove(path)
        load_pf()
        print(f"unblocked {app}")

def unblock_all():
    if os.path.exists(ANCHOR_DIR):
        for f in os.listdir(ANCHOR_DIR):
            os.remove(os.path.join(ANCHOR_DIR, f))
        load_pf()
        print("unblocked all")

def export_rules(filepath):
    with open(filepath, "w") as out:
        for f in os.listdir(ANCHOR_DIR):
            app = f.replace(".conf", "")
            with open(os.path.join(ANCHOR_DIR, f)) as rf:
                out.write(f"# {app}\n")
                out.writelines(rf.readlines())
                out.write("\n")

def persist_block(app):
    src = os.path.join(ANCHOR_DIR, f"{app}.conf")
    dst = os.path.join(PERSIST_DIR, f"{app}.conf")
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"persisted {app}")

def clear_persistent():
    for f in os.listdir(PERSIST_DIR):
        os.remove(os.path.join(PERSIST_DIR, f))

def load_persistent_on_boot():
    ensure_dirs()
    for f in os.listdir(PERSIST_DIR):
        shutil.copy(os.path.join(PERSIST_DIR, f), os.path.join(ANCHOR_DIR, f))
    load_pf()

def schedule_unblock(app, duration_sec):
    unblock_time = time.time() + duration_sec
    with open(SCHEDULE_FILE, "a") as f:
        f.write(f"{app},{int(unblock_time)}\n")

def check_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return
    now = int(time.time())
    lines = []
    to_unblock = []
    with open(SCHEDULE_FILE) as f:
        for line in f:
            app, ts = line.strip().split(",")
            if int(ts) <= now:
                to_unblock.append(app)
            else:
                lines.append(line.strip())
    with open(SCHEDULE_FILE, "w") as f:
        for l in lines:
            f.write(l + "\n")
    for app in to_unblock:
        unblock_app(app)

