#Author: Kyle Anderson "menu" Purpose: To be the menu portion of my ape over math summative program
import tkinter, time, game, json, pygame, random, shutil, os
import tkinter.filedialog as tkFD
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText
imported = False
class musicer():
    def __init__(self, museList): 
        pygame.init()
        pygame.mixer.init()
        self.museList = museList['list']
        self.backgroundMusic = pygame.mixer.Channel(0)
        self.queue, self.museSelection, self.newFileList = [], [], []
        self.files = os.listdir("Music/Menu") #Pre set list of music for the lobby
        for self.adder in range(0, len(self.files)):
            self.name, self.extension = os.path.splitext(self.files[self.adder])
            if self.extension ==".wav" and self.files[self.adder] in self.museList:  #Conditions: Must be in the folder, must be on the list of music
                self.museSelection.append(self.files[self.adder]) #Only add the file if it is .wav and on the music list
            if self.extension == ".wav": #If it exists but not on the list, delete it.
                self.newFileList.append(self.files[self.adder])
        self.newMuseList = self.museList.copy()
        for self.listRemove in range(0, len(self.museList)):
            if self.museList[self.listRemove] not in self.files: del self.newMuseList[self.listRemove]
        self.museList = self.newMuseList #Forget the old muselist, it is outdated.
        self.count, self.length = len(self.museSelection), len(self.museSelection) #Need self.count as a counter starting at the total number of files. Self.length will always be that number of files as well.
        for self.museMaker in range(len(self.museSelection)):
            self.num = random.randint(0, len(self.museSelection) - 1) #So that they play in a different order each time.
            self.current= pygame.mixer.Sound("music/Menu/" + str(self.museSelection[self.num]))
            self.queue.append(self.current) #Append the sound to the queue list.
            del self.museSelection[self.num] #Get rid of it so it does not play more than once.
        self.backgroundMusic.play(self.queue[self.count % self.length], 0) #Modulus allows us to get remainders between all numbers on the musicList
    def next(self):
        #if pygame.mixer.get_init() == False: pygame.mixer.init()
        if self.backgroundMusic.get_busy() != False: #Only run this if the channel isn't busy.
            return
        self.count += 1
        self.backgroundMusic.play(self.queue[self.count % self.length], 0)
    def stop(self, screen):
        screen.after_cancel(0)
        self.backgroundMusic.stop()
        pygame.mixer.quit()
        pygame.quit()

class charButton():
    def __init__(self, screen, column, row, charNo, user):
        self.character = user['characters'][charNo]
        if self.character == user['character']: self.colour = "#00FF00"
        else: self.colour = "#33ccff"
        self.image = tkinter.PhotoImage(file = "Elves versions/" + self.character)
        self.image = self.image.subsample(3, 3)
        self.button = tkinter.Button(screen, image = self.image, activebackground = "#00FF00", bg = self.colour, command = lambda: Main.characterSet(self.character))
        self.button.grid(column = column, row = row) #Pack the character onto the screen, with one row of space for the label.
class button(): #Use this to keep track of which button's which.
    def __init__(self, buttonMaker, frame, colour, command, column, row, theFont, text = None):
        self.userNo = buttonMaker
        if command == "register":
            self.userSelection = tkinter.Button(frame, text = "User " + str(buttonMaker), bg = colour, width = 7, height = 1, justify = "center", activebackground = "#CC6600", 
                                                activeforeground = "#00FF00", command = lambda: Main.register(buttonMaker), font = theFont)
        else: self.userSelection = tkinter.Button(frame, text = text, width = 7, height = 1, activebackground = "#CC6600", activeforeground = "#00FF00", 
                                                command = lambda: Main.goToD(buttonMaker), bg = colour, font = theFont)
        self.userSelection.grid(column = column, row = row, pady = 50, padx = 5)
    def configure(self, colour, command, name = None): #A function to configure what the button does
        if command == None: self.userSelection.configure(command = command, bg = colour, text = name)
        elif command == "register": self.userSelection.configure(command = lambda: Main.register(self.userNo), bg = colour, text = name)
        else: self.userSelection.configure(command = lambda: Main.goToD(self.userNo), bg = colour)
