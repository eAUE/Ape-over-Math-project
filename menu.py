#Author: Kyle Anderson "menu" Purpose: To be the menu portion of my ape over math summative program
#data = open("userData.json", "w")
#data.truncate()
#data.close()
import tkinter, time, game, json, importlib, pygame, random
imported = False
from tkinter import messagebox as tkMessageBox
class musicer():
    def __init__(self): 
        pygame.mixer.init()
        self.backgroundMusic = pygame.mixer.Channel(0)
        self.queue, self.count = [], 5
        self.museSelection = ["dontletmedown.wav", "happy.wav", "magic.wav", "skyfall.wav", "nevergonnagiveyouup.wav"] #Pre set list of music for the lobby
        for self.museMaker in range(len(self.museSelection)):
            self.num = random.randint(0, len(self.museSelection) - 1) #So that they play in a different order each time.
            self.current= pygame.mixer.Sound("music/Menu/" + str(self.museSelection[self.num]))
            self.queue.append(self.current) #Append the sound to the queue list.
            del self.museSelection[self.num] #Get rid of it so it does not play more than once.
        self.backgroundMusic.play(self.queue[self.count % 5], 0) #Modulus 5 allows us to get remainders between 0 and 4, which are all numbers on the musicList
    def next(self):
        if pygame.mixer.get_init() == False: pygame.mixer.init()
        if self.backgroundMusic.get_busy() != False: #Only run this if the channel isn't busy.
            screen.after(1000, music.next)
            return
        self.count += 1
        self.backgroundMusic.play(self.queue[self.count % 5], 0)
        screen.after(1000, music.next)
class charButton():
    def __init__(self, screen, row, column, charNo):
        self.character = user['characters'][charNo]
        self.image = tkinter.PhotoImage(file = "Elves versions/" + self.character)
        self.image = self.image.subsample(5, 5)
        self.button = tkinter.Button(screen, image = self.image, command = lambda: characterSet(self.character))
        self.button.grid(column = column, row = row) #Pack the character onto the screen, with one row of space for the label.
def mainButtonMaker(infoGather, existingUsers):
    data = open("userData.json", "r+")
    if infoGather != None: infoGather.destroy()
    for buttonMaker in range(1, 5): #Loop around making the buttons.
        if buttonMaker in existingUsers: colour = "#00FF00"
        else: colour = "#717D7E"
        Button = button(buttonMaker, screen, colour, data)
        buttons.append(Button)
class button(): #Use this to keep track of which button's which.
    def __init__(self, buttonMaker, screen, colour, data):
        self.userSelection = tkinter.Button(screen, text = "User " + str(buttonMaker), bg = colour, width = 10, justify = "center", activebackground = "#CC6600", command = lambda: login(buttonMaker, data))
        self.userSelection.pack()
def login(userNo, data):
    for a in range(0, len(buttons)): buttons[a].userSelection.pack_forget()
    if userNo not in existingUsers:
        infoGather = tkinter.Tk("Create New User", None, "New User")
        okBox = tkinter.Button(infoGather, text = "Ok", command = lambda : dashboard([nameBox.get(), userNo, infoGather], data))
        cancelBox = tkinter.Button(infoGather, text = "Cancel", command = lambda: mainButtonMaker(infoGather, existingUsers))
        nameBox = tkinter.Entry(infoGather, bg = "#000000", fg = "#00FF00")
        label = tkinter.Label(infoGather, text = "Your Name : ")
        label.grid(column = 0, row = 1)
        nameBox.grid(column = 1, row = 1)
        okBox.grid(column = 2, row = 1)
        cancelBox.grid(column = 2, row = 2)
        #okBox.pack(side = "bottom")
        #cancelBox.pack(side = "bottom")
        infoGather.mainloop()
    else: 
        data.seek(0)
        found = False
        readline = data.readline()
        while readline != "":
            readline = json.loads(readline)
            if readline['user'] == userNo:
                dashboard(readline, data)
                break
            else: readline = data.readline()
