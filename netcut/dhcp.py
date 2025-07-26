def view_dhcp_leases():
    try:
        with open("/var/lib/dhcp/dhclient.leases") as f:
            leases = f.read()
            print(leases)
    except FileNotFoundError:
        print("DHCP lease file not found.")