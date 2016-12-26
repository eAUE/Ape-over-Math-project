import math, time, random, pygame #Import some modules
from pygame.locals import *
clock = pygame.time.Clock()
class Barrel(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.image = pygame.image.load("Barrel.png") #Load the image
        self.image.convert() #Convert it
        self.image.set_colorkey((255, 255, 255)) #Set the background stuff
        self.image = pygame.transform.scale(self.image, (90, 90))#Scale it proeperly
        self.rect = self.image.get_rect() #Get the rectangle.
        self.imageExpendable = self.image.copy()
        self.font = pygame.font.Font(None, 20) #Get the font ready
        self.displayText = self.font.render( text, 1, (255, 255, 255)) #Render text
        self.textPos = self.displayText.get_rect() #Set up for placing the text in the centre.
        self.textPos.center = self.rect.center #Place the font in the centre.
        self.image.blit(self.displayText, self.textPos) #Put the font on the image.
        self.rect.move_ip(50, 650) #Move the rectangle to the proper locations.
    def roll(self):
        self.image = self.imageExpendable.copy() #Get a brand new barrel to blit the text to so that it is not upside down or sideways, etc.
        self.rect = self.rect.move(1, 0)#Move the barrel to the right
        self.image = pygame.transform.rotate(self.image, -90) #Rotate the barrel clockwise 90 degrees
        self.imageExpendable = pygame.transform.rotate(self.imageExpendable, -90) #Duplicate the step above with the copiable barrel
        self.image.blit(self.displayText, self.textPos) #Put the text onto the image.
def box(screen, text, correct, oldTextPos): #Make this function to draw the box for the input.
    if oldTextPos != None: screen.fill((0,0 ,0), oldTextPos) #Get rid of what is there
    font = pygame.font.Font(None, 22) #Get font variable
    green, red, white = (0, 255, 0), (255, 0, 0), (255, 255, 255) #Make some colours.
    if correct == False: displayText = font.render(text, 1, red)
    elif correct == True: displayText = font.render(text, 1, green)
    elif correct == None: displayText = font.render(text, 1, white)
    textpos = displayText.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_height()/5
    screen.blit(displayText, textpos)
    pygame.display.flip()
    return textpos
def keyer(): #Make a function to get the key that was pressed down.
    event = pygame.event.poll()
    if event.type == KEYDOWN:
        return event.key
def barrelGenerator(screen, difficulty, speed): #Make a function that will generate the barrels for the user. Difficulty affects both the speed of the barrels and the question difficulty.
    question = questionCreator(difficulty)    
    if 1 <= difficulty <= 2:
        if difficulty == 1:interval = 10 #Variable define: This will regulate how fast the barrels move later on.
        else: interval = 7
        answer = question['answer']
        text = str(question['values'][0]) + str(question['operation']) + str(question['values'][1]) #Format this properly.
    elif difficulty == 3:
        interval = 10 #Variable define: This will regulate how fast the barrels move later on.
        questionType = question['questionType']
        if questionType == 1:
            text = "" #Make the text an empty string
            if question['unknownValue'] != 1: text += str(question['b']) + " " + question['operation 1'] #Add to the text
            else: 
                answer = question['b']
                text += "b " + question['operation 1'] 
            if question['unknownValue'] != 2: text += " " + str(question['c']) + " " + question['operation 2'] #Add to the text some more.
            else: 
                answer = question['c']
                text += " c " + question['operation 2'] 
            if question['unknowValue'] != 3: text += " " + str(question['d']) #Add to the text even more
            else: 
                answer = question['d']
                text += " d "
        elif 2<= questionType <=  3: 
            text = str(question['values'][0]) + str(question['values'][2]) + " " + question['values'][1] + question['values'][3] + " " + str(question['values'][4]) #Big mouthful for one line.
            answer = question['answer']
        elif 4<= questionType <= 5: 
            text = question['equation']
            answer = question['answer']
        barrel = Barrel(text)
        objects = pygame.sprite.Group(barrel)
        objects.draw(screen)
        pygame.display.flip()
    alive = True #Variable define: A variable to hold the life of the user. Soon as they die, alive is False
    oldTextPos = box(screen, "Answer = ", None, None) #Put in the text
    inputted = "" #Make a variable for what the user inputs.
    turn = 0 #Variable define: Will be used to determine if we should turn the barrel or not.
    while alive:
        turn += 1
        clock.tick(60) #Limit to 60 fps
        if turn % interval == 0: #Limit how fast the barrels move.
            screen.fill((0,0,0))
            barrel.roll() #Roll the barrel
            objects.update(barrel) #Update the objects class
            objects.draw(screen) #Draw it
            pygame.display.flip()
        keyPressed = keyer() #See if key has been pressed
        if keyPressed == None: continue #If the user puts in nothing we try again.
        correct = None
        if 48 <= keyPressed <= 57: #We make sure that they are only inputting numbers.
            inputted += str(chr(keyPressed))
        if inputted[-1] == str(answer)[len(inputted)-1]: correct = True
        else: correct = False
        oldTextPos = box(screen, "Answer = " + inputted, correct, oldTextPos) #Put in the text
        if correct == False: inputted = ""
        if inputted == answer: 
            jump = True
            break
            print("Jump!")

def questionCreator(difficulty): #Make a function that will make the question for the barrel
    #Operation legend: 1 = addition, 2 = subtraction, 3 = multiplication, 4 = division, 5 = powers, 6 = square roots.
    if difficulty == 1:
        num1, num2 = random.randint(0, 100), random.randint(0, 100)
        operation = random.randint(1, 2) #Make a random number between 1 and 2 to decide the operation that will be used
        if operation == 1: 
            answer = num1 + num2
            operation = "+"
        elif operation == 2: 
            answer = num1 - num2
            operation = "-"
        equation = {'operation': operation, 'answer': answer, 'values':[num1, num2]} #Variable define: Making a list for all of the numbers and the operation.

    elif difficulty == 2: #Get questions for difficulty 2
        operation = random.randint(1, 4) #Make a random number between 1 and 4 to get the operation that will be used.
        if operation <= 2: #1: addition, 2: subtraction
            num1, num2, = random.randint(0, 100), random.randint(0, 30), 
            oldnum1, oldnum2 = num1, num2 #Variable define: The numbers for addition or subtraction.
            if operation == 1: 
                operation = "+"
                answer = num1 + num2 #Get the answer
            elif operation == 2: 
                operation = "-"
                num1, num2 = max(oldnum1, oldnum2), min(oldnum1, oldnum2) #Variable define: The numbers for subtraction
                answer = num1 - num2 #Get the answer.
        elif operation == 3: #3: Multiplication
            operation = chr(158) #Multiplication symbol
            num1, num2 = random.randint(0, 12), random.randint(0, 12)
            answer = num1 * num2
        elif operation == 4: #4: Division
            operation = chr(246) #Division symbol FTW
            num2 = random.randint(0, 12) #num2 is the divisor
            num1 = num2 * random.randint(0, 12) #num1 is then number to be divided.
            answer = num1 // num2
        equation = {'operation' : operaton, 'answer': answer, 'values': [num1, num2]} #Variable define: Making a dictionary for all of the numbers and the operation.

    elif difficulty == 3:
        questionType = random.randint(1, 5) #Variable define: We wil decide if we're doing a reverse-operations question (1), a powers or square root question (2 and 3) or an order of operations question (4 and 5).
        if questionType == 1: #These question types (reverse operations) will be binomials with one variable of the form a = bc + d or a = b/c - d or other variations. The unknown will be either b, c or d.
            unknown = random.randint(1, 3) #Decide who will be the unknown. 1 = b, 2 = c, 3 = d
            op1, op2 = random.randint(1, 2), random.randint(1, 2) #Decide which operations to perform.
            b, c, d = random.randint(1, 15), random.randint(1, 15), random.randint(0, 100) #Variable define: Come up with all of the numbers in the equation.
            bc = b *c #We want this to run no matter what so that we can either use it for multiplication or for a nice integer division.
            if op1 == 2: #2 is division
                op1 = chr(246) 
                b = bc #Make b bc so that it will be an integer division.
                bc = bc/c #Get the results of that part.
            if op2 == 1: 
                a = bc + d #+
                op2 = "+"
            elif op2 == 2: 
                a = bc - d #-
                op2 = "-"
            equation = {'questionType':questionType, 'a':a, 'b':b, 'c':c, 'd':d, 'operation 1':op1, 'operation 2':op2, 'unknownValue':unknown} #Get ready to return the equation for the pygame to display during the game and to be displayed on the barrels.
        elif 2 <= questionType <= 3: #Equation of the form [math.sqrt]x[^2] [+][-] y
            psqrt = random.randint(0, 2) #Decide whether or not we're doing a power or a square root. 0 and 1 are power so that it is twice as likely.
            plusminus = random.randint(1, 2) #Decide if we will add or subtract y. 1 = add, 2 = subtract
            if psqrt != 2:
                psqrt = ""
                #Make the power.
                power = random.randint(1, 10) 
                if 9<= power : power = 2 #We want the power of 2 primarily.
                elif 7 <= power <= 8: power = 3 #We also want it to be more likely to have a power of 3. 
                base = random.randint(1, 12) #Make the base that will be put to an exponent.
                pAns = base ** power
                power = "^" + str(power) #Convert to string for later usage
                #This all means that powers of 1, 2, 3, 4, 5 and 6 are all possible but 2 is three times more likely and 3 is twice as likely.
            else:
                psqrt = chr(8730)
                pAns = random.randint(1, 12)
                base = pAns ** 2
                power = ""
            addsubtractNum = random.randint(1, 9) #Generate the random number that we will be adding to the power's product.
            if plusminus == 1: 
                answer = pAns + addsubtractNum
                plusminus = "+"
            else: 
                answer = pAns - addsubtractNum
                plusminus = "-"
            equation = {'questionType': questionType, 'answer':answer, 'values':[psqrt, power, base, plusminus, addsubtractNum]}
        elif 4 <= questionType <= 5: #Order of operations
            opNum = random.randint(3, 5) #Determine how many operators there will be, between 3 and 5.
            soFar = [] #Make a list that will eventually contain everything necessary for the equation.
            opList = ["+", "-", "*", "/"]
            for operators in range(0, opNum): #Loop around generating operators and numbers.
                if soFar.count("*") == 2 and "*" in opList: opList.remove("*") #We do not want more than two multiplication operators in any one equation.
                if soFar.count("/") == 1 and "/" in opList: opList.remove("/") #No more than 1 division operator per equation.
                if soFar.count("+") == 2 and "+" in opList: opList.remove("+") #No more than 2 addition operators.
                if soFar.count("-") == 2 and "-" in opList: opList.remove("-") #No more than 2 subtraction operator.
                number, operator = random.randint(1, 15), opList[random.randint(0, len(opList) -1)]
                try: 
                    if soFar[-1] == "/": 
                        soFar[-2] = number * soFar[-2]
                except IndexError: pass
                if operators != opNum -1: 
                    soFar.append(number)
                    soFar.append(operator)
                else: soFar.append(number)
            totalEquation = soFar.copy() #Duplicate the list of everything so far to be held for the end.
            while soFar.count("/") > 0 or soFar.count("*") > 0:
                if soFar.count("/") > 0: divisionPos = soFar.index("/")
                else: divisionPos = len(soFar)
                if soFar.count("*") > 0: multiplyPos = soFar.index("*")
                else: multiplyPos = len(soFar)
                num1, num2 = soFar[min(divisionPos, multiplyPos) -1], soFar[min(divisionPos, multiplyPos) + 1]
                if divisionPos < multiplyPos: 
                    replacement = num1//num2
                    for divisionB in range(0, 3): del soFar[divisionPos -1]
                    soFar.insert(divisionPos -1, replacement)
                else: 
                    replacement = num1 * num2
                    for multiplyB in range(0, 3): del soFar[multiplyPos -1]
                    soFar.insert(multiplyPos -1, replacement)
            while soFar.count("-") > 0:
                subtractionPos = soFar.index("-")
                num1, num2 = soFar[subtractionPos -1], soFar[subtractionPos + 1]
                replacement = num1-num2
                for subtractionB in range(0, 3): del soFar[subtractionPos -1]
                soFar.insert(subtractionPos -1, replacement)
            while soFar.count("+") > 0:
                additionPos = soFar.index("+")
                num1, num2 = soFar[additionPos -1], soFar[additionPos + 1]
                replacement = num1+num2
                for additionB in range(0, 3): del soFar[additionPos -1]
                soFar.insert(additionPos -1, replacement)
            answer = soFar[0]
            totalEquationStr = "" #Variable for the totalequation's string version
            for equationMaker in range(0, len(totalEquation)): #Make the totalequation into a string
                totalEquationStr += str(totalEquation[equationMaker])
            equation = {'questionType':questionType, 'answer': answer, 'equation':totalEquationStr} #Get ready to return this all.

        #elif difficulty == 4:

    return equation