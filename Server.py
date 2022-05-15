import socket
import sys
import requests

def parse(header):
    B = header.split()
    length = len(B)
    method = 0
    url = 0
    payload = 0
    http_version = 0
    if B[0]:
        method = B.pop(0)
    if B[1]:
        url = B.pop(0)
    if B[2]:
        http_version = B.pop(0)
    if length > 3:
        B.pop(0)
        payload = " ".join(B)
    return method, url, http_version, payload

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverport = 80
    serverSocket.bind(('', serverport))
    serverSocket.listen()
    print('The server is ready to receive\n')
    while True:
        found = 1
        data1, address = serverSocket.accept()
        data = data1.recv(2048).decode()
        method, url, http_version, payload = parse(data)
        http_response = ""
        if method == "POST":
            http_response = http_version + " 200 OK\r\n\r\n"
            data1.send(http_response.encode('UTF-8'))
            print(payload)

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
            else:
                http_response = http_version + " 404 Not Found\r\n"
                data1.send(http_response.encode('UTF-8'))
    serverSocket.close()
