from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .conftest import HEADER_REAL_IP, INVALID_HOST, VALID_DOMAIN


def test_my_ip_endpoint(client, mocker):
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    response = client.get("/api/me")
    assert response.status_code == HTTP_200_OK
    assert response.text == HEADER_REAL_IP
    mock_get_requester.assert_called_once()


def test_get_port_check_endpoint_with_hostname(client, mocker):
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_ipv4 = mocker.patch(
        "app.routes.v2.query_ipv4", return_value=[{"port": 443, "status": True}]
    )
    response = client.get(f"/api/{VALID_DOMAIN}/443")

    assert response.status_code == HTTP_200_OK
    assert response.text == "True"
    mock_get_requester.assert_not_called()
    mock_query_ipv4.assert_called_once_with("example.com", [443])


def test_get_port_check_endpoint_with_me(client, mocker):
    # Use the correct path to mock 'get_requester' and 'query_ipv4'
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_ipv4 = mocker.patch(
        "app.routes.v2.query_ipv4",
        return_value=[{"port": 443, "status": True}],
    )

    # Send the request with the 'me' parameter to trigger get_requester
    response = client.get("/api/me/443")

    # Assertions to ensure function calls and response correctness
    assert response.status_code == HTTP_200_OK
    assert response.text == "True"
    mock_get_requester.assert_called_once()  # Confirm get_requester was called once
    mock_query_ipv4.assert_called_once_with(HEADER_REAL_IP, [443])


def test_query_post_endpoint_v1(client, mocker):
    mock_query_ipv4 = mocker.patch(
        "app.routes.v2.query_ipv4",
        return_value=[{"port": 80, "status": True}, {"port": 443, "status": False}],
    )

    request_data = {"host": VALID_DOMAIN, "ports": [80, 443]}
    response = client.post("/api/v1/query", json=request_data)
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "example.com",
        "check": [{"port": 80, "status": True}, {"port": 443, "status": False}],
    }
    mock_query_ipv4.assert_called_once_with(VALID_DOMAIN, [80, 443])


def test_query_post_endpoint_invalid_port_v1(client):
    # Validate behavior with invalid port,
    # should raise a validation error from APISchema
    request_data = {"host": VALID_DOMAIN, "ports": [80, 70000]}  # Invalid port range

    path = "/api/v1/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"validation error: Validation failed for POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["message"] == "Input should be less than or equal to 65535"


def test_query_post_endpoint_invalid_hostname_v1(client):
    # Validate behavior with invalid hostname,
    # should raise a validation error from APISchema
    request_data = {"host": INVALID_HOST, "ports": [80]}  # Invalid host
    path = "/api/v1/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"validation error: Validation failed for POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "host"
    assert ret["extra"][0]["message"] == "Hostname does not appear to resolve"


def test_query_post_endpoint_v2(client, mocker):
    mock_query_ipv4 = mocker.patch(
        "app.routes.v2.query_ipv4",
        return_value=[{"port": 80, "status": True}, {"port": 443, "status": False}],
    )

    request_data = {"host": VALID_DOMAIN, "ports": [80, 443]}
    response = client.post("/api/query", json=request_data)
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "example.com",
        "check": [{"port": 80, "status": True}, {"port": 443, "status": False}],
    }
    mock_query_ipv4.assert_called_once_with(VALID_DOMAIN, [80, 443])


def test_query_post_endpoint_invalid_port_v2(client):
    # Validate behavior with invalid port,
    # should raise a validation error from APISchema
    request_data = {"host": VALID_DOMAIN, "ports": [80, 70000]}  # Invalid port range

    path = "/api/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"validation error: Validation failed for POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["message"] == "Input should be less than or equal to 65535"


def test_query_post_endpoint_invalid_hostname_v2(client):
    # Validate behavior with invalid hostname,
    # should raise a validation error from APISchema
    request_data = {"host": INVALID_HOST, "ports": [80]}  # Invalid host
    path = "/api/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"validation error: Validation failed for POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "host"
    assert ret["extra"][0]["message"] == "Hostname does not appear to resolve"
