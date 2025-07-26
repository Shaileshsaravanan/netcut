import socket
from ping3 import ping

def icmp_ping(host, timeout=2):
    try:
        delay = ping(host, timeout=timeout)
        if delay is None:
            return False, None
        return True, round(delay * 1000, 2)  # ms
    except Exception:
        return False, None

def tcp_check(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def check_host(host, port=80):
    print(f"🔍 Checking Host: {host}")
    
    print("\n🌐 ICMP Ping:")
    icmp_result, delay = icmp_ping(host)
    if icmp_result:
        print(f"✅ ICMP Ping Success - {delay} ms")
    else:
        print("❌ ICMP Ping Failed")

    print(f"\n🔌 TCP Port {port} Check:")
    if tcp_check(host, port):
        print(f"✅ TCP Port {port} is OPEN")
    else:
        print(f"❌ TCP Port {port} is CLOSED or BLOCKED")