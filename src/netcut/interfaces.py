import psutil
import socket

def show_interfaces():
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    net_io_counters = psutil.net_io_counters(pernic=True)

    print(f"{'Interface':<15}{'Status':<10}{'Speed(Mbps)':<13}{'IP Address':<20}{'MAC Address':<20}")
    print("-" * 80)

    for iface, addrs in net_if_addrs.items():
        ip = "-"
        mac = "-"
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
            elif addr.family == psutil.AF_LINK:
                mac = addr.address

        stats = net_if_stats.get(iface)
        status = "UP" if stats.isup else "DOWN"
        speed = stats.speed if stats.speed else "N/A"

        print(f"{iface:<15}{status:<10}{str(speed):<13}{ip:<20}{mac:<20}")

    print("\n📈 I/O Counters:\n")
    print(f"{'Interface':<15}{'RX Bytes':>12}{'TX Bytes':>12}{'RX Errors':>12}{'TX Errors':>12}")
    for iface, counters in net_io_counters.items():
        print(f"{iface:<15}{counters.bytes_recv:>12}{counters.bytes_sent:>12}{counters.errin:>12}{counters.errout:>12}")