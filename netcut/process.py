import psutil

def normalize(name):
    return name.lower().split(".app")[0]

def find_pid(app_name):
    target = normalize(app_name)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = normalize(proc.info['name'])
            if target in pname:
                return proc.info['pid']
        except Exception:
            continue
    return None

def is_running(app_name):
    return find_pid(app_name) is not None

def find_all():
    found = {}
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            conns = proc.connections(kind='inet')
            if conns:
                found[proc.info['name']] = proc.info['pid']
        except Exception:
            continue
    return found

def list_ports(pid):
    ports = set()
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.pid == pid and conn.laddr:
                ports.add(conn.laddr.port)
    except Exception:
        pass
    return list(ports)