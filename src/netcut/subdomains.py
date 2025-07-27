import requests

def enumerate_subdomains(domain):
    found = set()
    print(f"🔍 Searching CertSpotter for SSL-certified subdomains of {domain}...")

    try:
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        for entry in data:
            for name in entry.get("dns_names", []):
                if name.endswith(domain):
                    found.add(name.strip())

    except Exception as e:
        print(f"⚠️ CertSpotter lookup failed: {e}")

    if found:
        print(f"\n✅ Found {len(found)} subdomains with SSL certificates:")
        for sub in sorted(found):
            print(f"  • {sub}")
    else:
        print("❌ No SSL-certified subdomains found.")