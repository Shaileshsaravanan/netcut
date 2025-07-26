from scapy.all import sniff
from rich.console import Console
from rich.table import Table

def packet_filter(pkt, port=None, proto=None, src=None, dst=None):
    if port and (pkt.haslayer("TCP") or pkt.haslayer("UDP")):
        l4 = pkt["TCP"] if pkt.haslayer("TCP") else pkt["UDP"]
        if l4.sport != int(port) and l4.dport != int(port):
            return False
    if proto and not pkt.haslayer(proto):
        return False
    if src and pkt[0][1].src != src:
        return False
    if dst and pkt[0][1].dst != dst:
        return False
    return True

def sniff_packets(port=None, proto=None, src=None, dst=None):
    console = Console()
    def process(pkt):
        if packet_filter(pkt, port, proto, src, dst):
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Src")
            table.add_column("Dst")
            table.add_column("Proto")
            table.add_column("Len")
            proto_type = pkt.lastlayer().name
            table.add_row(pkt[0][1].src, pkt[0][1].dst, proto_type, str(len(pkt)))
            console.print(table)
    sniff(prn=process, store=0)