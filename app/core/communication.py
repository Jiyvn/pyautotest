import platform
import os

import time
import urllib3


def port_in_use(port: int) -> bool:
    cmd = 'lsof -i tcp:' + str(port)
    if platform.system().lower().startswith('windows'):
        cmd = 'netstat -ano | findstr ' + str(port)
    if os.popen(cmd).readline():
        return True
    return False


def get_free_port(port: int, pairs: int = 1, amount_per_pair: int = 1) -> list:
    ports = []
    i = 0
    amount = 0
    while amount < pairs * amount_per_pair:
        if not port_in_use(port):
            amount += 1
            # if pairs == 1:
            #     ports.append(str(port))
            # else:
            if i % amount_per_pair == 0:
                i = 0
                ports.append([])
            ports[-1].append(str(port))
            i += 1
        port += 1
    return ports


def get_state(url):
    conn = urllib3.PoolManager(timeout=1.0)
    res = conn.request('HEAD', f'{url}')
    return res.status


def get_status(url: str):
    import urllib.request
    response = urllib.request.urlopen(url, timeout=5)
    return response.getcode()


def is_valid(url: str):
    try:
        if get_state(url) < 400:
            return True
        return False
    except:
        return False


def wait_for_valid(url: str, timeout: int):
    start_time = time.time()
    while time.time() < start_time + timeout:
        if is_valid(url):
            return True
        time.sleep(1)
    return False

