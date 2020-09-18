# server.py
# coursera week 5 (https://www.coursera.org/learn/diving-in-python)
# dimishpatriot@github.com

import socket
import re
import selectors


def run_server(host: str, port: int):
    server = Server(host, port)
    server.start()


class Server:
    def __init__(self, host: str, port: int):
        self.memory = dict()
        self.host = host
        self.port = port


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.setblocking(False)
            print(f"\n=== Server on the port {self.port} starts! ===")
            s.listen(5)
            sel = selectors.DefaultSelector()
            sel.register(s, selectors.EVENT_READ)
            while True:
                for key, mask in sel.select():
                    if key.fileobj is s:
                        conn, addr = s.accept()
                        print(f"\n[!] Connect from {addr}")
                        conn.setblocking(False)
                        sel.register(conn, selectors.EVENT_READ)
                    else:
                        conn = key.fileobj
                        try:
                            data = conn.recv(1024)
                        except ConnectionResetError as e:
                            self.close_connection(conn, sel)
                            print(e)
                            break
                        if not data:
                            self.close_connection(conn, sel)
                            break
                        print(f"> Request data: {data} from {conn.getpeername()}")
                        res = self.form_responce(data)
                        print(f"< Responce: {res.encode()}")
                        conn.send(res.encode("utf-8"))


    def close_connection(self, conn, sel):
        print(f"[x] Connection from {conn.getpeername()} is closed!")
        conn.close()
        sel.unregister(conn)


    def form_responce(self, data: str) -> str:
        if self.request_is_correct(data.decode()) is not False:
            command, *args = data.decode().split()[0:]

            if command == "get":
                metric = args[0]
                if metric == "*":
                    result = self.get_all_metrics()
                else:
                    result = self.get_metric(metric)

                res = f"ok\n{result}\n\n"
                if res.endswith("\n\n\n"):  # if result==""
                    res = res[:-1]

            else:  # only put
                self.put(args)
                res = "ok\n\n"
        else:
            res = "error\nwrong command\n\n"
        return res


    def put(self, args: list) -> None:
        metric, value, timestamp = args  # str
        value = float(value)
        timestamp = int(timestamp)

        if metric not in self.memory:
            self.memory[metric] = list()
        else:
            for elem in self.memory[metric]:
                if elem[1] == timestamp:
                    self.memory[metric].remove(elem)
                    self.memory[metric].append((value, timestamp))
                    # print(f"Memory: {self.memory}")
                    return

        self.memory[metric].append((value, timestamp))
        # print(f"Memory: {self.memory}")


    @staticmethod
    def request_is_correct(data: str) -> object or False:
        if len(data) > 0 and not data.isspace():  # check for '\n', '\r', ''
            if data.split()[0] == "get":
                return re.fullmatch(r"get ([*]|\S+)\n", data) or False

            elif data.split()[0] == "put":
                return re.fullmatch(r"put \S+ \d+([.]{1}\d+)* \d+\n", data) or False
        return False


    def get_all_metrics(self) -> str:
        all_data = []
        for m in self.memory.keys():
            all_data.append(self.get_metric(m))
        return "\n".join(all_data)


    def get_metric(self, metric: str) -> str:
        data = []
        if metric in self.memory:
            for value, timestamp in self.memory[metric]:
                data.append(f"{metric} {value} {timestamp}")
        return "\n".join(data)


if __name__ == "__main__":
    server = Server(host="127.0.0.1", port=8888)
    server.start()
