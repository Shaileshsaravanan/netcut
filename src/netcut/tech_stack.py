import requests
from bs4 import BeautifulSoup

def fingerprint_tech(url):
    r = requests.get(url)
    server = r.headers.get('Server', 'Unknown')
    x_powered_by = r.headers.get('X-Powered-By', 'Unknown')

    soup = BeautifulSoup(r.text, 'html.parser')
    scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
    styles = [s.get('href') for s in soup.find_all('link') if s.get('href')]

    print("Server:", server)
    print("X-Powered-By:", x_powered_by)
    print("Scripts:", scripts)
    print("Stylesheets:", styles)