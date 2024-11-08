# Standard Library
import os
import socket
from ipaddress import ip_address
from urllib.parse import urlparse

# Third Party
from litestar import Request


def validate_port(port: int) -> bool:
    return port in range(1, 65535 + 1)


def is_ip_address(address: str) -> bool:
    try:
        return bool(ip_address(address))
    except ValueError:
        return False


def is_address_valid(address: str) -> bool:
    if not address:
        raise ValueError("An IPv4 address must be provided")
    address_obj = ip_address(address)
    if address_obj.is_private and not os.environ.get("ALLOW_PRIVATE"):
        raise ValueError(
            f"IPv{address_obj.version} address '{address}' does not appear to be public"
        )
    return address_obj.version


def is_valid_hostname(hostname: str) -> bool:
    if not hostname:
        raise ValueError("A hostname must be provided")
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


def get_requester(request: Request) -> str:
    known_headers = ["cf-connecting-ip", "do-connecting-ip", "x-real-ip"]
    headers = {**{k.lower(): v for k, v in request.headers.items()}}
    requester = next((headers[key] for key in known_headers if key in headers), None)
    if requester is None:
        raise ValueError("The requester IP was not detected")
    return requester
