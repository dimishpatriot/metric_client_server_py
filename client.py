# client.py
# coursera week 5 (https://www.coursera.org/learn/diving-in-python)
# dimishpatriot@github.com

import socket
import time
import re


class Client:
    EOT = "\n\n"  # end of the correct server transmission

    def __init__(self, ip: str, port: int, timeout: int = None) -> object:
        self.sock = socket.socket()
        self.timeout = timeout  # for future
        try:
            self.sock.connect((ip, port))  # need tuple
        except socket.error as e:
            raise ClientError("Can't connect to the server. Socket error", e)


    def get(self, payload: str) -> dict:
        self._send_data(f"get {payload}\n".encode("utf-8"))
        r = self._recive_data()

        if not self._get_response_is_valid(r):
            raise ClientError("Incorrect GET response")
        else:
            r = r.rstrip().splitlines()

            if len(r) == 1 and r[0] == "ok":
                return dict()  # if data absent on the server, return empty dict
            else:
                params = r[1:]
                params = (tuple(x.split()) for x in params)
                # sort values by timestamp
                params = sorted(params, key=lambda item: item[2])
                return self._fill_dictionary(params)


    def put(self, metric: str, value: float, timestamp: int = None) -> None:
        if metric is None or value is None:
            raise ClientError("Incorrect PUT request")
        if timestamp is None:
            timestamp = int(time.time())
        req = f"{metric} {value} {timestamp}"

        self._send_data(f"put {req}\n".encode("utf-8"))
        r = self._recive_data()

        if not self._put_response_is_valid(r):
            raise ClientError("Incorrect format of the server response")
        else:
            return(None)  # if correct put request


    def _send_data(self, data: str) -> None:
        try:
            self.sock.sendall(data)
        except socket.error as e:
            raise ClientError("Can't send data. Socket error", e)


    def _recive_data(self) -> str:
        response = ""
        while not response.endswith(self.EOT):  # end of the server transmission
            try:
                response += self.sock.recv(1024).decode("utf-8")  # for long data
            except socket.error as e:
                raise ClientError("Can't receive data. Socket error", e)
        return response


    @classmethod
    def _get_response_is_valid(cls, response: str) -> bool:
        if response == f"ok{cls.EOT}":  # if data absent on the server
            return True
        if response == f"error\nwrong command{cls.EOT}":  # if incorrect request
            return False
        if response.startswith("ok\n"):
            data_list = response.lstrip("ok\n").rstrip().splitlines()
            for data in data_list:
                if not re.fullmatch(r"\S{1,} \d{1,}(.\d{1,})? \d{1,}", data):
                    return False
        else:
            return False
        return True


    @classmethod
    def _put_response_is_valid(cls, response: str) -> bool:
        return response == f"ok{cls.EOT}"


    @staticmethod
    def _fill_dictionary(params: tuple) -> dict:
        ans = dict()
        for i in params:
            if i[0] in ans.keys():
                ans[i[0]].append((int(i[2]), float(i[1])))  # multi tuples by key
            else:
                ans[i[0]] = [(int(i[2]), float(i[1]))]
        return ans


class ClientError(Exception):
    pass
