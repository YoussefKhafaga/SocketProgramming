import socket
import cv2

serverport = 80
serverName = "localhost"


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
            httprequest = httprequest + filename + " HTTP/1.0\r\nHOST:"
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

        #create connection
        try:
            clientSocket.connect((serverName, int(serverport)))
        except ValueError:
            print("Caught exception : ", ValueError)
            quit()

        #post method
        if words[0] == "POST":
            try:
                sentfile = open(words[1], "rb")
            except OSError:
                print("File not found ")
                found = 0
            if found == 1:
                sentfile = sentfile.read()
                httprequest = httprequest.encode('UTF-8') + sentfile + "\r\n".encode('UTF-8')
                clientSocket.send(httprequest)
                print(httprequest.decode('UTF-8'))
                print("File sent successfully ")
                data = clientSocket.recv(2048)
                print(data.decode())


        #get method
        if words[0] == "GET":
            clientSocket.send(bytes(httprequest, 'utf-8'))
            data = clientSocket.recv(4096)
            print(data.decode("UTF-8"))
    clientSocket.close()