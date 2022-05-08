import socket

serverport = 1200

def server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverport))
    print('The server is ready to receive')
    serverSocket.listen(1)
    while True:
        data, clientAddress = serverSocket.recvfrom(2048)
        message = data.decode("UTF-8")
        print(message)
        #if "Get" search for the file if found send it else send error not found
        #if "Post"



def client():
    serverName = "localhost"
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sentobject = "message"
    clientSocket.sendto(sentobject.encode('UTF-8'), (serverName, serverport))
    data, clientAddress = clientSocket.recvfrom(2048)
    print(data.decode("UTF-8"))
    clientSocket.close()