def dashboard(userTicket, data): #This is the function to create the user's dashboard. Will also be responsible for actually creating the user information.
    global user
    if type(userTicket) != dict: #It will only not be a dictionary if the user is signing up for the first time
        userTicket[2].destroy()
        user = {'name': userTicket[0], 'user':userTicket[1], 'score': [], 'character': 'elf.png', 'characters': ['elf.png', 'darkElf.png', 'coolElf.png', 'jackElf.png', 'purpleElf.png', 'summerElf.png'],'creationD': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': 1, 'gameMusic': ["Arc - Mind Vortex.wav", "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"]}
        data.seek(0)
        data.readlines()
        data.write(json.dumps(user) + "\n")
        data.close()
    elif type(userTicket) == dict and userTicket['user'] == "settings1": #This will happen after the user changes their settings
        user = userTicket['oldUser']
        for closer in range(len(userTicket['buttons']) -1): userTicket['buttons'][closer].grid_forget() #Get rid of all of this stuff.
        for closer2 in range(len(userTicket['buttons'][-1])): userTicket['buttons'][-1][closer2].button.grid_forget() #Get rid of the character buttons too.
        user['difficulty'] = userTicket['difficulty']
    elif type(userTicket) == dict and userTicket['user'] == "settings2": #This will happen after the user goes to the settings page and presses cancel.
        for closer in range(len(userTicket['buttons']) -1): userTicket['buttons'][closer].grid_forget() #Get rid of all of this stuff.
        for closer2 in range(len(userTicket['buttons'][-1])): userTicket['buttons'][-1][closer2].button.grid_forget() #Get rid of the character buttons too.
    else: user = userTicket
    print(user['difficulty'])
    playButton = tkinter.Button(screen, text = "Play", command = lambda : playtime(user))
    settingsButton = tkinter.Button(screen, text = "Settings", command = lambda : settings(user, [playButton, outButton, settingsButton]))
    outButton = tkinter.Button(screen, text = "Log Out", command = lambda: restart([settingsButton, outButton, playButton], 0))
    playButton.pack(side = "bottom")
    settingsButton.pack(side = "top")
    outButton.pack(side = "right")
def characterSet(character): #Simple function that will reset the character of the user.
    user['character'] = character
def playtime(user):
    music.backgroundMusic.stop()
    pygame.mixer.quit()
    screen.withdraw()
    #pygame.mixer.quit()
    score = game.main(user['difficulty'], user)
    user['score'].append({'timeStamp': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': user['difficulty'], 'score': score}) #Add the score to the user's score record.
    screen.deiconify()
    music.__init__() #Restart the music
    screen.after(1000, music.next)
def settings(user, buttonsToErase):
    for eraser in range(len(buttonsToErase)): buttonsToErase[eraser].pack_forget()
    charList = [] #Empty list that will hold all the character buttons that I must erase.
    row, column = 1, 3 #Set the row and column for the character pictures.
    for charMaker in range(len(user['characters'])):
        charbutton = charButton(screen, row, column, charMaker)
        charList.append(charbutton)
        row += 1 #Add to the number of rows we have.
        if (row - 1) %4 == 0: row, column = 1, column + 1 #We want 4 pictures per column
    oldUser = user.copy() #Make a copy of this now in case the user decides to quit
    elvesLabel = tkinter.Label(screen, text = "Choose your elf...")
    difficultySet = tkinter.IntVar()
    difSlider = tkinter.Scale(screen, label = "Difficulty", variable = difficultySet, from_ = 1, to = 3)
    deleteButton = tkinter.Button(screen, text = "Erase User Data", command = lambda: restart([difSlider, KButton, cancelButton, deleteButton], 1))
    KButton = tkinter.Button(screen, text = "Submit", command = lambda: dashboard({'difficulty': difficultySet.get(), "oldUser": user, 'user': "settings1", "buttons":[difSlider, KButton, cancelButton, deleteButton, elvesLabel, charList]}, data))
    cancelButton = tkinter.Button(screen, text = "Cancel", command = lambda: dashboard({'oldUser': oldUser, 'buttons':[difSlider, KButton, cancelButton, deleteButton, elvesLabel, charList], "user": "settings2"}, data))
    elvesLabel.grid(column = 3, row = 0)
    cancelButton.grid(column = 0, row = 5)
    difSlider.grid(column = 0, row = 0, rowspan = 4)
    KButton.grid(column = 1, row = 5)
    deleteButton.grid(column = 1, row = 0)
    
def quit(): #Function used to quit
    music.backgroundMusic.stop()
    data = open("userData.json", "r+")
    data.seek(0)
    old = data.readlines()
    data.seek(0)
    data.truncate()
    try: readyToWrite = user
    except NameError: readyToWrite = None
    for a in range (len(old)):
        if readyToWrite != None and json.loads(old[a].replace("\n", ""))['user'] == readyToWrite['user']: old[a] = json.dumps(readyToWrite) + "\n"
        data.write(old[a])
    data.close()
    screen.destroy()
def restart(buttonsToErase, function):
    music.backgroundMusic.stop()
    data = open("userData.json", "r+")
    for eraser in range(len(buttonsToErase)): #Sometimes (if the user is coming from the dashboard) a pack will be used, other times (the settings) a grid is used.
        if function == 0: 
            buttonsToErase[eraser].pack_forget()
        else:
            buttonsToErase[eraser].grid_forget()
    if user['user'] not in existingUsers: existingUsers.append(user['user'])
    data.seek(0)
    old = data.readlines()
    data.seek(0)
    data.truncate()
    try: readyToWrite = user
    except NameError: readyToWrite = None
    for a in range (len(old)):
        if readyToWrite != None and json.loads(old[a].replace("\n", ""))['user'] == readyToWrite['user'] and function == 1: 
            del old[a]
            userLoc = existingUsers.index(readyToWrite['user'])
            del existingUsers[userLoc]
        elif readyToWrite != None and json.loads(old[a].replace("\n", ""))['user'] == readyToWrite['user']: 
            old[a] = json.dumps(readyToWrite) + "\n"
            data.write(old[a])
    pygame.mixer.quit() #Quit the mixer to allow it to initialize again properly.
    mainButtonMaker(None, existingUsers)
screen = tkinter.Tk("Welcome - User Selection", None, "User Selection")
data = open("userData.json", "r+")
readline, existingUsers, buttons = data.readline(), [], [] #buttons will be used to get all of the user buttons offscreen.
while readline != "":
    readline = json.loads(readline)
    existingUsers.append(readline['user'])
    readline = data.readline()
data.close()
music = musicer() #Get the tracks rolling
mainButtonMaker(None, existingUsers)
screen.after(1000, music.next) #Tell tkinter to run this in its mainloop
screen.protocol("WM_DELETE_WINDOW", quit)
screen.mainloop() 