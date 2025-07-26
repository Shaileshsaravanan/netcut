from rich.table import Table
from rich.console import Console
import datetime, json, os

def display_stats():
    with open("data/logs.json", "r") as f:
        logs = json.load(f)

    uptimes = [log["uptime"] for log in logs]
    downtimes = [log["downtime"] for log in logs]
    responses = [log["response_time"] for log in logs]

    avg_uptime = round(sum(uptimes) / len(uptimes), 2)
    longest_downtime = max(downtimes)
    mean_response = round(sum(responses) / len(responses), 2)

    console = Console()
    table = Table(title="Downtime Analytics")

    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold green")

    table.add_row("Average Uptime (%)", str(avg_uptime))
    table.add_row("Longest Downtime (s)", str(longest_downtime))
    table.add_row("Mean Response Time (ms)", str(mean_response))

    console.print(table)