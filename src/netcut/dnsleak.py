import dns.resolver

def test_dns_leak():
    resolver = dns.resolver.Resolver()
    print("Detected DNS Servers:")
    for server in resolver.nameservers:
        print(server)