#Author: Kyle Anderson. "RST". Purpose: To make a game where barrels will roll on the ground with 
#math questions on them that the user must answer the question to be able to jump over the barrel and survive.
import pygame, time, input, json, tkinter, BarrelGenerator
from pygame.locals import * 
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("User Selection")
BarrelGenerator.barrelGenerator(screen, 3, 1)
def login(): #Make a function to log in the specific user.
    users = open("userData.json", "r+")
    if users.readline() == "":
        screen.fill((169, 169, 169), None, 0)
        userInfo = {'user': 1, "creationD": time.strftime("%Y - %m - %d %H:%M, %u")} 
        users.write(json.dumps(userInfo))
        users.close()
        #username = input.accepter(screen, "Username", 0, "Between 4 and 20 characters", screen.get_rect().centerx, screen.get_rect().centery, "auto", "auto")
        menu(userInfo)
    else:
        users.seek(0)
        screen.fill((169, 169, 169), None, 0)
        screen.blit(oldBackground, (0,0))
        numUsers = len(users.readlines())
        existingUsers = [] #Make a variable to store which user slots have been taken.
        users.seek(0)
        for a in range(0, numUsers): #Loop around and find out which user slots have been used.
            existingUsers.append((json.loads(users.readline()))['user'])
        regColour, unregColour = (102, 209, 90), (115, 115, 115) #Variable defines: Different colours for rectangles depending whether or not the user has been created.
        user1 = pygame.draw.rect(screen, regColour, (screen.get_rect().centerx - 200, screen.get_height()/5 -32.5, 400, 75), 0)
        if 2 in existingUsers: user2 = pygame.draw.rect(screen, regColour, (screen.get_rect().centerx - 200, screen.get_height()/5 * 2 -32.5, 400, 75), 0)
        else: user2 = pygame.draw.rect(screen, unregColour, (screen.get_rect().centerx - 200, screen.get_height()/5 *2 -32.5, 400, 75), 0)
        if 3 in existingUsers: user3 = pygame.draw.rect(screen, regColour, (screen.get_rect().centerx - 200, screen.get_height()/5 * 3 -32.5, 400, 75), 0)
        else: user3 = pygame.draw.rect(screen, unregColour, (screen.get_rect().centerx - 200, screen.get_height()/5 *3 -32.5, 400, 75), 0)
        if 4 in existingUsers: user4 = pygame.draw.rect(screen, regColour, (screen.get_rect().centerx - 200, screen.get_height()/5 * 4 -32.5, 400, 75), 0)
        else: user4 = pygame.draw.rect(screen, unregColour, (screen.get_rect().centerx - 200, screen.get_height()/5 *4 -32.5, 400, 75), 0)
        rectList = [user1, user2, user3, user4] #Variable define: To be used to print out the text for each one.
        for printText in range(1, 5): #Loop through to print all of the text that we want.
            text = font.render("User " + str(printText), 1, (255, 255, 255))
            pos = text.get_rect()
            pos.center = rectList[printText-1].center
            screen.blit(text, pos)
        pygame.display.flip()
        clicked = False
        while not clicked:
            clock.tick(60)
            pygame.event.get()
            if pygame.mouse.get_pressed() == (True, False, False):
                if user1.collidepoint(pygame.mouse.get_pos()) == True and 1 in existingUsers: 
                    clicked = True
                    userID = 1
                elif user2.collidepoint(pygame.mouse.get_pos()) == True and 2 in existingUsers: 
                    clicked = True
                    userID = 2
                elif user3.collidepoint(pygame.mouse.get_pos()) == True and 3 in existingUsers: 
                    clicked = True
                    userID = 3
                elif user4.collidepoint(pygame.mouse.get_pos()) == True and 4 in existingUsers: 
                    clicked = True
                    userID = 4
            pygame.display.flip()
        users.seek(0)
        for findingUser in range(0, numUsers): #Look for that user's number
            found = json.loads(users.readline())
            if found['user'] == userID:
                break
        users.close()
        menu(found)

def menu(user): #Make a function that will actually host the menu
    welcomeMusic.stop()
    pygame.display.set_caption("Main Menu")
    font = pygame.font.Font(None, 18)
    userWelcome = font.render("Hello User " + str(user['user']) + "!", 1, (140, 111, 136))
    userWelcome_Pos = displayText.get_rect()
    userWelcome_Pos.topright = screen.get_rect().topright

#background = pygame.Surface(screen.get_size())
#background = background.convert()
#background.fill((169, 169, 169))
background = pygame.image.load("jungleGood.jpg")
background = pygame.transform.scale(background, (836, 400))
RGBAbackground = pygame.image.tostring(background, "RGBA")
background = background.convert()
clicked = False #Variable define: A variable to hold whether or not the mouse clicker has been clicked
pygame.mixer.init()
welcomeMusic = pygame.mixer.Sound("imperialMarch.wav")
welcomeMusic.set_volume(1.0)
welcomeMusic.play(-1)

while not clicked:
    oldBackground = background.copy()
    font = pygame.font.Font(None, 36)
    text = font.render("Enter", 1, (255, 255, 255))
    rect1 = pygame.draw.rect(background, (0,0,0), (screen.get_rect().centerx - 200, screen.get_rect().centery - 50, 400, 100), 0)
    textPos = text.get_rect()
    textPos.center = rect1.center
    background.blit(text, textPos)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.event.get()
    if pygame.mouse.get_pressed() == (True, False, False):
        if pygame.mouse.get_pos() > (rect1.left, rect1.top) and pygame.mouse.get_pos() < (rect1.right, rect1.bottom):
            clicked = True
    clock.tick(60)
login()



#totalList = []
#for a in range(0, len(Contents)):
#    cost = ""
#    for b in range(0, len(Contents[a])):
#        if Contents[a][b].isdigit() == True or Contents[a][b] == ".": 
#            cost += Contents[a][b]
#    totalList.append(float(cost))
#totalCost = sum(totalList)
#Contents = ["Kyle The total cost of your items is 9.9", "Sean The total cost of your items is 8.9"]