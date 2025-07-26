import ssl
import socket
from datetime import datetime

def view_cert(host):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
        s.connect((host, 443))
        cert = s.getpeercert()
        print("Subject:", cert.get('subject'))
        print("Issuer:", cert.get('issuer'))
        print("Valid From:", cert.get('notBefore'))
        print("Valid Until:", cert.get('notAfter'))
        print("SANs:", [entry[1] for entry in cert.get('subjectAltName', [])])