import subprocess

def discover_lan_services():
    output = subprocess.getoutput("avahi-browse -a -t")
    print(output)