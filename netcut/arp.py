import os
from collections import defaultdict
from rich.console import Console
from rich.table import Table

def view_arp_table():
    console = Console()
    arp_table = os.popen("arp -a").read()
    table = Table(title="ARP Table")
    table.add_column("IP")
    table.add_column("MAC")
    table.add_column("Interface")
    mac_map = defaultdict(list)
    for line in arp_table.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            ip, mac, iface = parts[0], parts[1], parts[-1]
            mac_map[mac].append(ip)
            table.add_row(ip, mac, iface)
    console.print(table)
    for mac, ips in mac_map.items():
        if len(ips) > 1:
            console.print(f"[bold red]Potential ARP spoofing detected on MAC {mac} used by: {', '.join(ips)}[/bold red]")