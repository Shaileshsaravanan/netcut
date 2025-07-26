import argparse
from stats import display_stats
from geo import geo_lookup
from statuspage import generate_status_page
from protocols import icmp_ping, tcp_check
from bandwidth import show_bandwidth
from packets import sniff_packets
from portscan import scan_ports
from arp import view_arp_table
from firewall import list_rules, add_rule, remove_rule
from netifaces_viewer import show_interfaces
from ssl_viewer import ssl_cert_info
from subdomains import enumerate_subdomains
from cdn_detect import detect_cdn
from tech_stack import fingerprint_tech
from api_monitor import monitor_api
from wifi_heatmap import export_wifi_heatmap
from bluetooth import scan_bluetooth
from dhcp import view_dhcp_leases
from lan_discovery import discover_lan_services
from proxy_check import check_proxy
from dnsleak import dns_leak_test
from traceroute import visualize_traceroute

parser = argparse.ArgumentParser(prog='netcut', description='Network Utility Tool')
subparsers = parser.add_subparsers(dest='command')

parser_stats = subparsers.add_parser('stats')
parser_geo = subparsers.add_parser('geo')
parser_geo.add_argument('host')
parser_status = subparsers.add_parser('statuspage')
parser_bandwidth = subparsers.add_parser('bandwidth')
parser_sniff = subparsers.add_parser('sniff')
parser_sniff.add_argument('--port')
parser_sniff.add_argument('--proto')
parser_sniff.add_argument('--src')
parser_sniff.add_argument('--dst')
parser_scan = subparsers.add_parser('scan')
parser_scan.add_argument('host')
parser_scan.add_argument('--fast', action='store_true')
parser_arp = subparsers.add_parser('arp')
parser_firewall = subparsers.add_parser('firewall')
parser_firewall.add_argument('--add')
parser_firewall.add_argument('--remove')
parser_netif = subparsers.add_parser('netif')
parser_ssl = subparsers.add_parser('ssl')
parser_ssl.add_argument('host')
parser_subs = subparsers.add_parser('subdomains')
parser_subs.add_argument('domain')
parser_cdn = subparsers.add_parser('cdn')
parser_cdn.add_argument('domain')
parser_fingerprint = subparsers.add_parser('fingerprint')
parser_fingerprint.add_argument('url')
parser_api = subparsers.add_parser('apimon')
parser_api.add_argument('url')
parser_api.add_argument('--header', action='append')
parser_wifi = subparsers.add_parser('wifi')
parser_bluetooth = subparsers.add_parser('bt')
parser_dhcp = subparsers.add_parser('dhcp')
parser_lan = subparsers.add_parser('lan')
parser_proxy = subparsers.add_parser('proxy')
parser_proxy.add_argument('proxy_url')
parser_dns = subparsers.add_parser('dnsleak')
parser_trace = subparsers.add_parser('trace')
parser_trace.add_argument('host')

args = parser.parse_args()

if args.command == 'stats':
    display_stats()
elif args.command == 'geo':
    geo_lookup(args.host)
elif args.command == 'statuspage':
    services = [
        {"name": "Example", "up": icmp_ping("example.com")},
        {"name": "SSH", "up": tcp_check("example.com", 22)}
    ]
    generate_status_page(services)
elif args.command == 'bandwidth':
    show_bandwidth()
elif args.command == 'sniff':
    sniff_packets(args.port, args.proto, args.src, args.dst)
elif args.command == 'scan':
    scan_ports(args.host, args.fast)
elif args.command == 'arp':
    view_arp_table()
elif args.command == 'firewall':
    if args.add:
        add_rule(args.add)
    elif args.remove:
        remove_rule(args.remove)
    else:
        list_rules()
elif args.command == 'netif':
    show_interfaces()
elif args.command == 'ssl':
    ssl_cert_info(args.host)
elif args.command == 'subdomains':
    enumerate_subdomains(args.domain)
elif args.command == 'cdn':
    detect_cdn(args.domain)
elif args.command == 'fingerprint':
    fingerprint_tech(args.url)
elif args.command == 'apimon':
    monitor_api(args.url, args.header)
elif args.command == 'wifi':
    export_wifi_heatmap()
elif args.command == 'bt':
    scan_bluetooth()
elif args.command == 'dhcp':
    view_dhcp_leases()
elif args.command == 'lan':
    discover_lan_services()
elif args.command == 'proxy':
    check_proxy(args.proxy_url)
elif args.command == 'dnsleak':
    dns_leak_test()
elif args.command == 'trace':
    visualize_traceroute(args.host)
else:
    parser.print_help()
