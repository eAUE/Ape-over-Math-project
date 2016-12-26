#Just testing the controller functionality in pygame.
import pygame, time
pygame.init()
pygame.joystick.init()

try: 
    xboxController = pygame.joystick.Joystick(0)
    xboxController.init()
    print(xboxController.get_name())
    print("Axes", (xboxController.get_numaxes()))
    print("Balls", xboxController.get_numballs())
    print("Buttons", xboxController.get_numbuttons())
    print("Hats", xboxController.get_numhats())
    if xboxController.get_init() == True: print("Initialized properly")
    #while 1:
    #    pygame.event.get()
    #    for event in pygame.event.get():
    #        if event.type == pygame.JOYAXISMOTION:
    #            print("Joystick")
    #        elif event.type == pygame.JOYBUTTONDOWN:
    #            print("Joy down")
    #        elif event.type == pygame.JOYBUTTONUP: print("Joy up")
    #found = False
    #trial = 0
    while 1:
        #trial += 1
        #print(trial)
        pygame.event.get()
        for a in range(0, xboxController.get_numaxes()):
            if xboxController.get_axis(a) != 0.0: 
                print(xboxController.get_axis(a))
        for b in range(0, xboxController.get_numballs()):
            if xboxController.get_ball(b) != 0: 
                print(xboxController.get_ball(b))
        for c in range(0, xboxController.get_numbuttons()):
            if xboxController.get_button(c) != 0: 
                print(xboxController.get_button(c))
        for d in range(0, xboxController.get_numhats()):
            if xboxController.get_hat(d) != (0, 0): 
                print(xboxController.get_hat(d))
except KeyboardInterrupt:
    pygame.joystick.quit()
    quit()