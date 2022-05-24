import socket
import requests
import cv2
import base64
serverport = 80
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
        if len(words) == 3:
            serverName = words[2]
            httprequest = httprequest + serverName + ":"
        else:
            httprequest = httprequest + serverName + ":"
        if len(words) == 4:
            serverport = words[3]
            httprequest = httprequest + str(serverport) + "\r\n\r\n"
        else:
            httprequest = httprequest + str(serverport) + "\r\n\r\n"

        #print(httprequest)
        # create connection
        try:
            clientSocket.connect((serverName, int(serverport)))
        except ValueError:
            print("Caught exception : ", ValueError)
            quit()

        # post method
        if words[0] == "POST":
            try:
                sentfile = open(words[1], "rb")
            except OSError:
                print("File not found ")
                found = 0
            if found == 1:
                sentfile = sentfile.read()
                filename1 = filename.split(".")
                httprequest1 = httprequest + "\r\n\r\n"
                if filename1[1] != "png":
                    httprequest = httprequest1 + sentfile.decode('utf-8')
                    clientSocket.sendall(bytes(httprequest, 'utf-8'))
                    print(httprequest)
                else:
                    sentfile = base64.b64encode(sentfile)
                    httprequest = httprequest1 + str(sentfile)
                    clientSocket.sendall(bytes(httprequest, 'utf-8'))
                    print(httprequest1)
                print("File sent successfully ")
                data = clientSocket.recv(2048)
                print(data.decode())

        # get method
        if words[0] == "GET":
            clientSocket.send(bytes(httprequest, 'utf-8'))
            print(httprequest)
            data = clientSocket.recv(102400)
            data = data.split(b"\r\n\r\n")
            response = data[0].decode('UTF-8')
            filename1 = filename.split(".")
            res = response
            res1 = response.split(" ")
            if res1[1] == "404":
                print(response)
                quit()
            print(response)
            if filename in cache:
                with open(filename, 'rb') as f:
                    print("File found in cache")
                    if filename1[1] != "png":
                        print(f.read())
                    else:
                        img = cv2.imread(filename)
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
            else:
                print("File not found in cache")
                with open(filename, 'wb') as f:
                    f.write(data[1])
                    cache.update({filename: filename})
                    f = open(filename, 'rb')
                    if filename1[1] != "png":
                        print(data[1].decode())
                    else:
                        img = cv2.imread(filename)
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
        print("---------------------------")
        # clientSocket.close()
