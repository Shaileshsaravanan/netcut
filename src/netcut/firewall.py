import subprocess

def list_rules():
    output = subprocess.getoutput("sudo iptables -L")
    print(output)

def add_rule(rule):
    result = subprocess.getoutput(f"sudo iptables {rule}")
    print(result)

def remove_rule(rule):
    result = subprocess.getoutput(f"sudo iptables {rule}")
    print(result)