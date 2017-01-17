#Server.

import socket, game               # Import socket module
from _thread import * 
def clientWork(conn):
    game.main(1, {"characters": ["elf.png", "darkElf.png", "coolElf.png", "jackElf.png", "purpleElf.png", "summerElf.png"], "creationD": "2017 - 01 - 11 08:35, 3", "name": "neato", "character": "elf.png", "gameMusic": ["Arc - Mind Vortex.wav", "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"], "user": 1, "score": [], "difficulty": 1})

s = socket.socket() # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(s)

s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.
print('Got connection from', addr)
c.send(str.encode('Connected'))
while True:
    start_new_thread(clientWork(c,))
#while True:
#   received = (c.recv(1024)).decode("utf-8")
#   if received == "quit":
#       c.send(str.encode('Closing'))
#       c.close()                # Close the connection
#       break
#   else: c.send(str.encode("Got nothing of good use"))