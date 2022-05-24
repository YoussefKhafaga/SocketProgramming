import socket
import threading
from _thread import *
import base64

def parse(header):
    B = header.split()
    length = len(B)
    method = 0
    url = 0
    payload = 0
    http_version = 0
    if length > 1:
        method = B.pop(0)
    if length > 2:
        url = B.pop(0)
    if length > 3:
        http_version = B.pop(0)
    if length > 4:
        B.pop(0)
        payload = " ".join(B)
    return method, url, http_version, payload


def pipelined(c):
    print("Created new thread")
    c.settimeout(10)
    try:
        while True:
            data = c.recv(102400)
            print("This is data ", data)
            if (data):
                start_new_thread(pipelined, (c,))
                print(parse(data))
                response, requestType, filename, httpVersion = parse(data)
                c.sendall(response)
                print()
                break
            if not data:
                print("Client aborted,Closing connection.....")
                c.close()
                return
    except socket.timeout as e:
        # connection closed
        print('Timed Out,Connection closed')
        c.close()


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.cAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        while True:
            found = 1
            try:
                data = data1.recv(102400)

            except socket.timeout:
                print("Server timed out")
                break
            data = data.decode()
            if not data:
                print("No data received")
                break
            start_new_thread(pipelined, (self.csocket,))
            method, url, http_version, payload = parse(data.rstrip())
            http_response = ""
            if method == "POST":
                http_response = http_version + " 200 OK\r\n\r\n"
                data1.send(http_response.encode('UTF-8'))
                filename1 = url.split(".")
                if filename1[1] == "png":
                    payload = payload[1 :].encode("utf-8")
                    payload = base64.b64decode(payload)
                    with open(url, 'wb') as f:
                        f.write(payload)
                else:
                    with open(url, 'wb') as f:
                        f.write(payload.encode('utf-8'))

            elif method == "GET":
                try:
                    file = open(url, "rb")
                except OSError:
                    found = 0

                if found:
                    http_response = http_version + " 200 OK\r\n\r\n"
                    file = file.read()
                    http_response = http_response.encode()
                    http_response = http_response + file
                    data1.send(http_response)
                # print("Connection ended")
                else:
                    http_response = http_version + " 404 Not Found\r\n\r\n"
                    data1.send(http_response.encode('UTF-8'))

            if http_version == "HTTP/1.0":
                break
        # print(self.csocket)
        self.csocket.close()
    # print(self.csocket)


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverport = 80
serverSocket.bind(('', serverport))
serverSocket.listen()
print('The server is ready to receive\n')
while True:  # Keep the server running
    data1, address = serverSocket.accept()
    data1.settimeout(10)
    newthread = ClientThread(address, data1)
    newthread.start()
