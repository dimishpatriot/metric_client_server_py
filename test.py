"""test.py for the client and server parts
coursera week 5 (https://www.coursera.org/learn/diving-in-python)
dimishpatriot@github.com
"""

import pytest
import subprocess
from client import Client, ClientError
from server import Server


# === PARAM ====================================================================
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
def client():
    return Client(IP, PORT)  # need running server in separate process

@pytest.fixture(scope="session")
def server():
    s = Server(IP, PORT)
    s.memory = memory
    return s

@pytest.fixture(scope="session")
def debug_server():
    return subprocess.Popen("python debug_server.py")


class TestServer:
    # === CONNECTION (UNDER CONSTRUCTION) ======================================
    # @pytest.mark.connection
    # def test_client_creation(self, client):
    #     """for test async run:
    #     pytest test_server.py -k "connection" in same terms
    #     """
    #     for i in range(20):
    #         client.put("hello", i)

    # === SERVER TESTS =========================================================
    @pytest.mark.parametrize('req', good_get_requests)
    def test_request_get_filter_true(self, req):
        res = Server.request_is_correct(req)
        assert res is not False

    @pytest.mark.parametrize('req', good_put_requests)
    def test_request_put_filter_true(self, req):
        res = Server.request_is_correct(req)
        assert res is not False

    @pytest.mark.parametrize('req', bad_get_requests)
    def test_bad_get_request_filter(self, req):
        res = Server.request_is_correct(req)
        assert res is False

    @pytest.mark.parametrize('req', bad_put_requests)
    def test_bad_put_request_filter(self, req):
        res = Server.request_is_correct(req)
        assert res is False

    def test_get_metric_type(self, server):
        result = server.get_metric("palm.cpu")
        assert isinstance(result, str)

    def test_get_metric_is_absent(self, server):
        result = server.get_metric("metric_absent")
        assert result == str()

    def test_get_one_metric_is_present(self, server):
        result = server.get_metric("palm.cpu")
        assert result == "palm.cpu 10 100"

    def test_get_one_metric_multi(self, server):
        result = server.get_metric("palm")
        assert result == "palm 0.1 124\npalm 0.2 125\npalm 0.3 130"

    def test_get_all_metrics(self, server):
        result = server.get_all_metrics()
        assert result == "palm.cpu 10 100\npalm 0.1 124\npalm 0.2 125\npalm 0.3 130\npc.memory 1.0 126\npc.memory 2.0 127"

    def test_get_all_metrics_absent(self, server):
        server.memory = dict()  # empty dict for replace date in the fixture
        result = server.get_all_metrics()
        assert result == ""

    def test_put_new_value(self, server):
        change_to = 99
        server.put(f"palm.cpu {change_to} 100".split())
        new_value = float(server.get_metric("palm.cpu").split()[1])
        assert new_value == change_to

    @pytest.mark.parametrize('req', good_put_requests)
    def test_put_correct_metric(self, server, req):
        server.memory = dict()  # empty dict for replace date in the fixture
        _, *args = req.split()[0:]
        metric, value, timestamp = args
        server.put(args)
        assert (float(value), int(timestamp)) in server.memory[metric]

    def test_update_by_timestamp(self, server):
        server.memory = dict()  # empty dict for replace date in the fixture
        server.put(["cpu", "1", "1000"])  # new tuple
        server.put(["cpu", "1", "3000"])  # new tuple
        server.put(["cpu", "2", "1000"])  # remove by timestamp and append to end
        assert server.memory["cpu"] == [(1, 3000), (2, 1000)]


class TestClient:
    @pytest.mark.connection
    def test_make_server(self, debug_server):
        assert debug_server

    @pytest.mark.connection
    def test_make_client(self, client):
        assert client

    # === GET ==================================================================
    @pytest.mark.get
    def test_get_all(self, debug_server, client):
        resp = client.get("*")
        assert len(resp) == 2, "Incorrect num of results"
        assert len(resp["all.cpu"]) == 2, "Incorrect num of results"
        assert len(resp["eradrum.memory"]) == 1, "Incorrect num of results"
        assert resp["all.cpu"][0][0] < resp["all.cpu"][1][0], "Incorrect range of results"

    @pytest.mark.get
    def test_get_type(self, debug_server, client):
        param = "palm.cpu"
        resp = client.get(f"{param}")
        assert type(resp) is dict

    @pytest.mark.get
    def test_get_correct_value(self, debug_server, client):
        param = "palm.cpu"
        resp = client.get(param)
        assert param in resp.keys()
        assert len(resp[param]) == 1

    @pytest.mark.get
    def test_get_check_param_types(self, debug_server, client):
        param = "palm.cpu"
        resp = client.get(param)
        assert isinstance(resp[param][0][0], int)
        assert isinstance(resp[param][0][1], float)

    @pytest.mark.get
    def test_get_incorrect_server_value(self, debug_server, client):
        param = "incorrect_server.cpu"
        resp = client.get(param)
        assert resp == dict()

    @pytest.mark.get
    def test_get_incorrect_param_value(self, debug_server, client):
        param = "palm.incorrect_param"
        resp = client.get(param)
        assert resp == dict()

    @pytest.mark.get
    def test_get_error_param(self, debug_server, client):
        param = "error"
        with pytest.raises(ClientError):
            client.get(param)

    @pytest.mark.parametrize('i', [x for x in range(1, 7)])
    @pytest.mark.get
    def test_get_error_resr(self, debug_server, client, i):
        param = f"error_resp_{i}"
        with pytest.raises(ClientError):
            client.get(param)

    # === PUT ==================================================================
    @pytest.mark.put
    def test_put_two_param(self, debug_server, client):
        resp = client.put(metric="palm.cpu", value=1)
        assert resp is None

    @pytest.mark.put
    def test_put_three_param(self, debug_server, client):
        resp = client.put(metric="palm.cpu", value=1, timestamp=1000)
        assert resp is None

    @pytest.mark.put
    def test_put_error_param(self, debug_server, client):
        with pytest.raises(ClientError):
            client.put(metric="error", value=None)
# ==============================================================================