#Author: Kyle Anderson. "input". Purpose: To make function for my hangman game that allow input boxes.
#Credit: Timothy Downs' inputbox. Looked at that and got inspiration, however I wrote this on my own.
#Modified from my own program from U6A4_1 to fit the RST's purposes.
import pygame
from pygame.locals import *

def box(screen, text, x, y, w, h, oldRect): #Make this function to draw the box for the input.
    font = pygame.font.Font(None, 22) #Get font variable
    displayText = font.render(text, 1, (0, 0, 0))
    textpos = displayText.get_rect()
    if w == "auto": 
        w, blab = font.size(text)
        w += 5
    if h == "auto": 
        blab, h = font.size(text)
        h += 5
    if oldRect != False: screen.fill((169, 169, 169), (oldRect[0] - oldRect[2]/2, oldRect[1] - oldRect[3]/2, oldRect[2] + 2, oldRect[3] + 2), 0)
    rect1 = pygame.draw.rect(screen, (119, 208, 237), (x - w/2, y - h/2, w, h), 0) #Draw the first rectangle.
    textpos.center = rect1.center
    pygame.draw.rect(screen, (255, 255, 255), (x- w/2, y - h/2, w, h), 2) #Draw the second rectangle.
    screen.blit(displayText, textpos)
    pygame.display.flip()
    return [x, y, w, h]
def keyer(): #Make a function to get the key that was pressed down.
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else: continue
def accepter(screen, prompt, security, help, x, y, w, h): #Make a function that will accept the input from the user.
    pygame.font.init()
    help = ": [" + help + "]"
    inputted = "" #Make a variable for what the user inputs.
    feedback = ""  #Make a variable for what we actually put on screen. 
    oldRect = False
    oldRect = box(screen, prompt + help, x, y, w, h, oldRect) #Make the box
    keyPressed = keyer()
    while keyPressed != K_RETURN:
        if keyPressed == K_BACKSPACE:
            inputted = inputted[0:-1]
            feedback = feedback[0:-1]
        elif keyPressed <= 127:
            if pygame.key.get_mods() == 1: #We want to have case-sensitive stuff.
                if keyPressed == 9: keyPressed = 32 #TAB is nothing
                elif keyPressed == 48: keyPressed = 41 #SHIFT + 0 = )
                elif keyPressed == 49: keyPressed = 33 #SHIFT + 1 = !
                elif keyPressed == 50: keyPressed = 64 #SHIFT + 2 = @
                elif keyPressed == 51: keyPressed = 35 #SHIFT + 3 = #
                elif keyPressed == 52: keyPressed = 36 #SHIFT + 4 = $
                elif keyPressed == 53: keyPressed = 37 #SHIFT + 5 = %
                elif keyPressed == 54: keyPressed = 94 #SHIFT + 6 = ^
                elif keyPressed == 55: keyPressed = 38 #SHIFT + 7 = &
                elif keyPressed == 56: keyPressed = 42 #SHIFT + 8 = *
                elif keyPressed == 57: keyPressed = 40 #SHIFT + 9 = (
                elif keyPressed == 47: keyPressed = 63 #SHIFT + / = ?
                elif keyPressed == 32: keypressed = 32 #SHIFT + SPACE remains a space
                else: keyPressed -= 32 #Make it an uppercase letter.
            inputted += str(chr(keyPressed))
            if security == 0: feedback += str(chr(keyPressed))
            else: feedback += "*"
        oldRect = box(screen, (prompt + ": " + feedback), x, y, w, h, oldRect)
        keyPressed = keyer()
    return inputted