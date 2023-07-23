# Standard Library
import os
import socket
from ipaddress import ip_address
from urllib.parse import urlparse


def validate_port(port: int) -> bool:
    return port in range(1, 65535 + 1)


def is_ip_address(address: str) -> bool:
    try:
        return bool(ip_address(address))
    except ValueError:
        return False


def is_address_valid(address: str) -> bool:
    address_obj = ip_address(address)
    if address_obj.is_private and not os.environ.get("ALLOW_PRIVATE"):
        raise ValueError(
            f"IPv{address_obj.version} address '{address}' does not appear to be public"
        )
    return address_obj.version


def is_valid_hostname(hostname):
    try:
        parsed = urlparse(hostname)
        if parsed.scheme:
            raise ValueError("The hostname must not have a scheme")
    except Exception as ex:
        raise Exception(str(ex))

    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        raise Exception("Hostname does not appear to resolve")


def query_ipv4(address, ports):
    results = []
    for port in ports:
        result = {"port": port, "status": False}
        sock = socket.socket()
        sock.settimeout(1)
        port_check = sock.connect_ex((address, int(port)))
        if port_check == 0:
            result["status"] = True
        sock.close()
        results.append(result)
    return results
