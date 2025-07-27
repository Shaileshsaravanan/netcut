import subprocess
import platform

def list_rules():
    system = platform.system()
    if system == "Linux":
        try:
            output = subprocess.check_output(["sudo", "iptables", "-L", "-n"], text=True)
            print(output)
        except Exception as e:
            print(f"Error listing rules: {e}")
    elif system == "Darwin":
        try:
            output = subprocess.check_output(["sudo", "pfctl", "-sr"], text=True)
            print("🔒 macOS Packet Filter Rules (pf):\n")
            if not output.strip():
                print("⚠️ No active firewall rules found.")
            else:
                print(output)
        except Exception as e:
            print(f"Error reading pf rules: {e}")
    else:
        print("Unsupported platform.")