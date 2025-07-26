import dns.resolver

def dns_leak_test():
    resolver = dns.resolver.Resolver()
    print("Detected DNS Servers:")
    for server in resolver.nameservers:
        print(server)