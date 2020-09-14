# test_client.py
# coursera week 5 (https://www.coursera.org/learn/diving-in-python)
# dimishpatriot@github.com

import pytest
import subprocess
from client import Client, ClientError


@pytest.fixture(scope="session")
def server():
    return subprocess.Popen("python debug_server.py")


@pytest.fixture(scope="session")
def client():
    return Client("127.0.0.1", 8888)


@pytest.mark.connection
def test_make_server(server):
    assert server


@pytest.mark.connection
def test_make_client(client):
    assert client


# ================= GET ===================
@pytest.mark.get
def test_get_all(server, client):
    resp = client.get("*")
    assert len(resp) == 2
    assert len(resp["all.cpu"]) == 2
    assert len(resp["eradrum.memory"]) == 1
    assert resp["all.cpu"][0][0] < resp["all.cpu"][1][0]


@pytest.mark.get
def test_get_type(server, client):
    param = "palm.cpu"
    resp = client.get(f"{param}")
    assert type(resp) is dict


@pytest.mark.get
def test_get_correct_value(server, client):
    param = "palm.cpu"
    resp = client.get(param)
    assert param in resp.keys()
    assert len(resp[param]) == 1


@pytest.mark.get
def test_get_check_param_types(server, client):
    param = "palm.cpu"
    resp = client.get(param)
    assert isinstance(resp[param][0][0], int)
    assert isinstance(resp[param][0][1], float)


@pytest.mark.get
def test_get_incorrect_server_value(server, client):
    param = "incorrect_server.cpu"
    resp = client.get(param)
    assert resp == dict()


@pytest.mark.get
def test_get_incorrect_param_value(server, client):
    param = "palm.incorrect_param"
    resp = client.get(param)
    assert resp == dict()


@pytest.mark.get
def test_get_error_param(server, client):
    param = "error"
    with pytest.raises(ClientError):
        client.get(param)


@pytest.mark.parametrize('i', [x for x in range(1, 7)])
@pytest.mark.get
def test_get_error_resr(server, client, i):
    param = f"error_resp_{i}"
    with pytest.raises(ClientError):
        client.get(param)


# ============== PUT =================
@pytest.mark.put
def test_put_two_param(server, client):
    resp = client.put(metric="palm.cpu", value=1)
    assert resp is None


@pytest.mark.put
def test_put_three_param(server, client):
    resp = client.put(metric="palm.cpu", value=1, timestamp=1000)
    assert resp is None


@pytest.mark.put
def test_put_error_param(server, client):
    with pytest.raises(ClientError):
        client.put(metric="error", value=None)
