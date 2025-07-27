import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_proxy(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        start = time.time()
        session = requests.Session()
        session.verify = False
        session.trust_env = False
        r = session.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        end = time.time()
        if "application/json" in r.headers.get("Content-Type", ""):
            print("Your IP via Proxy:", r.json().get("origin"))
        else:
            print("Non-JSON response received:")
            print(r.text.strip())
        print("Latency (ms):", round((end - start) * 1000, 2))
    except Exception as e:
        print("Proxy check failed:", e)