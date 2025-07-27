import requests
import time

def monitor_api(url, headers):
    hdrs = {}
    if headers:
        try:
            for h in headers.split(";"):
                if ":" in h:
                    k, v = h.split(":", 1)
                    hdrs[k.strip()] = v.strip()
        except Exception as e:
            print(f"❌ Failed to parse headers: {e}")
            return

    try:
        start = time.time()
        r = requests.get(url, headers=hdrs)
        end = time.time()
        print("Status Code:", r.status_code)
        print("Latency (ms):", round((end - start) * 1000, 2))
        print("Headers:", r.headers)
    except Exception as e:
        print("Error:", e)