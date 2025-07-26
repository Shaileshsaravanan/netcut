import subprocess

def detect_mitm():
    arp_output = subprocess.getoutput("arp -a")
    macs = [line.split()[1] for line in arp_output.splitlines() if "-" in line or ":" in line]
    duplicates = set([mac for mac in macs if macs.count(mac) > 1])
    if duplicates:
        print("⚠️ Possible MITM detected: Duplicate MACs ->", duplicates)
    else:
        print("✅ No signs of MITM detected.")