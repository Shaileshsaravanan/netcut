import requests
import socket

def geo_lookup(host):
    ip = socket.gethostbyname(host)
    response = requests.get(f"http://ip-api.com/json/{ip}").json()
    
    print(f"[{host}] -> {ip}")
    print("Country:", response.get("country"))
    print("Region:", response.get("regionName"))
    print("City:", response.get("city"))
    print("ISP:", response.get("isp"))