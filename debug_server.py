# debug_server.py
# coursera week 5 (https://www.coursera.org/learn/diving-in-python)
# dimishpatriot@github.com

import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8888))
sock.listen(1)
conn, addr = sock.accept()
print("=== Debug server is start ===\n")

servers = ("palm", "eardrum")
metrtics = ("cpu", "usage", "disk_usage", "network_usage", "memory")

while True:
    data = conn.recv(1024)
    if not data:
        break

    r = data.decode('utf-8')
    method = r.split(' ')[0]
    payload = r.split(' ')[1].rstrip('\n')
    ok = "ok\n\n"
    print(f">>> {method} request: {data}")

    if method == "get":
        if payload == "*":
            response = "ok\nall.cpu 123.1 125\neradrum.memory 0 126\nall.cpu 222.2 124\n\n"

        elif payload == "error":
            response = "error\nwrong command\n\n"
        elif payload == "error_resp_1":
            response = "ok\n123 abc 123\n\n"
        elif payload == "error_resp_2":
            response = "ok\npalm.cpu abc 123\n\n"
        elif payload == "error_resp_3":
            response = "ok\npalm.cpu abc abc\n\n"
        elif payload == "error_resp_4":
            response = "ok\npalm.cpu 123.1 00000000\npalm.cpu a 000001\n\n"
        elif payload == "error_resp_5":
            response = "ok\npalm.cpu 123.1 00000000\npalm.cpu 0 0000.01\n\n"
        elif payload == "error_resp_6":
            response = "ko\npalm.cpu 123.1 00000000\npalm.cpu 0 0000.01\n\n"

        else:
            need_server = payload.split('.')[0]
            need_param = payload.split('.')[1]
            if need_server in servers and need_param in metrtics:
                response = f"ok\n{need_server}.{need_param} 666 999\n\n"
            else:
                response = ok
    elif method == "put":
        if True:
            response = ok
    conn.send(response.encode("utf-8"))
    print(f">>> send response: {response.encode('utf-8')}\n")
conn.close()
