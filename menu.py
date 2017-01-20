#Author: Kyle Anderson "menu" Purpose: To be the menu portion of my ape over math summative program
import tkinter, time, game, json, pygame, random, shutil, os
import tkinter.filedialog as tkFD
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText
imported = False
class musicer():
    def __init__(self): 
        pygame.init()
        pygame.mixer.init()
        self.backgroundMusic = pygame.mixer.Channel(0)
        self.queue, self.museSelection = [], []
        self.files = os.listdir("Music/Menu") #Pre set list of music for the lobby
        for self.adder in range(0, len(self.files)):
            self.name, self.extension = os.path.splitext(self.files[self.adder])
            if self.extension ==".wav": self.museSelection.append(self.files[self.adder]) #Only add the file if it is .wav.
        self.count, self.length = len(self.museSelection), len(self.museSelection) #Need self.count as a counter starting at the total number of files. Self.length will always be that number of files as well.
        for self.museMaker in range(len(self.museSelection)):
            self.num = random.randint(0, len(self.museSelection) - 1) #So that they play in a different order each time.
            self.current= pygame.mixer.Sound("music/Menu/" + str(self.museSelection[self.num]))
            self.queue.append(self.current) #Append the sound to the queue list.
            del self.museSelection[self.num] #Get rid of it so it does not play more than once.
        self.backgroundMusic.play(self.queue[self.count % self.length], 0) #Modulus 5 allows us to get remainders between 0 and 4, which are all numbers on the musicList
    def next(self):
        #if pygame.mixer.get_init() == False: pygame.mixer.init()
        if self.backgroundMusic.get_busy() != False: #Only run this if the channel isn't busy.
            return
        self.count += 1
        self.backgroundMusic.play(self.queue[self.count % 5], 0)
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
        self.image = self.image.subsample(5, 5)
        self.button = tkinter.Button(screen, image = self.image, activebackground = "#00FF00", bg = self.colour, command = lambda: Main.characterSet(self.character))
        self.button.grid(column = column, row = row) #Pack the character onto the screen, with one row of space for the label.
