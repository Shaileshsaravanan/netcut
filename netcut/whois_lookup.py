import whois

def perform_whois(domain):
    w = whois.whois(domain)
    print(f"Domain: {domain}")
    print(f"Registrar: {w.registrar}")
    print(f"Creation Date: {w.creation_date}")
    print(f"Expiration Date: {w.expiration_date}")
    print(f"Name Servers: {w.name_servers}")