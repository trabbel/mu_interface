from subprocess import check_output

def get_ip_address():
    ip = check_output(['hostname', '-I']).decode().strip()
    return ip if ip else '127.0.0.1'
