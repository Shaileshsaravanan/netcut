import socket

def enumerate_subdomains(domain):
    with open("wordlist.txt") as f:
        subdomains = f.read().splitlines()

    for sub in subdomains:
        try:
            full = f"{sub}.{domain}"
            ip = socket.gethostbyname(full)
            print(f"{full} -> {ip}")
        except:
            continue