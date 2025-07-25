import argparse
import requests
import time
import json
import os
import threading
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.progress import track, Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from urllib.parse import urlparse

CONFIG_FILE = 'urls.txt'
LOG_FILE = 'log.json'
console = Console()

class URLMonitor:
    def __init__(self):
        self.urls = self.load_urls()
        self.statuses = []
        self.lock = threading.Lock()
        self.interval = 10

    def load_urls(self):
        if not os.path.exists(CONFIG_FILE):
            return []
        with open(CONFIG_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def save_urls(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write('\n'.join(self.urls))

    def log_status(self, entry):
        with open(LOG_FILE, 'a') as log:
            log.write(json.dumps(entry) + '\n')

    def add_url(self, url):
        if url not in self.urls:
            self.urls.append(url)
            self.save_urls()
            console.print(f"[green]Added:[/green] {url}")
        else:
            console.print(f"[yellow]Already exists:[/yellow] {url}")

    def remove_url(self, url):
        if url in self.urls:
            self.urls.remove(url)
            self.save_urls()
            console.print(f"[red]Removed:[/red] {url}")
        else:
            console.print(f"[yellow]Not found:[/yellow] {url}")

    def fetch_status(self, url):
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            latency = round((time.time() - start) * 1000, 2)
            return response.status_code, latency, None
        except requests.RequestException as e:
            return 'ERROR', None, str(e)

    def build_table(self):
        table = Table(title="NetCut - Monitoring", box=box.SIMPLE_HEAD, expand=True)
        table.add_column("URL", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Latency (ms)", justify="right")
        table.add_column("Timestamp", style="dim")
        for s in self.statuses:
            url = s['url']
            status = s['status']
            latency = s.get('latency')
            ts = s['timestamp']
            if status == 'ERROR':
                sc = f"[bold red]{status}[/bold red]"
                lt = "-"
            elif 200 <= status < 300:
                sc = f"[bold green]{status}[/bold green]"
                lt = str(latency)
            elif 400 <= status < 500:
                sc = f"[bold yellow]{status}[/bold yellow]"
                lt = str(latency)
            else:
                sc = f"[bold red]{status}[/bold red]"
                lt = str(latency)
            table.add_row(url, sc, lt, ts)
        return table

    def run_check(self):
        with self.lock:
            self.statuses.clear()
            for url in self.urls:
                code, latency, error = self.fetch_status(url)
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                entry = {
                    'url': url,
                    'status': code,
                    'latency': latency,
                    'timestamp': timestamp
                }
                if error:
                    entry['error'] = error
                self.statuses.append(entry)
                self.log_status(entry)

    def live_display(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["header"].update(Align.center(Text("NetCut - Real-Time Monitor", style="bold blue")))
        with Live(layout, refresh_per_second=1, console=console):
            while True:
                self.run_check()
                layout["body"].update(Panel(self.build_table()))
                layout["footer"].update(Align.center(Text(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), style="dim")))
                time.sleep(self.interval)

    def start(self):
        if not self.urls:
            console.print("[red]No URLs to monitor. Add some with 'add <url>'.[/red]")
            return
        self.live_display()

    def clear_logs(self):
        open(LOG_FILE, 'w').close()
        console.print("[blue]Cleared logs.[/blue]")

    def export_logs(self):
        if not os.path.exists(LOG_FILE):
            console.print("[red]Log file not found.[/red]")
            return
        export_file = 'log_export.csv'
        with open(LOG_FILE, 'r') as f, open(export_file, 'w') as out:
            out.write('url,status,latency,timestamp\\n')
            for line in f:
                try:
                    entry = json.loads(line)
                    out.write(f"{entry['url']},{entry['status']},{entry.get('latency', '')},{entry['timestamp']}\\n")
                except:
                    continue
        console.print(f"[green]Exported logs to {export_file}[/green]")

    def prompt_loop(self):
        while True:
            action = Prompt.ask("[bold magenta]netcut[/bold magenta]", choices=["add", "remove", "start", "clear", "export", "exit"])
            if action == "add":
                url = Prompt.ask("Enter URL")
                self.add_url(url)
            elif action == "remove":
                url = Prompt.ask("Enter URL")
                self.remove_url(url)
            elif action == "start":
                self.start()
            elif action == "clear":
                self.clear_logs()
            elif action == "export":
                self.export_logs()
            elif action == "exit":
                console.print("[bold red]Exiting NetCut...[/bold red]")
                break

    def list_urls(self):
        console.print("[bold underline]Tracked URLs:[/bold underline]")
        for url in self.urls:
            parsed = urlparse(url)
            console.print(f"[cyan]{parsed.netloc}[/cyan] → {url}")

    def help_menu(self):
        help_text = Text()
        help_text.append("NetCut Help\n\n", style="bold underline")
        help_text.append("add <url>      ", style="cyan")
        help_text.append("Add a URL to monitor\n")
        help_text.append("remove <url>   ", style="cyan")
        help_text.append("Remove a URL from monitor list\n")
        help_text.append("start          ", style="cyan")
        help_text.append("Begin live monitoring\n")
        help_text.append("clear          ", style="cyan")
        help_text.append("Clear log file\n")
        help_text.append("export         ", style="cyan")
        help_text.append("Export log to CSV\n")
        help_text.append("exit           ", style="cyan")
        help_text.append("Exit NetCut\n")
        panel = Panel(help_text, title="NetCut CLI Help", border_style="blue")
        console.print(panel)

monitor = URLMonitor()

def main():
    parser = argparse.ArgumentParser(description='NetCut - CLI URL Monitor')
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('url')

    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('url')

    parser_start = subparsers.add_parser('start')
    parser_clear = subparsers.add_parser('clear')
    parser_export = subparsers.add_parser('export')
    parser_ui = subparsers.add_parser('ui')
    parser_help = subparsers.add_parser('help')
    parser_list = subparsers.add_parser('list')

    args = parser.parse_args()

    if args.command == 'add':
        monitor.add_url(args.url)
    elif args.command == 'remove':
        monitor.remove_url(args.url)
    elif args.command == 'start':
        monitor.start()
    elif args.command == 'clear':
        monitor.clear_logs()
    elif args.command == 'export':
        monitor.export_logs()
    elif args.command == 'ui':
        monitor.prompt_loop()
    elif args.command == 'list':
        monitor.list_urls()
    elif args.command == 'help':
        monitor.help_menu()
    else:
        console.print("[bold yellow]No command provided. Try 'ui' or 'help'.[/bold yellow]")

if __name__ == '__main__':
    main()