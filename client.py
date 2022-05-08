import socket
serverport = 1200
serverName = "localhost"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    try:
        clientSocket.connect((serverName, serverport))
    except ValueError:
        print("Caught exception : ", ValueError)
        quit()
    file = open("client.txt", "r")
    for line in file:
        words = line.split()
        found = 1
        if words[0] == "POST":
            sentmessage = line
            try:
                sentfile = open(words[1], "r")
            except ValueError:
                print("File not found ")
                found = 0
            clientSocket.sendto(sentmessage.encode('UTF-8'), (serverName, serverport))
            if found == 1:
                clientSocket.sendto(sentfile.encode('UTF-8'), (serverName, serverport))
                print("File sent successfully ")
        if words[0] == "GET":
            sentobject = line
            clientSocket.sendto(sentobject.encode('UTF-8'), (serverName, serverport))
            data, clientAddress = clientSocket.recvfrom(2048)
            print(data.decode("UTF-8"))
    clientSocket.close()