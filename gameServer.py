#Author: Kyle Anderson "GameServer" Purpose: To be the server for the multiplayer element of my ape over math game
import pygame, socket, json, time
from _thread import *
class lobby(): #Make a lobby/manager for games 
    def __init__(self):
        self.gameCount = 0 #No games yet
        self.games, self.queue, self.names = [], [], [] #Will hold all active games and players in queue
        self.timeReg = round(time.time()*1000)
        self.posList, self.requestList = [], [] #Empty list for requests made to players.
    def queuer(self, statinfo, userConn):
        if userConn not in self.queue and statinfo[0] not in self.names: 
            self.queue.append(userConn)
            self.names.append(statinfo[0])
            print(self.names)
        self.sendable = json.dumps(self.names)
        self.sendable = self.sendable.encode('utf-8')
        for self.receiver in range(0, len(self.queue)): #Loop around receiving information
            self.message = json.loads(self.queue[self.receiver].recv(1024).decode('utf-8'))
            if self.message[1] == "Request": 
                self.posList.append(self.names.index(self.message[3]))
                self.requestList.append(self.message[0]) #Request List has the player's position
        for self.updater in range(0, len(self.queue)): #Loop around telling players their options
            if self.updater in self.posList:
                self.queue[self.updater].send(json.dumps(self.requestList[self.posList.index(self.posList[self.updater])]).encode('utf-8')) #Get the name of the person who sent the request

                print("Go to game")
            self.queue[self.updater].send(self.sendable)
            #self.state = json.loads((self.queue[self.updater].recv(1024)).decode('utf-8'))
        #self.gameCount += 1
        #start_new_thread(inGame(p1, p1, ))
class inGame(): #Make the class for what will happen once the users are in game
    def __init__(self, player1, player2):
        pass
    def end(self): #Ends the game
        pass
#connected = [] #Make an empty list to be used later for list of connected users.
handler = lobby()
pipe = socket.socket() #New socket object
host = socket.gethostname()
port = 12345
pipe.bind((host, port))
print(pipe)
pipe.listen(5) #Await a client connection
client, address = pipe.accept() #Connect with the client
#connected.append(client) #Append to connected users list
print(client, address)
while True:
    if round(time.time()*1000) - handler.timeReg >= 500:
        statusInfo = json.loads((client.recv(1024)).decode('utf-8'))
        handler.queuer(statusInfo, client)