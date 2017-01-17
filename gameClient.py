#Author: Kyle Anderson "gameClient". Purpose: To be the client's portion of the online multiplayer element to the Ape Over Math game.
import socket, json, tkinter, time
class lobby():
    class playerButton():
        def __init__(self, myName, myPipe):
            print("Button")
            self.button = tkinter.Button(screen, text = str(playerName), command = lambda: request([myName, "Request"], myPipe))
            self.button.pack()
    def __init__(self, screen):
        self.screen = screen
        self.name = "Bob"
        self.pipe = socket.socket() #Make the socket
        self.host = "192.168.9.200"
        self.port = 12345
        self.pipe.connect((self.host, self.port))
        print("Connected")
        self.label = tkinter.Label(self.screen, text = "Connected to Server...")
        self.label.pack()
        self.sendable = json.dumps(["Waiting", self.name])
        self.sendable = self.sendable.encode('utf-8')
        self.pipe.send(self.sendable)
        self.buttons, self.inGame = [], False
        self.timeReg = round(time.time()*1000) #Get the current time for reference later.
    def waiting(self):
        print("Awaiting game")
        while not self.inGame:
            for self.buttonRemover in range(len(self.buttons)): self.buttons[self.buttonRemover].destroy()
            self.update = json.loads((self.pipe.recv(1024)).decode('utf-8'))
            for self.mover in range(len(self.update)):
                self.button = lobby.playerButton(self.update[self.mover], self.pipe)
                self.buttons.append(self.button.button)
            updater([self.name, "Waiting"], self.pipe)
            screen.mainloop()
def updater(statinfo, pipe):
    pipe.send((json.dumps(statinfo)).encode('utf-8'))
    print("Click")
def quit():
    screen.destroy()
    quit()
screen = tkinter.Tk("Game Lobby", None, "Game Lobby")
Lobby = lobby(screen)
screen.protocol("WM_DELETE_WINDOW", quit)
Lobby.waiting()
#screen.after(500, Lobby.waiting())