class button(): #Use this to keep track of which button's which.
    def __init__(self, buttonMaker, frame, colour, command, column, row, theFont, text = None):
        self.userNo = buttonMaker
        if command == "register":
            self.userSelection = tkinter.Button(frame, text = text + str(buttonMaker), bg = colour, width = 7, height = 1, justify = "center", activebackground = "#CC6600", 
                                                activeforeground = "#00FF00", command = lambda: Main.register(buttonMaker), font = theFont)
        else: self.userSelection = tkinter.Button(frame, text = text, width = 7, height = 1, activebackground = "#CC6600", activeforeground = "#00FF00", 
                                                command = lambda: Main.goToD(buttonMaker), bg = colour, font = theFont)
        self.userSelection.grid(column = column, row = row, pady = 50, padx = 5)
    def configure(self, colour, command): #A function to configure what the button does
        if command == None: self.userSelection.configure(command = command, bg = colour)
        elif command == "register": self.userSelection.configure(command = lambda: Main.register(self.userNo), bg = colour)
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
        while self.readline != "":
            self.readline = json.loads(self.readline)
            self.existingUsers.append(self.readline['user'])
            self.usernames.append(self.readline['gamertag'])
            self.readline = self.data.readline()
        self.music = musicer() #Get the tracks rolling
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
            #   "Music Import": The user is importing their own music into the game.
            #   "play": The user is preparing to play the game.
            #   "restart": The user just logged in again
            #   "exit": exiting the program.

            if self.state == "Transfer to Main Functions": 
                self.dashboard()
                self.userSelectUpdate()
                self.scoreWriter()
            elif self.state == "restart":
                self.userSelectUpdate()
                self.organiser.select(1)
                self.characterSet(self.user['character']) #Reset the user's character colours
                self.state = "Idle"
            elif self.state == "quit": self.quit()
            elif self.state == "play":
                self.screen.withdraw()
                self.music.stop(self.screen)
                self.score = game.main(self.user['difficulty'], self.user)
                self.user['score'].append({'timeStamp': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': 
                              self.user['difficulty'], 'score': self.score}) #Add the score to the user's score record.
                self.state = "idle"
                self.music.__init__()
                self.screen.deiconify()
            elif self.state == "erase":
                self.userSelectUpdate()
        self.screen.after(50, self.mainloop)
    def userSelect(self): #Make a function for the user to select their user.
        self.row, self.column = 0, 0
        for self.buttonMaker in range(1, 5): #Loop around making the buttons.
            if self.buttonMaker == 2: self.column = 1
            elif self.buttonMaker == 3: self.column, self.row = 0, 1
            elif self.buttonMaker == 4: self.column, self.row = 1, 1
            if self.buttonMaker in self.existingUsers: #If the user already exists
                self.colour = "#00FF00"
                self.text = self.usernames[self.existingUsers.index(self.existingUsers[self.buttonMaker -1 ])] #Get the user's name
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
            self.nameBox.get()
            self.user = {'gamertag': self.nameBox.get(), 'user':userNo, 'score': [], 'character': 'elf.png', 'characters': ['elf.png', 'darkElf.png', 'coolElf.png', 'jackElf.png', 'purpleElf.png', 'summerElf.png'],'creationD': time.strftime("%Y - %m - %d %H:%M, %u"), 'difficulty': 1, 'gameMusic': ["Arc - Mind Vortex.wav", "Be Electric.wav", "Burning.wav", "Etude.wav", "Lightbringer - Far Too Loud.wav", "Rocksteady.wav", "Windwaker.wav"]}
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
        if self.dashboardBool != True: 
            self.state = "Transfer to Main Functions"
            self.dashboardBool = True #We only want to make the dashboard once
        else: self.state = "restart"
    def userSelectUpdate(self):
        for self.updater in range(len(self.buttons)):
            if self.updater + 1 == self.user['user']: 
                self.colour = "#3399ff"
                self.command = None
            elif self.updater + 1 in self.existingUsers: 
                self.colour = "#00FF00"
                self.command = "exists"
            else:
                self.colour = "#717D7E"
                self.command = "register"
            self.buttons[self.updater].configure(self.colour, self.command)
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
        self.fileName = os.path.split(self.newFileLoc)
        MessageBox.showinfo("Success!", "Success! The music will be in your menu music lineup.")
    def register(self, userNo):
        if userNo not in self.existingUsers:
            self.infoGather = tkinter.Tk("Create New User", None, "New User")
            self.okBox = tkinter.Button(self.infoGather, text = "Ok", command = lambda : self.goToD(userNo, self.infoGather))
            self.cancelBox = tkinter.Button(self.infoGather, text = "Cancel", command = lambda: self.revert_settings(self.infoGather, self.existingUsers))
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
    def erase(self): #Function to erase the user's data
        self.state = "erase"
        self.data.seek(0)
        self.users = self.data.readlines()
        self.data.seek(0)
        self.data.truncate()
        for self.userReader in range(len(self.users)): #Loop around deleting the right user
            if json.loads(self.users[self.userReader].replace("\n", ""))['user'] == self.user['user']: del self.users['self.userReader']
            else: self.data.write(self.users[self.userReader])
    def dashboard(self): #This is the function to create the user's dashboard. Will also be responsible for actually creating the user information.
        self.state = "Idle"
        print(self.user['difficulty'])

        #Home Tab Buttons
        self.playButton = tkinter.Button(self.Dashboard, text = "Play", command = self.playtime, bg = "#2874A6", activebackground = "#00FF00", font = self.font)
        #self.outButton = tkinter.Button(self.Dashboard, font = self.font, text = "Log Out", command = lambda: restart([settingsButton, outButton, playButton], 0), bg = "#ff0000", activebackground = "#00FF00")
        #self.outButton.place(relx = 0.1, rely = 0.1)
        self.playButton.place(relx = 0.35, rely = 0.25)
        self.organiser.add(self.Dashboard)
        self.organiser.tab(1, text = "Home")
        self.organiser.select(1)

        #Settings Buttons
        self.charButtons, self.characters = [], [] #This will hold all of the character buttons that there are. The other one will have the actual character names
        self.difficultySet = tkinter.IntVar()
        self.oldUser = self.user.copy() #Make a backup copy of the user in case they want to cancel
        self.characterSpace = tkinter.Frame(self.Settings) #Make a seperate frame for the character icons
        self.column, self.row = -1, -1
        for self.charMaker in range(len(self.user['characters'])): #Make the character buttons
            self.row += 1
            if self.row % 4 == 0: self.column += 1
            self.charButtons.append(charButton(self.characterSpace, self.column, self.row % 4,self.charMaker, self.user))
            self.characters.append(self.user['characters'][self.charMaker])
        self.elvesLabel = tkinter.Label(self.Settings, text = "Choose Your Elf")
        self.difSlider = tkinter.Scale(self.Settings, label = "Difficulty", variable = self.difficultySet, from_ = 1, to = 4)
        self.deleteButton = tkinter.Button(self.Settings, text = "Erase User Data", command = self.erase)
        self.KButton = tkinter.Button(self.Settings, text = "Save", command = lambda: self.settingUpdate(self.difficultySet.get()))
        self.cancelButton = tkinter.Button(self.Settings, text = "Discard", command = lambda: self.settingUpdate(self.oldUser, 1))

        self.importMenu = tkinter.Menubutton(self.Settings, text = "Import...", relief = tkinter.RAISED)
        self.importMenu.menu = tkinter.Menu(self.importMenu)
        self.importMenu['menu'] = self.importMenu.menu
        self.importMenu.menu.add_command(label = "Import Game Music", command = lambda: self.museImporter(2))
        self.importMenu.menu.add_command(label = "Import Menu Music", command = lambda: self.museImporter(1))

        self.importMenu.grid(column = 1, row = 1)
        self.characterSpace.grid(column = 3, row = 1, rowspan = 4, columnspan = 8)
        self.elvesLabel.grid(column = 3, row = 0)
        self.cancelButton.grid(column = 0, row = 5)
        self.difSlider.grid(column = 0, row = 0, rowspan = 4)
        self.KButton.grid(column = 1, row = 5)
        self.deleteButton.grid(column = 1, row = 0)

        self.organiser.add(self.Settings)
        self.organiser.tab(2, text = "Settings")
    def playtime(self):
        self.state = "play"
        
        self.screen.deiconify()
        self.music.__init__() #Resume the music
    def scoreWriter(self, option = 0): #Option 0 means that the buttons do need to be generated.
        if option == 0:
            #self.scroller = tkinter.Scrollbar(self.Scores)
            #self.scroller.place(x = 1115, y = 0, relheight = 1.0)
            self.organiser.add(self.Scores)
            self.organiser.tab(3, text = "View Your Scores")
            self.scoreFont = tkFont.Font(family = "terminal", size = 25)
        elif option == 1: self.scoreList.destroy()
        self.scoreList = ScrolledText.ScrolledText(self.Scores, spacing1 = 10, font = self.scoreFont)
        for self.scorewriter in range(len(self.user['score'])):           
            ##Make tags to be able to edit these later
            #self.timeStamptag = self.scoreList.tag_add("timeStamp", ("%d.%d" % (self.scorewriter, 0)), ("%d.%d" % (self.scorewriter, 1)))
            #self.difficultytag = self.scoreList.tag_add("timeStamp", ("%d.%d" % (self.scorewriter, 1)), ("%d.%d" % (self.scorewriter, 2)))
            #self.scoretag = self.scoreList.tag_add("timeStamp", ("%d.%d" % (self.scorewriter, 2)), ("%d.%d" % (self.scorewriter, 3)))

            #Put the text on
            self.scoreList.insert("timeStamp", ("%d.%d" % (self.scorewriter, 2)) ,str(self.user['score'][self.scorewriter]['score']))
            self.scoreList.insert("timeStamp", ("%d.%d" % (self.scorewriter, 1)), str(self.user['score'][self.scorewriter]['difficulty']))
            self.scoreList.insert("timeStamp", ("%d.%d" % (self.scorewriter, 0)) , self.user['score'][self.scorewriter]['timeStamp'])
        self.scoreList.pack()
        self.scoreList.config(state = tkinter.DISABLED)
    def quitCall(self): 
        self.state = "quit" #Make a function that will just tell the program to quit
    def quit(self): #Function used to quit
        self.data.seek(0)
        self.old = self.data.readlines()
        self.data.seek(0)
        self.data.truncate()
        try: self.readyToWrite = self.user
        except AttributeError: self.readyToWrite = None
        for self.a in range (len(self.old)):
            if self.readyToWrite != None and json.loads(self.old[self.a].replace("\n", ""))['user'] == self.readyToWrite['user']: 
                self.old[self.a] = json.dumps(self.readyToWrite) + "\n"
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
exit = False
screen = tkinter.Tk("Welcome - User Selection", None, "User Selection")
screen.geometry("1200x800")
global Main
Main = main(screen)
screen.protocol("WM_DELETE_WINDOW", Main.quitCall)
screen.after(50, Main.mainloop)
screen.mainloop()