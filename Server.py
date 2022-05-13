import socket
import sys
import threading

import requests


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
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ")
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            found=1
            data = data1.recv(2048).decode()
            # print(data)
            method, url, http_version, payload = parse(data)
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
                else:
                    http_response = http_version + " 404 Not Found\r\n"
                    data1.send(http_response.encode('UTF-8'))
        serverSocket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverport = 80
    serverSocket.bind(('', serverport))
    serverSocket.listen()
    print('The server is ready to receive\n')
    while True:
        data1, address = serverSocket.accept()
        newthread = ClientThread(address, data1)
        newthread.start()
