#Author: Kyle Anderson "menu" Purpose: To be the menu portion of my ape over math summative program
#data = open("userData.json", "w")
#data.truncate()
#data.close()
import tkinter, time, game, json, importlib, pygame, random
imported = False
from tkinter import messagebox as tkMessageBox
def musicer():
    pygame.mixer.init()
    global backgroundMusic
    backgroundMusic = pygame.mixer.Channel(0)
    musicList = ["dontletmedown.wav", "happy.wav", "magic.wav", "skyfall.wav", "nevergonnagiveyouup.wav"] #Pre set list of music for the lobby
    museSelection = musicList.copy() #Make a copy of this so we don't affect the original.
    for museMaker in range(len(museSelection)):
        num = random.randint(0, len(museSelection) - 1) #So that they play in a different order each time.
        currentQueue= pygame.mixer.Sound("music/Menu/" + str(museSelection[num]))
        backgroundMusic.queue(currentQueue)
        del museSelection[num] #Get rid of it so it does not play more than once.
def mainButtonMaker(infoGather, existingUsers):
    data = open("userData.json", "r+")
    musicer() #Get the tracks rolling
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
        cancelBox = tkinter.Button(infoGather, text = "Cancel", command = lambda: mainButtonMaker(infoGather))
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
    if type(userTicket) != dict: #It will only not be a dictionary if the user
        userTicket[2].destroy()
        user = {'name': userTicket[0], 'user':userTicket[1], 'score': [], 'character': {}, 'creationD': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': 1, 'gameMusic': ["Arc - Mind Vortex.wav", "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"]}
        data.seek(0)
        data.readlines()
        data.write(json.dumps(user) + "\n")
        data.close()
    elif type(userTicket) == dict and userTicket['user'] == "settings1": #This will happen after the user changes their settings
        user = userTicket['oldUser']
        for closer in range(len(userTicket['buttons'])): userTicket['buttons'][closer].grid_forget() #Get rid of all of this stuff.
        user['difficulty'] = userTicket['difficulty']
    elif type(userTicket) == dict and userTicket['user'] == "settings2": #This will happen after the user goes to the settings page and presses cancel.
        for closer in range(len(userTicket['buttons'])): userTicket['buttons'][closer].grid_forget() #Get rid of all of this stuff.
    else: user = userTicket
    print(user['difficulty'])
    playButton = tkinter.Button(screen, text = "Play", command = lambda : playtime(user))
    settingsButton = tkinter.Button(screen, text = "Settings", command = lambda : settings(user, [playButton, outButton, settingsButton]))
    outButton = tkinter.Button(screen, text = "Log Out", command = lambda: restart([settingsButton, outButton, playButton], 0))
    playButton.pack(side = "bottom")
    settingsButton.pack(side = "top")
    outButton.pack(side = "right")
def playtime(user):
    backgroundMusic.pause()
    screen.withdraw()
    #pygame.mixer.quit()
    score = game.main(user['difficulty'], user)
    user['score'].append({'timeStamp': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': user['difficulty'], 'score': score}) #Add the score to the user's score record.
    screen.deiconify()
    pygame.mixer.init() #Initiate this part of pygame again.
    backgroundMusic.unpause()
def settings(user, buttonsToErase):
    for eraser in range(len(buttonsToErase)): buttonsToErase[eraser].pack_forget()
    difficultySet = tkinter.IntVar()
    difSlider = tkinter.Scale(screen, label = "Difficulty", variable = difficultySet, from_ = 1, to = 3)
    deleteButton = tkinter.Button(screen, text = "Erase User Data", command = lambda: restart([difSlider, KButton, cancelButton, deleteButton], 1))
    KButton = tkinter.Button(screen, text = "Submit", command = lambda: dashboard({'difficulty': difficultySet.get(), "oldUser":user, 'user': "settings1", "buttons":[difSlider, KButton, cancelButton, deleteButton]}, data))
    cancelButton = tkinter.Button(screen, text = "Cancel", command = lambda: dashboard({'oldUser':user, 'buttons':[difSlider, KButton, cancelButton, deleteButton], "user": "settings2"}, data))
    cancelButton.grid(column = 0, row = 5)
    difSlider.grid(column = 0, row = 0, rowspan = 4)
    KButton.grid(column = 1, row = 5)
    deleteButton.grid(column = 1, row = 0)
    
def quit(): #Function used to quit
    backgroundMusic.stop()
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
    backgroundMusic.stop()
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
mainButtonMaker(None, existingUsers)
try: 
    if backgroundMusic.get_busy() == False: musicer()  #If it stops playing, re-do the queue.
except NameError: pass
screen.protocol("WM_DELETE_WINDOW", quit)
screen.mainloop() 