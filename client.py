#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345          # Reserve a port for your service.
print(host, s)

s.connect((host, port))
print (s.recv(1024))
#while True:
#    sendable = input("Type something-->")
#    sendable = sendable.encode('utf-8')
#    s.send(sendable)
#    received = (s.recv(1024)).decode('utf-8')
#    if received == "Closing":
#        print("We\'re done here")
#        s.close
#        break
