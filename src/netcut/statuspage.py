def generate_status_page(services):
    html = "<html><head><title>Status Page</title></head><body><h1>Service Status</h1><ul>"
    for service in services:
        html += f"<li>{service['name']}: <b style='color: {'green' if service['up'] else 'red'}'>{'Up' if service['up'] else 'Down'}</b></li>"
    html += "</ul></body></html>"

    with open("status.html", "w") as f:
        f.write(html)
    print("Generated status.html")