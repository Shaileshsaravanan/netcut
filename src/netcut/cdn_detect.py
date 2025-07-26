import socket
import requests

def detect_cdn(domain):
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://{domain}")
        headers = r.headers
        print("IP Address:", ip)
        print("Server Header:", headers.get("Server", "N/A"))
        print("Via:", headers.get("Via", "N/A"))
        print("CDN Detected:", "Cloudflare" if "cf-ray" in headers else "Unknown")
    except Exception as e:
        print("Error:", e)