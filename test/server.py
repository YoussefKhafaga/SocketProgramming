import socket
s = socket.socket()

s.bind(('localhost', 12000))

s.listen(3)

while True:
    c, addr = s.accept()
    name = c.recv(1024).decode()
    print("connected with ",addr, name)

    c.send(bytes('welcome to here ', 'utf-8'))

    c.close