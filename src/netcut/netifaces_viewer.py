import psutil
import netifaces
from rich.console import Console
from rich.table import Table

def show_interfaces():
    console = Console()
    table = Table(title="Network Interfaces")

    table.add_column("Interface")
    table.add_column("IP Address")
    table.add_column("MAC Address")
    table.add_column("RX Bytes")
    table.add_column("TX Bytes")

    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        ip = addrs.get(netifaces.AF_INET, [{}])[0].get('addr', '-')
        mac = addrs.get(netifaces.AF_LINK, [{}])[0].get('addr', '-')
        stats = psutil.net_io_counters(pernic=True).get(iface)
        rx = str(stats.bytes_recv) if stats else '-'
        tx = str(stats.bytes_sent) if stats else '-'
        table.add_row(iface, ip, mac, rx, tx)

    console.print(table)