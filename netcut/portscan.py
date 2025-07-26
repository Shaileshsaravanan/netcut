import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return port
    except:
        return None

def scan_ports(host, fast=False):
    ports = range(1, 1025) if fast else range(1, 65536)
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(host, p), ports)
    for port in results:
        if port:
            open_ports.append(port)
    print(f"Open ports on {host}: {', '.join(map(str, open_ports))}")