class main():
    def __init__(self, screen):
        self.usernames = [] #Used to hold the usernames that exist later on.
        self.dashboardBool = False
        self.font = tkFont.Font(family = "timesnewroman", size = 100)
        self.screen = screen
        self.bgImage = tkinter.PhotoImage(file = "jungleHD.png")
        self.bg = tkinter.Label(self.screen, image = self.bgImage)
        self.bg.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.data = open("userData.json", "r+")
        self.state = "Initializing" #The state variable will operate the state of the person throughout the menu navigation
        self.readline, self.existingUsers, self.buttons, self.characterImgs = self.data.readline(), [], [], [] #buttons will be used to get all of the user buttons offscreen.
        if self.readline == "": #Means this is the first time the user is setting this up
            self.data.seek(0)
            self.museList = {'user': 'music', 'list': ["dontletmedown.wav", "happy.wav", "magic.wav", "nevergonnagiveyouup.wav", "skyfall.wav"]} #Will be used to determine what we play later on
            self.data.write(json.dumps(self.museList) + "\n")
            self.data.flush()
        while self.readline != "": #This won't happen if the above did happen.
            self.readline = json.loads(self.readline.replace("\n", ""))
            if self.readline['user'] != "music": 
                self.existingUsers.append(self.readline['user'])
                self.usernames.append(self.readline['gamertag'])
            else: self.museList = self.readline #Load the music playlist from the file
            self.readline = self.data.readline()
        self.music = musicer(self.museList) #Get the tracks rolling
        #screen.after(1000, self.music.next) #Tell tkinter to run this in its mainloop
        self.organiser = ttk.Notebook(self.screen)
        self.userSelection = tkinter.Frame(self.organiser)
        self.Settings, self.Dashboard, self.HelpAbout, self.Scores = tkinter.Frame(self.organiser), tkinter.Frame(self.organiser), tkinter.Frame(self.organiser), tkinter.Frame(self.organiser)
        self.userSelect()
    def mainloop(self):
        self.music.next()
        if self.state != "exit": #Loop around until we need to exit
            #   State index:
            #   "Initializing": The program is initializing (note: no procedure for this one)
            #   "Waiting For User Selection": Waiting for the user to select which user they would like to proceed as
            #   "Transfer to Main Functions": Got past the main log in screen and will go to the main part of the menu
            #   "Idle": The user is on the dashboard, browsing around buttons.
            #   "Menu Music Import": The user is importing their own music to the menu.
            #   "play": The user is preparing to play the game.
            #   "restart": The user just logged in again
            #   "returnGame": The user just returned from playing a game
            #   "eraseAll": The user has initiated a complete wipe of the application
            #   "exit": exiting the program.

            if self.state == "Transfer to Main Functions": 
                self.dashboard()
                self.userSelectUpdate()
                self.museCheckboxer()
                self.scoreWriter()
                self.helpGen()
            elif self.state == "Menu Music Import":
                self.museCheckboxer(1, self.fileName)
                self.state = "idle"
            elif self.state == "restart":
                self.userSelectUpdate()
                self.organiser.add(self.Dashboard)
                self.organiser.add(self.Settings)
                self.organiser.add(self.Scores) #Add the old tabs back on to the screen.
                self.organiser.select(1)
                self.characterSet(self.user['character']) #Reset the user's character colours
                self.scoreWriter(1)
                self.difficultySet.set(self.user['difficulty'])
                self.state = "Idle"
            elif self.state == "quit": self.quit()
            elif self.state == "play":
                self.screen.withdraw()
                self.music.stop(self.screen)
                self.score = game.main(self.oldUser['difficulty'], self.oldUser)
                if self.score != None: #Will be none if user quits pre-maturely
                    self.user['score']['timeStamp'].append(time.strftime("%Y-%m-%d %H:%M"))
                    self.user['score']['difficulty'].append(self.user['difficulty'])
                    self.user['score']['score'].append(self.score) #Add the score to the user's score record.
                self.state = "returnGame"
                self.scoreWriter(1)
                self.music.__init__(self.museList)
                self.screen.deiconify()
            elif self.state == "erase":
                self.existingUsers.remove(self.user['user'])
                self.bgReset(0) #0 to just erase this user's stuff.
                self.user = {'user': None} #No user... Too bad...
                self.userSelectUpdate()
                self.organiser.select(0)
                self.organiser.hide(1)
                self.organiser.hide(2)
                self.organiser.hide(3)
  
            elif self.state == "returnGame":
                self.scoreWriter(1) #1 to tell it not to re-generate buttons
                self.state = "idle" #Go back to being idle once more!
            elif self.state == "eraseAll":
                self.music.stop(self.screen)
                self.data.seek(0)
                self.data.truncate()
                self.data.close()
                self.origMusic = ["dontletmedown.wav", "happy.wav", "skyfall.wav", "nevergonnagiveyouup.wav", "magic.wav"]
                for self.museReset in range(len(self.music.newFileList)): #We need to delete all the non-default music.
                    if self.music.newFileList[self.museReset] not in self.origMusic: os.remove("Music/Menu/" + self.music.newFileList[self.museReset])
                self.origGameMusic = ['Arc - Mind Vortex.wav', "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"]
                self.gameMuseList = os.listdir("Music/In game") #Get a list of all the game music.
                for self.museReset2 in range(len(self.gameMuseList)):
                    if self.gameMuseList[self.museReset2] not in self.origGameMusic: os.remove("Music/In game/" + self.gameMuseList[self.museReset2])
                self.bgReset(1) #1 to delete everything.
                MessageBox.showinfo("Success", "All information deleted. The application will now quit.")
                self.screen.destroy()
                exit()
        self.screen.after(50, self.mainloop)
    def userSelect(self): #Make a function for the user to select their user.
        self.userBackground = tkinter.PhotoImage(file = "jungleLogin.png")
        self.userBackground = tkinter.Label(self.userSelection, image = self.userBackground)
        self.userBackground.place(relwidth = 1, relheight = 1, x = 0, y = 0)
        self.row, self.column = 0, 0
        for self.buttonMaker in range(1, 5): #Loop around making the buttons.
            if self.buttonMaker == 2: self.column = 1
            elif self.buttonMaker == 3: self.column, self.row = 0, 1
            elif self.buttonMaker == 4: self.column, self.row = 1, 1
            if self.buttonMaker in self.existingUsers: #If the user already exists
                self.colour = "#00FF00"
                self.text = self.usernames[self.existingUsers.index(self.buttonMaker)] #Get the user's name
                self.command = "exists"
                self.Button = button(self.buttonMaker, self.userSelection, self.colour, self.command, self.column, self.row, self.font, self.text)
            else: #If the user does not already exist
                self.colour = "#717D7E"
                self.command = "register"
                self.Button = button(self.buttonMaker, self.userSelection, self.colour, self.command, self.column, self.row, self.font)
            self.buttons.append(self.Button)
        self.organiser.add(self.userSelection)
        self.organiser.tab(0, text = "User Selection")
        self.organiser.pack()
        self.state = "Waiting For User Selection"
        return
    def goToD(self, userNo, infoGather = None): #Function will prepare for going to the dashboard
        if infoGather != None:
            self.name = self.nameBox.get()
            if len(self.name) > 12 or len(self.name) < 2:
                MessageBox.showerror("Invalid Length", "Your gamertag must be between 2 and 12 characters.")
                return
            self.user = {'background': "", 'gamertag': self.nameBox.get(), 'user':userNo, 'score': {'score': [], 'difficulty': [], 'timeStamp': []}, 'character': 'elf.png', 'characters': ['elf.png', 'darkElf.png', 'coolElf.png', 'jackElf.png', 'purpleElf.png', 'summerElf.png'],'creationD': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': 1, 'gameMusic': ["Arc - Mind Vortex.wav", "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"]}
            infoGather.destroy()
            self.data.seek(0)
            self.data.readlines()
            self.data.write(json.dumps(self.user) + "\n")
            self.data.flush()
            self.existingUsers.append(userNo)
        else: 
            self.data.seek(0)
            self.readline = self.data.readline()
            while self.readline != "":
                self.readline = json.loads(self.readline)
                if self.readline['user'] == userNo:
                    self.user = self.readline
                    break
                else: self.readline = self.data.readline()
        if self.dashboardBool != True: #Is true when the user is in the dashboard already, so we must make it true when entering it.
            self.state = "Transfer to Main Functions"
            self.dashboardBool = True #We only want to make the dashboard once
        else: self.state = "restart"
    def userSelectUpdate(self):
        for self.updater in range(len(self.buttons)):
            if self.updater + 1 == self.user['user']: 
                self.colour = "#3399ff"
                self.command = None
                self.text = self.user['gamertag']
            elif self.updater + 1 in self.existingUsers: 
                self.colour = "#00FF00"
                self.command = "exists"
                self.text = None
            else:
                self.colour = "#717D7E"
                self.command = "register"
                self.text = "User " + str(self.updater + 1)
            self.buttons[self.updater].configure(self.colour, self.command, self.text)
        if self.state == "erase": self.state = "idle" #Otherwise it will run this continually.
    def bgReset(self, id):
        if id == 1: #Erase all
            self.filesToDelete = os.listdir("Player Background/")
            for self.deleter in range(len(self.filesToDelete)):
                self.name, self.ext = os.path.splitext(self.filesToDelete[self.deleter])
                if self.ext == ".png": os.remove("Player Background/" + self.filesToDelete[self.deleter]) #If it is of .png, remove it.
            self.user['background'] = ""
        elif id == 0: #Erase just one
            os.remove("Player Background/" + self.user['background'])
            self.user['background'] = ""
    def bgImporter(self): #Function to import the background for the game.
        MessageBox.showinfo("Picture Import", "To begin, select a \".png\" file of the dimensions of 2x3.")
        self.imgLoc = tkFD.askopenfilename(title = "Select a .png file.")
        self.imgName, self.imgExtension = os.path.splitext(self.imgLoc) #Making sure that it is .png
        if self.imgExtension != ".png": MessageBox.showerror("Invalid", "The filetype is invalid. Mus be a \".png\" file.")
        else: 
            try:
                if self.user['background'] != "": #Otherwise permission error
                    os.remove("Player Background/" + self.user['background'])
            except PermissionError: #If there are permission issues
                MessageBox.showerror("Operation Failed.", "Access to the folder was denied.")
                return
            try:
                shutil.copy(self.imgLoc, "Player Background/") #Copy to the local player background folder.
            except PermissionError: 
                MessageBox.showerror("Operation Failed.", "Access to the folder was denied.")
                return
            self.dir, self.newImgLoc = os.path.split(self.imgLoc)
            self.user['background'] = self.newImgLoc #Make it accessible by the game program.
            MessageBox.showinfo("Success!", "Success! You will see the new background after you press save.\nIf you press discard, it will be reset.")
    def museImporter(self, id): #id will decide where to add the music
        self.fileLoc = tkFD.askopenfilename(title = "Select Wave Music Files")
        self.name, self.extension = os.path.splitext(self.fileLoc)
        if self.extension != ".wav": 
             MessageBox.showerror("Invalid", "The filetype is invalid. Must be of \".wav\" format.") #Warn the user of what they did.
        elif id == 1: self.museToGame(self.fileLoc) #Send off to the menu music
        elif id == 2: self.museToMenu(self.fileLoc) #Send off to the game music
    def museToGame(self, fileLoc): #A function to send the file to the game music location, if the user so desires
        shutil.copy(fileLoc, "Music/In game/") 
        self.directory, self.fileName = os.path.split(fileLoc)
        self.user['gameMusic'].append(self.fileName)
        MessageBox.showinfo("Success!", "Success! The music will be in your game music lineup.")
    def museToMenu(self, fileLoc): #A function to send the music to the menu folder
        self.newFileLoc = shutil.copy(fileLoc, "Music/Menu/") #Copy the file to the proper location.
        self.dir, self.fileName = os.path.split(self.newFileLoc)
        self.music.newFileList.append(self.fileName)
        self.music.museList.append(self.fileName)
        MessageBox.showinfo("Success!", "Success! The music will be in your menu music lineup \nafter restarting the application.")
        self.state = "Menu Music Import"
    def register(self, userNo):
        if userNo not in self.existingUsers:
            self.infoGather = tkinter.Tk("Create New User", None, "New User")
            self.okBox = tkinter.Button(self.infoGather, text = "Ok", command = lambda : self.goToD(userNo, self.infoGather))
            self.cancelBox = tkinter.Button(self.infoGather, text = "Cancel", command = lambda: self.infoGather.destroy())
            self.nameBox = tkinter.Entry(self.infoGather, bg = "#000000", fg = "#00FF00")
            self.label = tkinter.Label(self.infoGather, text = "Gamertag : ")
            self.label.grid(column = 0, row = 1)
            self.nameBox.grid(column = 1, row = 1)
            self.okBox.grid(column = 2, row = 1)
            self.cancelBox.grid(column = 2, row = 2)
            self.state = "User Creation"
            self.infoGather.mainloop()
    def settingUpdate(self, newUser, type = 0): #Type 1 for when you are reverting to the old user.
        if type == 1: #The cancel button was pressed
            self.user = newUser
            self.oldUser = self.user.copy()
            self.characterSet(self.oldUser['character']) #In case they set their character
            self.museCheckboxer(1) #Reset the checkboxes too!
        elif type == 0:
            self.user['difficulty'] = newUser
            self.data.seek(0)
            self.readline, self.backon = self.data.readline(), []
            while self.readline != "":
                self.readline = json.loads(self.readline)
                if self.readline['user'] == self.user['user']: self.readline = self.user
                self.backon.append(json.dumps(self.readline) + "\n")
                self.readline = self.data.readline()
            self.data.seek(0)
            self.data.truncate()
            for self.reWrite in range(len(self.backon)):
                self.data.write(self.backon[self.reWrite])
            self.data.flush()
            self.oldUser = self.user.copy() #New copy of the old user because of the submitted changes.
            for self.museChanger in range(len(self.music.newFileList)): #Loop around and reset the music options
                if self.varList[self.museChanger].get() == 1 and self.music.newFileList[self.museChanger] not in self.music.museList: 
                    self.music.museList.append(self.music.newFileList[self.museChanger])
                elif self.varList[self.museChanger].get() == 0 and self.music.newFileList[self.museChanger] in self.music.museList:
                    self.music.museList.remove(self.music.newFileList[self.museChanger]) #Get it out of the music listing
            self.museCheckboxer(1) #Update the music checkboxes.
            MessageBox.showinfo("Saved!", "All Settings Saved! Note that changes to music settings will \ntake effect next time you start the application")
        self.difficultySet.set(self.user['difficulty'])
    def erase(self): #Function to erase the user's data
        self.result = MessageBox.askokcancel("Are you sure?", "Erase all of your user data?")
        if not self.result: return #If they press cancel, cancel the erasing.
        self.state = "erase"
        self.data.seek(0)
        self.users = self.data.readlines()
        self.data.seek(0)
        self.data.truncate()
        for self.userReader in range(len(self.users)): #Loop around deleting the right user
            if json.loads(self.users[self.userReader].replace("\n", ""))['user'] == self.user['user']: del self.users[self.userReader]
            else: self.data.write(self.users[self.userReader])
        self.data.flush()
    def eraseAllSetup(self):
        self.result = MessageBox.askokcancel("Are you sure?", "Erase all data, including all users and settings?")
        if self.result : self.state = "eraseAll"
        else: return
    def dashboard(self): #This is the function to create the user's dashboard. Will also be responsible for actually creating the user information.
        self.state = "Idle"
        print(self.user['difficulty'])

        #Home Tab Buttons
        self.playButton = tkinter.Button(self.Dashboard, text = "Play", command = self.playtime, bg = "#2874A6", activebackground = "#00FF00", font = self.font)
        self.quitButton = tkinter.Button(self.Dashboard, text = "Quit", command = self.quit, bg = "red", activebackground = "white", font = self.font)
        #self.outButton = tkinter.Button(self.Dashboard, font = self.font, text = "Log Out", command = lambda: restart([settingsButton, outButton, playButton], 0), bg = "#ff0000", activebackground = "#00FF00")
        #self.outButton.place(relx = 0.1, rely = 0.1)
        self.playButton.place(relx = 0.35, rely = 0.25)
        self.quitButton.place(relx = 0.1, rely = 0.5)
        self.organiser.add(self.Dashboard)
        self.organiser.tab(1, text = "Home")
        self.organiser.select(1)

        #Settings Buttons
        self.settingsFont = tkFont.Font(family = "georgia", size = 20)
        self.charButtons, self.characters = [], [] #This will hold all of the character buttons that there are. The other one will have the actual character names
        self.difficultySet = tkinter.IntVar()
        self.difficultySet.set(self.user['difficulty']) #Make the scrollbar the right difficulty setting to start.
        self.oldUser = self.user.copy() #Make a backup copy of the user in case they want to cancel
        self.characterSpace = tkinter.Frame(self.Settings) #Make a seperate frame for the character icons
        self.column, self.row = -1, -1
        for self.charMaker in range(len(self.user['characters'])): #Make the character buttons
            self.row += 1
            if self.row % 2 == 0: self.column += 1
            self.charButtons.append(charButton(self.characterSpace, self.column, self.row % 2,self.charMaker, self.user))
            self.characters.append(self.user['characters'][self.charMaker])
        self.elvesLabel = tkinter.Label(self.Settings, text = "Choose Your Elf", font = self.settingsFont)
        self.difSlider = tkinter.Scale(self.Settings, label = "Difficulty", variable = self.difficultySet, from_ = 1, to = 4, width = 30, length = 150, font = self.settingsFont, cursor = "hand1", orient = tkinter.HORIZONTAL)
        self.deleteButton = tkinter.Button(self.Settings, text = "Erase User Data", command = self.erase, font = self.settingsFont)
        self.KButton = tkinter.Button(self.Settings, text = "Save", command = lambda: self.settingUpdate(self.difficultySet.get()), font = self.settingsFont)
        self.cancelButton = tkinter.Button(self.Settings, text = "Discard", command = lambda: self.settingUpdate(self.oldUser, 1), font = self.settingsFont)
        self.eraseAllButton = tkinter.Button(self.Settings, text = "Reset Application", command = self.eraseAllSetup, font = self.settingsFont)
        

        self.importMenu = tkinter.Menubutton(self.Settings, text = "Import...", relief = tkinter.RAISED, font = self.settingsFont)
        self.importMenu.menu = tkinter.Menu(self.importMenu)
        self.importMenu['menu'] = self.importMenu.menu
        self.importMenu.menu.add_command(label = "Import Game Music", command = lambda: self.museImporter(1), font = self.settingsFont)
        self.importMenu.menu.add_command(label = "Import Menu Music", command = lambda: self.museImporter(2), font = self.settingsFont)
        self.importMenu.menu.add_command(label = "Import Background Image", command = self.bgImporter, font = self.settingsFont) #Make it possible for the user to import background images.
        self.importMenu.menu.add_command(label = "Reset Background Image", command = lambda: self.bgReset(0), font = self.settingsFont) #Make it possible to reset the background

        self.importMenu.grid(column = 0, row = 0)
        self.characterSpace.grid(column = 4, row = 2, rowspan = 4, columnspan = 8)
        self.elvesLabel.grid(column = 6, row = 0)
        self.cancelButton.grid(column = 0, row = 8)
        self.difSlider.grid(column = 0, row = 2, rowspan = 2, columnspan = 3)
        self.KButton.grid(column = 1, row = 8)
        self.deleteButton.grid(column = 1, row = 0)
        self.eraseAllButton.grid(column = 2, row = 0)

        self.organiser.add(self.Settings)
        self.organiser.tab(2, text = "Settings")
    def museCheckboxer(self, id = 0, newFile = None): #Make a function that will both generate and update the music selection checkboxes in the settings tab. Id 0 for first time generation
        if id == 0: #Make the entire thing new
            self.museSelectButton = tkinter.Menubutton(self.Settings, text = "Music Selection", relief = tkinter.RAISED, font = self.settingsFont)
            self.museSelection = tkinter.Menu(self.museSelectButton)
            self.museSelectButton['menu'] = self.museSelection
            self.varList = [] #Empty list to hold all of the variables later on.
            for self.museChecker in range(len(self.music.newFileList)):
                self.varList.append(tkinter.IntVar())
                self.museSelection.add_checkbutton(label = str(self.music.newFileList[self.museChecker]), font = self.settingsFont, variable = self.varList[self.museChecker])
            self.museSelectButton.grid(column = 1, row = 4)
        if newFile != None: 
            self.variable = tkinter.IntVar()
            self.museSelection.add_checkbutton(label = str(newFile), font = self.settingsFont, variable = self.variable)
            self.varList.append(self.variable)
        for self.museUpdater in range(len(self.music.newFileList)): #Loop around the music file list updating things
            if self.music.newFileList[self.museUpdater] in self.music.museList: self.varList[self.museUpdater].set(1)
            else: self.varList[self.museUpdater].set(0)
    def playtime(self):
        self.state = "play"
        self.screen.deiconify()
    def helpGen(self): #Function to generate the help stuff
        self.aboutTitle = tkinter.Label(self.HelpAbout, text = "About", font = self.settingsFont)
        self.helpTitle = tkinter.Label(self.HelpAbout, text = "Help", font = self.settingsFont)
        self.help = ScrolledText.ScrolledText(self.HelpAbout, width = 85, spacing1 = 10, wrap = tkinter.WORD)
        self.about = ScrolledText.ScrolledText(self.HelpAbout, width = 45, spacing1 = 10, wrap = tkinter.WORD)
        self.help.insert(1.0, "-----Playing the Game-----\n1.Move horizontally using the arrow keys or the \"A\" and \"D\" keys.\n2.You must type in the answer to the question on the barrel closest to you.\n3.You get 2 attempts at doing so.\n4.Once you get it rigt, the text above will go green. Jump over the barrel using \"SPACE\"\n5.You only get one attempt at doing so.\n6.Exit the game using the \"ESCAPE\" key.\n-----Users-----\nYou can have a maximum of 4 users, which you can delete from the settings menu.\nYou can erase all application data from the settings menu.\nEach user can import their own music for the game and select global music for the menu.\nUsers can also customize themselves in the settings menu.")
        self.about.insert(1.0, "Author: Kyle Anderson.\nMusic credit available in \"readme.txt\" file in this directory.\nGame release 1.0")
        self.helpTitle.grid(column = 0, row = 0)
        self.aboutTitle.grid(column = 1, row = 0)
        self.help.grid(column = 0, row = 1)
        self.about.grid(column = 1, row = 1)
        self.organiser.add(self.HelpAbout)
        self.organiser.tab(4, text = "Help/About")
        self.help.config(state = tkinter.DISABLED)
        self.about.config(state = tkinter.DISABLED)
    def scoreWriter(self, option = 0): #Option 0 means that the buttons do need to be generated.
        if option == 0:
            #self.scroller = tkinter.Scrollbar(self.Scores)
            #self.scroller.place(x = 1115, y = 0, relheight = 1.0)
            self.organiser.add(self.Scores)
            self.organiser.tab(3, text = "Scores")
            self.scoreFont = tkFont.Font(family = "terminal", size = 25)
        elif option == 1: 
            self.scoreList.frame.destroy()
            self.scoreList.vbar.destroy()
        self.scoreList = ScrolledText.ScrolledText(self.Scores, spacing1 = 10, font = self.scoreFont, width = 30)
        self.column = 2.0 #Used to determine where to place text later on 
        if len(self.user['score']['score']) <= 0:
            self.scoreList.insert(tkinter.INSERT, "No Score... Get Playing!") #Tell the user they have no score and should start playing.
        else:
            self.scoreList.insert(1.0, "Timestamp--", ("timeHeader",))
            self.scoreList.tag_config("timeHeader", justify = tkinter.LEFT, underline = 1)
            self.scoreList.insert(tkinter.END, "Difficulty--", ("difHeader", ))
            self.scoreList.tag_config("difHeader", justify = tkinter.CENTER, underline = 1)
            self.scoreList.insert("1.end", "Score\n", ("scoreHeader",))
            self.scoreList.tag_config("scoreHeader", justify = tkinter.LEFT, underline = 1)
            self.highScore = max(self.user['score']['score']) #Get the highscore to highlight it later.
            for self.scorewriter in range(len(self.user['score']['score']) -1,  -1 , -1): #Count backwards to display most recent first
                self.column += 1
                #Make tags to be able to edit these later

                #Put the text on
                self.scoreList.insert(self.column ,str(self.user['score']['timeStamp'][self.scorewriter]) + " - ", ("timeStamp" + str(self.scorewriter),)) #Make unique tag
                #self.timeStamptag = self.scoreList.tag_add("timeStamp", self.column, tkinter.END)
                #self.difficultytag = self.scoreList.tag_add("difficulty", "timeStamp.last", tkinter.END)
                self.scoreList.insert(tkinter.END, str(self.user['score']['difficulty'][self.scorewriter]) + " - ", ("difficulty" + str(self.scorewriter),))
                self.scoreList.insert(tkinter.END, str(self.user['score']['score'][self.scorewriter]) + "\n", ("score" + str(self.scorewriter),))
                #self.scoretag = self.scoreList.tag_add("score", "difficulty.last", tkinter.END)
                self.scoreList.tag_config("difficulty", justify = 'center')
                self.scoreList.tag_config("score", justify = 'right')
                if self.user['score']['score'][self.scorewriter] == self.highScore: self.scoreList.tag_config("score" + str(self.scorewriter), background = "#FFFBCC")
        self.scoreList.pack()
        self.scoreList.config(state = tkinter.DISABLED)
    def quitCall(self): 
        self.state = "quit" #Make a function that will just tell the program to quit
    def quit(self): #Function used to quit
        self.data.seek(0)
        self.old = self.data.readlines()
        self.data.seek(0)
        self.data.truncate()
        self.museList['list'] = self.music.museList
        try: self.readyToWrite = self.user
        except AttributeError: self.readyToWrite = None
        for self.a in range (len(self.old)):
            if self.readyToWrite != None and json.loads(self.old[self.a].replace("\n", ""))['user'] == self.readyToWrite['user']: 
                self.old[self.a] = json.dumps(self.readyToWrite) + "\n"
            if json.loads(self.old[self.a].replace("\n", ""))['user'] == "music": self.old[self.a] = json.dumps(self.museList) + "\n" #Re-write the updated music stuff
            self.data.write(self.old[self.a])
        self.data.close()
        self.music.stop(self.screen)
        #self.screen.after_cancel(0)
        self.screen.destroy()
    def characterSet(self, character): #Simple function that will reset the character of the user.
        self.user['character'] = character
        for self.a in range(len(self.characters)):
            if self.characters[self.a] == self.user['character']: self.charButtons[self.a].button.configure(bg = "#00FF00")
            else: self.charButtons[self.a].button.configure(bg = "#66ccff")

data = open("userData.json", "r+")
data.close()
screen = tkinter.Tk("Ape Over Math", None, " Ape Over Math")
screen.geometry("1200x800")
global Main
Main = main(screen)
screen.protocol("WM_DELETE_WINDOW", Main.quitCall)
screen.after(50, Main.mainloop)
screen.mainloop()