import subprocess
import time
import json

def export_wifi_heatmap():
    data = []
    for _ in range(5):
        scan = subprocess.getoutput("nmcli -t -f SSID,SIGNAL dev wifi")
        timestamp = time.time()
        for line in scan.strip().splitlines():
            parts = line.split(":")
            if len(parts) == 2:
                ssid, signal = parts
                data.append({"ssid": ssid, "signal": signal, "timestamp": timestamp})
        time.sleep(1)
    with open("wifi_heatmap.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Exported wifi_heatmap.json")