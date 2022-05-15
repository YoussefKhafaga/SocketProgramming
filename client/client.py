import socket
import requests

serverport = 800
serverName = "localhost"
cache = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    file = open("client.txt", "r")
    for line in file:
        words = line.split()
        found = 1
        httprequest = ""
        if words[0]:
            method = words[0]
            httprequest = httprequest + method + " "
        if words[1]:
            filename = words[1]
            httprequest = httprequest + filename + " HTTP/1.1\r\nHOST:"
        if words[2]:
            serverName = words[2]
            httprequest = httprequest + serverName + ":"
        if words[3]:
            serverport = words[3]
            httprequest = httprequest + serverport + "\r\n\r\n"

        print(httprequest)
        # create connection
        try:
            clientSocket.connect((serverName, int(serverport)))
        except ValueError:
            print("Caught exception : ", ValueError)
            quit()

        # post method
        if words[0] == "POST":
            try:
                sentfile = open(words[1], "r")
            except OSError:
                print("File not found ")
                found = 0
            if found == 1:
                sentfile = sentfile.read()
                httprequest = httprequest + sentfile + "\r\n"
                print(httprequest)
                clientSocket.send(httprequest.encode('UTF-8'))
                print("File sent successfully ")
                data = clientSocket.recv(2048)
                print(data.decode())

        # get method
        if words[0] == "GET":
            clientSocket.send(bytes(httprequest, 'utf-8'))
            data = clientSocket.recv(2048)
            print(data.decode("UTF-8"))

    #clientSocket.close()
