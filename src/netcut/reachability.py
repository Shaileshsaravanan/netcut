import requests

def check_reachability(file):
    with open(file) as f:
        targets = [line.strip() for line in f if line.strip()]
    for target in targets:
        try:
            r = requests.get(target, timeout=3)
            print(f"{target} ✅ {r.status_code} {r.elapsed.total_seconds():.2f}s")
        except Exception as e:
            print(f"{target} ❌ {e}")