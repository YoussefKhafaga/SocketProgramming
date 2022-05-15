import socket
import threading


def parse(header):
    B = header.split()
    method = 0
    url = 0
    payload = 0
    http_version = 0
    if B[0]:
        method = B[0]
    if B[1]:
        url = B[1]
    if B[2]:
        http_version = B[2]
    try:
        payload = B[4]
    except:
        payload = 0
    return method, url, http_version, payload


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
                data = data1.recv(2048)
                # newthread = ClientThread(self.cAddress, self.csocket)
                # newthread.start()

            except socket.timeout:
                print("Server timed out")
                break
            data = data.decode()
            if not data:
                print("No data received")
                break
            method, url, http_version, payload = parse(data.rstrip())
            http_response = ""
            if method == "POST":
                http_response = http_version + " 200 OK\r\n\r\n"
                data1.send(http_response.encode('UTF-8'))

            elif method == "GET":
                try:
                    file = open(url, "r")
                except OSError:
                    found = 0

                if found:
                    http_response = http_version + " 200 OK\r\n"
                    file = file.read()
                    http_response = http_response + file + "\r\n"
                    data1.send(http_response.encode('UTF-8'))
                # print("Connection ended")
                else:
                    http_response = http_version + " 404 Not Found\r\n"
                    data1.send(http_response.encode('UTF-8'))

            if http_version == "HTTP/1.0":
                break
        # print(self.csocket)
        self.csocket.close()
    # print(self.csocket)


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverport = 800
serverSocket.bind(('', serverport))
serverSocket.listen()
print('The server is ready to receive\n')
while True:  # Keep the server running
    data1, address = serverSocket.accept()
    data1.settimeout(10)
    newthread = ClientThread(address, data1)
    newthread.start()
