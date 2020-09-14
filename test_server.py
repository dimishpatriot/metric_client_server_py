# test_server.py
# coursera week 5 (https://www.coursera.org/learn/diving-in-python)
# dimishpatriot@github.com

from client import Client
from server import Server
import pytest
from threading import Thread
import random
import time


# === SETUP ====================================================================
IP = "127.0.0.1"
PORT = 8888
OK = "ok\n\n"
ERROR = "error\nwrong command\n\n"


# === TEST DATA ================================================================
good_get_requests = ["get *\n", "get palm\n", "get palm.cpu\n"]

good_put_requests = ["put palm 0.1 124\n", "put palm.cpu 1 123\n",
                     "put palm 0.2 125\n", "put key_1 1 1\n"]

bad_get_requests = ["\n", "\n\n", "\n\r", "", " ", "\t",
                    "get", "get\n",
                    "get *", "got *\n",
                    "get palm",
                    "get palm 1\n", "get 1 1\n"]

bad_put_requests = ["put", "put\n",
                    "put 1", "put 1.0",
                    "put 1 1", "put 0 0.1\n",
                    "put put\n", "put 0 0 0 0\n"]

memory = {"palm.cpu": [(10, 100)],
          "palm": [(0.1, 124),
                   (0.2, 125),
                   (0.3, 130)],
          "pc.memory": [(1.0, 126),
                        (2.0, 127)]}


# === FX =======================================================================
@pytest.fixture(scope="session")
def server():
    s = Server(IP, PORT)
    s.memory = memory
    return s


@pytest.fixture(scope="session")
def client():
    return Client(IP, PORT)  # need running server in separate process


# === CONNECTION (UNDER CONSTRUCTION) ==========================================
# @pytest.mark.connection
# def test_server_creation(server):
#     server.start()


@pytest.mark.connection
def test_client_creation(client):
    # for test async run
    # pytest test_server.py -k "connection" in same terms
    for i in range(20):
        client.put("hello", i)
        time.sleep(1)


# === SERVER TESTS =============================================================
@pytest.mark.parametrize('req', good_get_requests)
def test_request_get_filter_true(req):
    res = Server.request_is_correct(req)
    assert res is not False


@pytest.mark.parametrize('req', good_put_requests)
def test_request_put_filter_true(req):
    res = Server.request_is_correct(req)
    assert res is not False


@pytest.mark.parametrize('req', bad_get_requests)
def test_bad_get_request_filter(req):
    res = Server.request_is_correct(req)
    assert res is False


@pytest.mark.parametrize('req', bad_put_requests)
def test_bad_put_request_filter(req):
    res = Server.request_is_correct(req)
    assert res is False


def test_get_metric_type(server):
    result = server.get_metric("palm.cpu")
    assert isinstance(result, str)


def test_get_metric_is_absent(server):
    result = server.get_metric("metric_absent")
    assert result == str()


def test_get_one_metric_is_present(server):
    result = server.get_metric("palm.cpu")
    assert result == "palm.cpu 10 100"


def test_get_one_metric_multi(server):
    result = server.get_metric("palm")
    assert result == "palm 0.1 124\npalm 0.2 125\npalm 0.3 130"


def test_get_all_metrics(server):
    result = server.get_all_metrics()
    assert result == "palm.cpu 10 100\npalm 0.1 124\npalm 0.2 125\npalm 0.3 130\npc.memory 1.0 126\npc.memory 2.0 127"


def test_get_all_metrics_absent(server):
    server.memory = dict()  # empty dict for replace date in the fixture
    result = server.get_all_metrics()
    assert result == ""


def test_put_new_value(server):
    change_to = 99
    server.put(f"palm.cpu {change_to} 100".split())
    new_value = float(server.get_metric("palm.cpu").split()[1])
    assert new_value == change_to


@pytest.mark.parametrize('req', good_put_requests)
def test_put_correct_metric(server, req):
    server.memory = dict()  # empty dict for replace date in the fixture
    _, *args = req.split()[0:]
    metric, value, timestamp = args
    server.put(args)
    assert (float(value), int(timestamp)) in server.memory[metric]


def test_update_by_timestamp(server):
    server.memory = dict()  # empty dict for replace date in the fixture
    server.put(["cpu", "1", "1000"])  # new tuple
    server.put(["cpu", "1", "3000"])  # new tuple
    server.put(["cpu", "2", "1000"])  # remove by timestamp and append to end
    assert server.memory["cpu"] == [(1, 3000), (2, 1000)]
# ==============================================================================
