import subprocess

def scan_bluetooth():
    print("Scanning for Bluetooth devices...")
    output = subprocess.getoutput("bluetoothctl scan on & sleep 5; bluetoothctl devices")
    print(output)