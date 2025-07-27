import subprocess
import platform

def discover_lan_services():
    system = platform.system()
    if system == "Linux":
        try:
            print("🔍 Running: avahi-browse -a -t")
            output = subprocess.check_output(["avahi-browse", "-a", "-t"], text=True)
            print(output)
            print("✅ avahi-browse completed.")
        except FileNotFoundError:
            print("❌ avahi-browse not found. Install with: sudo apt install avahi-utils")
        except Exception as e:
            print(f"Error: {e}")
    elif system == "Darwin":
        try:
            print("🔍 Running: dns-sd -B _services._dns-sd._udp")
            output = subprocess.check_output(["dns-sd", "-B", "_services._dns-sd._udp"], text=True)
            print(output)
            print("✅ dns-sd completed.")
        except FileNotFoundError:
            print("❌ dns-sd not found on this system.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Unsupported platform for LAN discovery.")