import socket

#ip 10.42.0.1
s = socket.socket()
host = '10.42.0.1'
print (host)
port = 12345

s.connect((host, port))
print (s.recv(1024))
s.close