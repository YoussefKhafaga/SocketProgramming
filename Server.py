import socket
serverport = 1200
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverport))
print('The server is ready to receive')
serverSocket.listen(1)
while True:
    data, clientAddress = serverSocket.recvfrom(2048)
    message = data.decode("UTF-8")
    print(message)
    # if "Get" search for the file if found send it else send error not found
    # if "Post"