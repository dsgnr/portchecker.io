"""
Flask
"""
# Standard Library
import socket

# Third Party
from flask import Flask, jsonify, request, url_for
from tasks import port_status
from voluptuous import Invalid, Required, Schema
from voluptuous.humanize import validate_with_humanized_errors
from worker import celery_init

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def catch_all():
    """
    Catchall routes that are not defined
    """
    return (
        jsonify({"msg": "Only POST is allowed", "error": True}),
        404,
    )


@app.route("/api", methods=["POST"])
def root():
    """
    Triggers a Celery task for a hostname or IP with a list of provided ports
    """
    base_schema = Schema(
        {
            Required("host"): validate_host,
            Required("ports"): validate_ports,
        },
    )
    try:
        payload = validate_with_humanized_errors(request.get_json(), base_schema)
    except Exception as ex:
        return jsonify({"error": True, "msg": str(ex)}), 400

    ret = {"error": False, "msg": None}
    status_code = 200
    try:
        task_id = port_status.apply_async(args=(payload["host"], payload["ports"])).task_id
        ret["task_id"] = task_id
        ret["bookmark"] = url_for(".task_results", task_id=task_id)
        ret["msg"] = "Task queued..."
    except Exception:
        ret.update({"error": True, "msg": "Unable to start the task"})
        status_code = 400
    return jsonify(ret), status_code


def validate_host(host):
    """
    Validates whether the provided host is a resolvable hostname or IP address
    """
    try:
        return socket.gethostbyname(host)
    except Exception as ex:
        raise Invalid("Host provided is not a valid hostname or IP address", path=["host"]) from ex


def validate_ports(ports):
    """
    Validates whether the ports provided are valid, and whether they're in the range of 1-65535
    """
    try:
        if not isinstance(ports, list):
            raise Exception("Ports must be provided as a list of integers", path=["ports"])
        ports_list = [int(port) for port in ports]
        if all(i >= 1 <= 65535 for i in ports_list):
            return ports_list
        raise Exception("Ports must be within 1-65535")
    except ValueError as noint:
        raise Invalid("Are you sure the ports are integers?", path=["ports"]) from noint
    except Exception as ex:
        raise Invalid(str(ex), path=["ports"]) from ex


@app.route("/api/results/<task_id>")
def task_results(task_id):
    """
    Obtains the task result from the Celery backend
    """
    ret = {"error": False, "msg": None, "results": {}}
    try:
        task = celery_init.AsyncResult(task_id)
        ret["results"] = task.result
    except Exception as ex:
        ret["error"]: True
        ret["msg"] = str(ex)
    return jsonify(ret)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
