import subprocess

def visualize_traceroute(host):
    print(f"Traceroute to {host}:")
    result = subprocess.getoutput(f"traceroute -n {host}")
    print(result)