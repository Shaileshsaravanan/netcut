import psutil
import time
from rich.console import Console
from rich.table import Table

def show_bandwidth():
    console = Console()
    prev = psutil.net_io_counters(pernic=True)
    time.sleep(1)
    curr = psutil.net_io_counters(pernic=True)
    table = Table(title="Bandwidth Usage by Interface")
    table.add_column("Interface")
    table.add_column("TX (KB/s)")
    table.add_column("RX (KB/s)")
    for iface in curr:
        tx = (curr[iface].bytes_sent - prev[iface].bytes_sent) / 1024
        rx = (curr[iface].bytes_recv - prev[iface].bytes_recv) / 1024
        table.add_row(iface, f"{tx:.2f}", f"{rx:.2f}")
    console.print(table)