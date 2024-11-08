from litestar.status_codes import HTTP_200_OK


def test_route_health_check(client):
    response = client.get("/healthz")
    assert response.status_code == HTTP_200_OK
    assert response.text == "true"
