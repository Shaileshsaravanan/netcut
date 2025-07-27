from rich.table import Table
from rich.console import Console
import psutil

def display_stats():
    console = Console()
    table = Table(title="Current Network Interface Stats")

    table.add_column("Interface", style="bold cyan")
    table.add_column("IP Address", style="bold green")
    table.add_column("MAC Address", style="bold yellow")
    table.add_column("RX (MB)", style="bold magenta")
    table.add_column("TX (MB)", style="bold magenta")
    table.add_column("Packets Sent", style="bold blue")
    table.add_column("Packets Recv", style="bold blue")

    net_addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters(pernic=True)

    for iface, addrs in net_addrs.items():
        ip = "-"
        mac = "-"
        for addr in addrs:
            if addr.family.name == "AF_INET":
                ip = addr.address
            elif addr.family.name == "AF_LINK":
                mac = addr.address

        stats = net_io.get(iface)
        if stats:
            rx = f"{stats.bytes_recv / (1024**2):.2f}"
            tx = f"{stats.bytes_sent / (1024**2):.2f}"
            table.add_row(iface, ip, mac, rx, tx, str(stats.packets_sent), str(stats.packets_recv))

    console.print(table)