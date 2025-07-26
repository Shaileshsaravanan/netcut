import requests
import time

def check_proxy(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        start = time.time()
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        end = time.time()
        print("Your IP via Proxy:", r.json().get("origin"))
        print("Latency (ms):", round((end - start) * 1000, 2))
    except Exception as e:
        print("Proxy check failed:", e)