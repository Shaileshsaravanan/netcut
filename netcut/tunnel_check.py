import requests
import socket

def detect_tunnel_leak():
    try:
        ip = requests.get("https://api.ipify.org").text
        print(f"🌐 Public IP: {ip}")
        dns = socket.getaddrinfo("example.com", 80)
        print("🔍 DNS Resolution Path:")
        for entry in dns:
            print(f"  {entry[4][0]}")
    except Exception as e:
        print("❌ Error detecting VPN leak:", e)