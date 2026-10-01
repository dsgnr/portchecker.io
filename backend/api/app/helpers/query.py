"""
Helper methods for the API
"""

import asyncio
import os
import socket
from ipaddress import ip_address
from urllib.parse import urlparse

from litestar import Request

from app.helpers.exceptions import JsonAPIException

CONNECT_TIMEOUT = 1
MAX_CONCURRENT_CHECKS = 32


def is_ip_address(address: str) -> bool:
    """
    Checks if a given string is a valid IP address (IPv4 or IPv6).

    Attempts to parse the provided address string as an IP address.
    Returns `True` if the address is valid, otherwise `False`.

    Args:
        address (str): The string to check for IP address validity.

    Returns:
        bool: `True` if the string is a valid IP address, `False` if not.
    """
    try:
        return bool(ip_address(address))
    except ValueError:
        return False


def is_address_valid(address: str) -> bool:
    """
    Validates whether a given IP address string is a public IPv4 address.

    Checks if the provided address is a valid IPv4 address. If the address is
    private and the environment variable `ALLOW_PRIVATE` is not set, an error is raised.
    IPv6 addresses are not supported and will raise a `ValueError`.

    Args:
        address (str): The IPv4 address string to validate.

    Returns:
        bool: `True` If the IPv4 address is valid.

    Raises:
        ValueError: If the address is invalid, private, or IPv6.
    """
    if not address:
        raise ValueError("An IPv4 address must be provided")
    address_obj = ip_address(address)
    if address_obj.version == 6:
        raise ValueError("IPv6 is not currently supported")
    if (
        address_obj.is_private
        and os.environ.get("ALLOW_PRIVATE", "false").lower() != "true"
    ):
        raise ValueError(
            f"IPv{address_obj.version} address '{address}' does not appear to be public"
        )
    return True


async def resolve_hostname(hostname: str) -> str:
    """
    Validates the provided hostname is a resolvable, scheme-free domain.

    Resolves the hostname once so every port check can connect to the same
    IPv4 address without repeating the DNS lookup.

    Args:
        hostname (str): The hostname to validate.

    Returns:
        str: The IPv4 address the hostname resolves to.

    Raises:
        ValueError: If the hostname is empty, contains a URL scheme, or fails to resolve.
    """
    if not hostname:
        raise ValueError("A hostname must be provided")
    try:
        if urlparse(hostname).scheme:
            raise ValueError("The hostname must not have a scheme")
    except Exception as ex:
        raise ValueError(str(ex)) from ex

    try:
        addr_info = await asyncio.get_running_loop().getaddrinfo(
            hostname, None, family=socket.AF_INET, type=socket.SOCK_STREAM
        )
    except socket.gaierror as socket_err:
        raise ValueError("Hostname does not appear to resolve") from socket_err
    if not addr_info:
        raise ValueError("Hostname does not appear to resolve")
    return addr_info[0][4][0]


async def _check_port_status(address: str, port: int) -> dict[str, int | bool]:
    """Check if a specific port on the provided address is open.

    Args:
        address (str): The IP address to check.
        port (int): The port to check on the given address.

    Returns:
        dict[str, int | bool]: Returns a dictionary with the port and the connection status.
    """
    loop = asyncio.get_running_loop()
    with socket.socket() as sock:
        sock.setblocking(False)
        try:
            async with asyncio.timeout(CONNECT_TIMEOUT):
                await loop.sock_connect(sock, (address, port))
        except OSError:
            # Covers refused connections, unreachable hosts and timeouts.
            return {"port": port, "status": False}
    return {"port": port, "status": True}


async def check_ports(address: str, ports: list[int]) -> list[dict[str, int | bool]]:
    """Check multiple ports for the provided address concurrently.

    Args:
        address (str): The IPv4 address to query.
        ports (list[int]): List of ports to check on the given address.

    Returns:
        list[dict[str, int | bool]]:
            A list of dictionaries containing the ports checked and their statuses.
    """
    # Explicit type check for ports
    for port in ports:
        if not isinstance(port, int):
            raise TypeError(f"Port '{port}' is not an integer.")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_CHECKS)

    async def _bounded_check(port: int) -> dict[str, int | bool]:
        async with semaphore:
            return await _check_port_status(address, port)

    # gather preserves input order so results line up with the input ports.
    return await asyncio.gather(*(_bounded_check(port) for port in ports))


async def query_address(address: str, ports: list[int]) -> list[dict]:
    """
    Checks whether the specified ports on a given IPv4 address or hostname are connectable.

    This function first validates the `address` as either a public IPv4 address or
    a resolvable hostname. Then attempts to establish a socket connection to each port
    provided in `ports`.

    Args:
        address (str): The hostname or IPv4 address to query.
        ports (list[int]): A list of port numbers to check for connectability.

    Returns:
        list[dict]: A list of dictionaries where each dictionary represents a port and its
                    status, with keys "port" (int) and "status" (bool, `True` if open).

    Raises:
        JsonAPIException: If the `address` is invalid, not public, or cannot be resolved.
    """
    try:
        if is_ip_address(address):
            is_address_valid(address)
            resolved = address
        else:
            resolved = await resolve_hostname(address)
    except Exception as ex:
        raise JsonAPIException(key="host", message=str(ex)) from ex
    return await check_ports(resolved, ports)


def get_requester(request: Request) -> str:
    """
    Extracts the requester's IP address from known headers.

    This function inspects the request headers for common client IP forwarding
    headers, typically added by reverse proxies or load balancers, and retrieves
    the IP address. It checks the following headers in order:
        - `cf-connecting-ip`
        - `do-connecting-ip`
        - `x-real-ip`

    If none of these headers are found, the function raises a `ValueError`.

    Args:
        request (Request): The HTTP request containing headers.

    Returns:
        str: The extracted requester IP address.

    Raises:
        ValueError: If none of the known headers are found in the request.
    """
    known_headers = ["cf-connecting-ip", "do-connecting-ip", "x-real-ip"]
    headers = {**{k.lower(): v for k, v in request.headers.items()}}
    requester = next((headers[key] for key in known_headers if key in headers), None)
    if requester is None:
        raise ValueError("The requester IP was not detected")
    return requester
