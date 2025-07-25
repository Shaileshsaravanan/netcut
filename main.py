import argparse
import requests
import time
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

CONFIG_FILE = 'urls.txt'
LOG_FILE = 'log.json'
console = Console()

# 
def load_urls():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_urls(urls):
    with open(CONFIG_FILE, 'w') as f:
        f.write('\n'.join(urls))

def log_status(entry):
    with open(LOG_FILE, 'a') as log:
        log.write(json.dumps(entry) + '\n')

def check_url(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start) * 1000, 2)
        return response.status_code, latency, None
    except requests.RequestException as e:
        return 'ERROR', None, str(e)

def build_table(statuses):
    table = Table(title="NetCut - URL Monitor", expand=True)
    table.add_column("URL", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Timestamp", style="dim")

    for status in statuses:
        url = status['url']
        code = status['status']
        latency = status.get('latency')
        timestamp = status['timestamp']

        if code == 'ERROR':
            code_display = f"[bold red]{code}[/bold red]"
            latency_display = "-"
        elif 200 <= code < 300:
            code_display = f"[bold green]{code}[/bold green]"
            latency_display = f"{latency}"
        elif 400 <= code < 500:
            code_display = f"[bold yellow]{code}[/bold yellow]"
            latency_display = f"{latency}"
        else:
            code_display = f"[bold red]{code}[/bold red]"
            latency_display = f"{latency}"

        table.add_row(url, code_display, latency_display, timestamp)
    return table

def monitor_loop(urls):
    statuses = []
    with Live(refresh_per_second=1, console=console) as live:
        while True:
            statuses.clear()
            for url in urls:
                code, latency, error = check_url(url)
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                entry = {
                    'url': url,
                    'status': code,
                    'latency': latency,
                    'timestamp': timestamp
                }
                if error:
                    entry['error'] = error
                statuses.append(entry)
                log_status(entry)

            live.update(Panel(build_table(statuses), title="[bold blue]Netcut Monitoring"))
            time.sleep(10)

def add_url(url):
    urls = load_urls()
    if url in urls:
        console.print("[yellow]URL already in list.[/yellow]")
        return
    urls.append(url)
    save_urls(urls)
    console.print("[green]URL added.[/green]")

def remove_url(url):
    urls = load_urls()
    if url not in urls:
        console.print("[red]URL not found in list.[/red]")
        return
    urls.remove(url)
    save_urls(urls)
    console.print("[green]URL removed.[/green]")

def start_monitoring():
    urls = load_urls()
    if not urls:
        console.print("[red]No URLs to monitor. Add some first.[/red]")
        return
    monitor_loop(urls)

def main():
    parser = argparse.ArgumentParser(description='NetCut - URL Monitor')
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add', help='Add a URL to monitor')
    parser_add.add_argument('url', help='URL to add')

    parser_remove = subparsers.add_parser('remove', help='Remove a URL from monitoring')
    parser_remove.add_argument('url', help='URL to remove')

    subparsers.add_parser('start', help='Start monitoring URLs')

    args = parser.parse_args()

    if args.command == 'add':
        add_url(args.url)
    elif args.command == 'remove':
        remove_url(args.url)
    elif args.command == 'start':
        start_monitoring()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()