import subprocess
import time
import platform
from rich.console import Console
from rich.table import Table

def export_wifi_heatmap():
    console = Console()
    table = Table(title="📶 WiFi Signal Heatmap")
    table.add_column("SSID", style="cyan")
    table.add_column("Signal", style="magenta")
    table.add_column("Timestamp", style="green")

    found = False
    os_name = platform.system()

    for _ in range(3):
        if os_name == "Darwin":
            try:
                result = subprocess.run(["networksetup", "-listpreferredwirelessnetworks", "en0"], capture_output=True, text=True, check=True)
                lines = result.stdout.strip().splitlines()
            except Exception as e:
                console.print(f"[red]Failed to query preferred networks: {e}[/red]")
                return

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for line in lines[1:]:
                ssid = line.strip()
                if ssid:
                    table.add_row(ssid, "?", timestamp)
                    found = True

        elif os_name == "Linux":
            scan = subprocess.getoutput("nmcli -t -f SSID,SIGNAL dev wifi")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for line in scan.strip().splitlines():
                parts = line.split(":")
                if len(parts) == 2 and parts[0].strip():
                    ssid, signal = parts
                    table.add_row(ssid, signal, timestamp)
                    found = True

        time.sleep(1)

    if found:
        console.print(table)
    else:
        console.print("[bold red]⚠️ No WiFi networks found.[/bold red]")