import click
from netcut import mac, process

@click.group()
def cli():
    pass

@cli.command()
@click.argument("app")
@click.option("--for", "duration", help="block duration (e.g. 10s, 5m)")
@click.option("--persist", is_flag=True, help="make block persistent")
@click.option("--dry-run", is_flag=True, help="preview rules only")
def block(app, duration, persist, dry_run):
    pid = process.find_pid(app)
    if not pid:
        print("app not running")
        return
    mac.block_app(app, pid, dry=dry_run)
    if persist:
        mac.persist_block(app)
    if duration:
        secs = parse_duration(duration)
        mac.schedule_unblock(app, secs)

@cli.command()
@click.argument("app", required=False)
@click.option("--all", "unblock_all", is_flag=True)
def unblock(app, unblock_all):
    if unblock_all:
        mac.unblock_all()
    elif app:
        mac.unblock_app(app)
    else:
        print("specify app or use --all")

@cli.command()
def list():
    apps = process.find_all()
    for name, pid in apps.items():
        print(f"{name.lower()} ({pid})")

@cli.command()
@click.argument("app")
def monitor(app):
    print("monitor not yet implemented")

@cli.command()
@click.argument("file")
def export(file):
    mac.export_rules(file)
    print("exported rules")

@cli.command("check-schedule")
def check_schedule():
    mac.check_schedule()

@cli.command("load-persisted")
def load_persisted():
    mac.load_persistent_on_boot()
    print("loaded persistent blocks")

@cli.command("dry-run")
@click.argument("app")
def dry_run(app):
    pid = process.find_pid(app)
    if not pid:
        print("app not running")
        return
    mac.block_app(app, pid, dry=True)

def parse_duration(s):
    units = {"s": 1, "m": 60, "h": 3600}
    for u in units:
        if s.endswith(u):
            return int(s[:-1]) * units[u]
    return int(s)

if __name__ == "__main__":
    cli()