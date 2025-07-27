import subprocess
import platform

def scan_bluetooth():
    print("Scanning for Bluetooth devices...")
    system = platform.system()

    if system == "Darwin":
        try:
            output = subprocess.check_output(["blueutil", "--inquiry"], text=True)
            lines = output.strip().splitlines()
            if lines:
                print("📡 Discovered Bluetooth devices:")
                for line in lines:
                    print(f"🔹 {line}")
            else:
                print("⚠️ No active devices found via inquiry. Checking paired devices...")
                paired = subprocess.check_output(["blueutil", "--paired"], text=True).strip().splitlines()
                if paired:
                    print("🔗 Paired Bluetooth devices:")
                    for line in paired:
                        print(f"🔸 {line}")
                else:
                    print("❌ No Bluetooth devices found.")
        except FileNotFoundError:
            print("❌ 'blueutil' is not installed. Install it with: brew install blueutil")
        except Exception as e:
            print(f"Error: {e}")

    elif system == "Linux":
        try:
            output = subprocess.getoutput("bluetoothctl scan on & sleep 5; bluetoothctl devices")
            print(output)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Unsupported platform.")