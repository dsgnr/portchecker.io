"""
Celery tasks
"""
# Standard Library
import socket

# Third Party
from worker import celery_init


@celery_init.task(bind=True)
def port_status(self, hostname, ports):  # pylint: disable=unused-argument
    """
    Attempts to connect to a list of ports on a host and returns the status
    """
    ret = {"host": hostname, "check": []}
    for port in ports:
        result = {"port": port, "status": False}
        sock = socket.socket()
        sock.settimeout(2)
        port_check = sock.connect_ex((hostname, port))
        if port_check == 0:
            result["status"] = True
            ret["check"].append(result)
        else:
            ret["check"].append(result)
        sock.close()
    return ret
