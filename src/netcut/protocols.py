import subprocess, socket

def icmp_ping(host):
    try:
        subprocess.run(["ping", "-c", "3", host], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def tcp_check(host, port=22):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"TCP {host}:{port} is reachable.")
            return True
    except socket.error:
        print(f"TCP {host}:{port} is not reachable.")
        return False