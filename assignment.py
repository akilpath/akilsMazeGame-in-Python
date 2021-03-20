#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     Maze game called Speed Maze. Goal is to exit the maze as fast as possible.
# the faster you exit the maze the better your score.
#
# Author:      Akil Pathiranage
# Created:     March 9th, 2021
# Updated:     March 14th 2021
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because I added many different parts to the game, and the game runs very smoothly.
# My collision detection between circles and rectangles is accurate. I used inheritance with some of my classes.
#I created a moving camera within the game that moves around a 2d world. There is scaling in the program, so you can
#run the game at fullscreen, 1920x1080 or 1280x720. You can also change the ball color and your highscore is saved to a json
#file
#
#Features Added:
#customizable screen dimensions and customizable character color
#settings and high score are saved to a file so they do not reset each time the program is opened
#2d camera makes game more difficult since the player cannot see the whole entire map
#there is randomness with the exit generation, so each time the player plays the exit is not in the same place
#how to play button opens the browser to a google doc with instructions on how to play and information about the settings. 
#-----------------------------------------------------------------------------
#all images used were created by me using pixlr.com
#references:
#FPS counter was taken from Mr.Brooks
#JSON file loading and writing was shown to me by Selim Abdelwahab

import pygame
import time
import random
import json
import webbrowser
from classes import Button
from classes import Ball
from classes import Wall
from classes import TextBox
from classes import MultiButton

pygame.init()
pygame.font.init()

def updateFps(clock):
    '''
    Function gets the fps and renders it to text.
    Function was taken from Mr.Brooks
    
    Parameters
    -----------------------------------
    clock: pygame Clock() object
        needed to get the fps for the program

    Return
    -----------------------------------
        function returns a pygame.surface object with the fps as text on it
    
'''
    font = pygame.font.SysFont("Calibri", 14)
    fps = str(round(clock.get_fps()))
    fpsText = font.render(fps,1,(0,255,0))
    return fpsText

def generateMap(surface):
    '''
    function generates the map by creating many wall objects.
    
    many different wall objects are created and added to an array called walls. Parts of the walls are commented,
    showing which walls correspond to which exit. The very last part of the function randomly picks which exit will
    be set for this generation. The last element in walls array will be a green wall object that represents the exit.
    
    Parameters
    -----------------------------------
    surface:
        takes in a surface object, this object is the surface that the walls will be drawn on.
        when generateMap is called, it draws all of these walls to that surface, but that surface is not displayed
        to the user, which is why scaling is not needed.
        
    Returns:
    -----------------------------------
    walls: returns a tuple of wall objects

'''
    walls = []
    walls.append(Wall(surface,(0, 375),(80,10)))
    walls.append(Wall(surface,(0, 335),(80,10)))
    walls.append(Wall(surface,(80, 375),(10,120)))
    walls.append(Wall(surface,(80, 205),(10,140)))
    
    walls.append(Wall(surface,(120, 255),(10,200)))
    walls.append(Wall(surface,(80,495),(100,10)))
    walls.append(Wall(surface,(120,455),(300,10)))
    walls.append(Wall(surface,(180,495),(10,120)))
    walls.append(Wall(surface,(220,495),(10,80)))
    walls.append(Wall(surface,(180,615),(240,10)))
    walls.append(Wall(surface,(220,575),(240,10)))
    
    #Exit One---------
    walls.append(Wall(surface,(460,575),(10,145)))
    walls.append(Wall(surface,(420,615),(10,140)))
    #---
    walls.append(Wall(surface,(230,495),(400,10)))
    walls.append(Wall(surface,(420,255),(10,210)))
    walls.append(Wall(surface,(460,245),(10,220)))
    walls.append(Wall(surface,(120,245),(310,10)))
    walls.append(Wall(surface,(470,455),(200,10)))
    walls.append(Wall(surface,(80,205),(350,10)))
    walls.append(Wall(surface,(420,100),(10,105)))
    walls.append(Wall(surface,(460,60),(10,155)))

    #Exit Two-----------
    walls.append(Wall(surface,(270,50),(200,10)))
    walls.append(Wall(surface,(270,90),(160,10)))
    walls.append(Wall(surface,(260,50),(10,50)))
    #----
    
    walls.append(Wall(surface,(470,245),(300,10)))
    walls.append(Wall(surface,(470,205),(340,10)))
    
    #Exit Three---------
    walls.append(Wall(surface,(760,255),(10,120)))
    walls.append(Wall(surface,(800,215),(10,160)))
    walls.append(Wall(surface,(760,375),(50,10)))
     #----
    #Exit Four-----------
    walls.append(Wall(surface,(630,495),(10,160)))
    walls.append(Wall(surface,(670,495),(10,160)))
    walls.append(Wall(surface,(630,655),(50,10)))
    #----    
    walls.append(Wall(surface,(680,495),(410,10)))
    walls.append(Wall(surface,(670,455),(210,10)))
    walls.append(Wall(surface,(880,320),(10,145)))
    walls.append(Wall(surface,(920,320),(10,145)))
    walls.append(Wall(surface,(880,310),(50,10)))
    walls.append(Wall(surface,(930,455),(120,10)))
    
    #Exit Five-----------
    walls.append(Wall(surface,(1090,205),(10,300)))
    walls.append(Wall(surface,(1050,205),(10,260)))
    walls.append(Wall(surface,(1050,195),(50,10)))
    #----   
    chance = random.randint(1,5)
    if chance == 1:     
        #Exit One rectangle
        walls.append(Wall(surface,(430,690),(30,30), wallColorIn = (0,255,0)))
    elif chance == 2:
        #Exit Two rectangle
        walls.append(Wall(surface,(270,60),(30,30), wallColorIn = (0,255,0)))
    elif chance == 3:
        #Exit Three Rectangle
        walls.append(Wall(surface,(770,345),(30,30), wallColorIn = (0,255,0)))
    elif chance == 4:
        #Exit Four Rectangle
        walls.append(Wall(surface,(640,625),(30,30),wallColorIn = (0,255,0)))
    else:
        #Exit Five Rectangle
        walls.append(Wall(surface,(1060,205),(30,30),wallColorIn = (0,255,0)))
        
    return walls

def permissionToMove(direction, walls, playerPoints):
    '''
    This function is the function responsible for making sure that the player can move in the direction they want to.
    
    Depending on the direction the player wants to move in, the function checks the points in the corresponding
    direction on the circumference of the circle and determines if they are inside of the wall. For example, if
    the player wants to move up, the functions checks if the North point, north west point and north east point are
    inside any of the walls, if that is true, then it returns False, indicating that the user cannot go in the direction they desire.
    
    Parameters
    -----------------------------------
    direction: a string being "UP","RIGHT","DOWN" or "LEFT". Used to determine which points to check
    walls: a tuple of walls, this parameter is the value returned by generateMap() when the map is created
    playerPoints: an array of tuples that represent the points on the players circumference. This is the value returned
    by the getPoints() method of the ball class.
    
    Returns
    -----------------------------------
    returns a boolean value, true if the player can move, false if it cannot.

'''
    if direction == "UP":
        for wall in walls:
            for i in range(1,4):
                if wall.checkColl(playerPoints[i]) == True:
                    return False
        return True
    elif direction == "RIGHT":
        for wall in walls:
            for i in range(-1,2):
                if wall.checkColl(playerPoints[i]) == True:
                    return False
        return True
    elif direction == "DOWN":
        #this extra if statement is needed, since there is no wall in this direction, just the end of the surface
        if playerPoints[6][1] + 3 >= 720:
            return False
        for wall in walls:
            for i in range(5,8):
                if wall.checkColl(playerPoints[i]) == True:
                    return False
        return True
    elif direction == "LEFT":
        if playerPoints[4][0] - 3 <= 0:
            return False
        for wall in walls:
            for i in range(3,6):
                if wall.checkColl(playerPoints[i]) == True:
                    return False
        return True
    return False


def main():
    '''
    Function containing the game loop, no returns or parameters. 
'''
    
    #Begins by loading the data from the data file
    with open(r"assets/data.json") as file:
        data = json.load(file)
        print(f"Information in settings: {data}")
        file.close()
    #if the window is set to fullscreen in the data, file create a fullscreen pygame window
    if data["resolution"] == [0,0]:
        mainGame = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        resolution = pygame.display.get_window_size()
    else:
        resolution = data["resolution"]
        mainGame = pygame.display.set_mode(resolution)
    #scaling stores the scaling factor for the width of the screen and the length/height
    scaling = (resolution[0]/1280,resolution[1]/720)
    #world object is the surface that the game is rendered to
    world = pygame.Surface((1150,720))
    player = Ball(world, (30,360), ballColorIn = data["ballcolor"])
    clock = pygame.time.Clock()
    
    #gameState of 0 is the intro screen, following code setups the intro screen and and other variables in the game
    gameState = 0
    buttons = [Button("QUIT", textIn = "QUIT", posIn = (700*scaling[0],500*scaling[1])),
               Button("PLAY", textIn = "Play", posIn = (500*scaling[0],500*scaling[1])),
               Button("TUTORIAL", textIn = "How to Play", posIn = (575*scaling[0],600*scaling[1])),
               Button("SETTINGS", textIn = "Settings", posIn = (1200*scaling[0],680*scaling[1]), fontSizeIn = 14)]
    if data["highscore"] == -1:
        highScore = None
    else:
        highScore = data["highscore"]
    score = 0
    startTimer = 0
    #scales backgrounds to the screen resolution
    backgrounds = (pygame.transform.scale(pygame.image.load(r"assets/background.jpg"), pygame.display.get_window_size()), pygame.transform.scale(pygame.image.load(r"assets/backgroundTwo.jpg"), pygame.display.get_window_size()))
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT or gameState == -1:
            #if the user clicks the x button or the gameState is -1, it breaks from the main loop and closes game
            break
        if gameState == 0:
            mainGame.blit(backgrounds[0],(0,0))
            for button in buttons:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if button.buttonHit() == "PLAY":
                        #if the player clicks the play button the gameState is set to 1.
                        #setsup map and buttons needed for the game, also creates a variable called starTimer which is used for the timer
                        gameState = 1
                        walls = generateMap(world)
                        mazeExit = walls[len(walls)-1]
                        del walls[len(walls)-1]
                        buttons = [Button("QUIT", textIn = "QUIT", posIn = (630*scaling[0],650*scaling[1]))]
                        texts = [TextBox(textIn = "Score:", posIn = (1000*scaling[0],100*scaling[1])),
                                 TextBox(textIn = f"{score}", posIn = (1000*scaling[0],160*scaling[1]))]
                        startTimer = time.time()
                        break
                    elif button.buttonHit() == "QUIT":
                        #gameState of -1 is the default gamestate which is called when the user clicks the quit button on any screen
                        gameState = -1
                        break
                    elif button.buttonHit() == "TUTORIAL":
                        #if the user clicks how to play, it opens a link to a google doc with instructions on how to play
                        webbrowser.open("https://docs.google.com/document/d/10sVfS0pjQY3BrWsw5jMPi9ZBJNQ-JpQf02bXztE-rAk/edit?usp=sharing")                    
                    elif button.buttonHit() == "SETTINGS":
                        #if the user clicks the settings button, then it sets up the setting screen (gameState = 3)
                        buttons = [MultiButton(keyIn = "RESOLUTION", textIn = ("1280x720", "1920x1080", "Fullscreen"), posIn = (700*scaling[0],350*scaling[1])),
                                   MultiButton(keyIn = "BALLCOLOR", textIn = ("Red", "Blue", "Green"), posIn= (700*scaling[0], 400*scaling[1])),
                                   Button("QUIT", textIn = "QUIT", posIn = (630*scaling[0],650*scaling[1])),
                                   Button("BACK", textIn = "Back", posIn = (200*scaling[0],650*scaling[1])),
                                   Button("RESET", textIn = "Reset Settings and HighScore", posIn = (500*scaling[0],550*scaling[1]))]
                        texts = [TextBox(textIn = "Resolution",textBoxColorIn = (30,30,30),posIn = (500*scaling[0],350*scaling[1])),
                                 TextBox(textIn = "Ball Color", textBoxColorIn = (30,30,30), posIn = (500*scaling[0],400*scaling[1])),
                                 TextBox(textIn = "Settings", textBoxColorIn = (30,30,30),fontSizeIn = 40,posIn = (550*scaling[0], 100*scaling[1])),
                                 TextBox(textIn = "Restart Game for Changes to Take Effect", textBoxColorIn = (30,30,30), fontSizeIn = 14, posIn = (500*scaling[0],200*scaling[1]))]
                        gameState = 3
                button.draw(mainGame)
        elif gameState == 1:
            #this gamestate is for when the user is actually playing the game
            #fills the background for the world and blits the background for the display surface
            world.fill((255,255,255))
            mainGame.blit(backgrounds[0],(0,0))
            
            #depending on which direction the player wants to move in, it checks if the player is allowed to move in that direction
            #if yes, then it moves the player in that direction.
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_w]:
                if permissionToMove("UP",walls,player.getPoints()):
                    player.moveUp()
            if keyPressed[pygame.K_s]:
                if permissionToMove("DOWN",walls,player.getPoints()):
                    player.moveDown()
            if keyPressed[pygame.K_a]:
                if permissionToMove("LEFT",walls,player.getPoints()):
                    player.moveLeft()
            if keyPressed[pygame.K_d]:
                if permissionToMove("RIGHT",walls,player.getPoints()):
                    player.moveRight()
            if (mazeExit.pos[0] <= player.pos[0] <= (mazeExit.pos[0] + mazeExit.wallDimensions[0]) and mazeExit.pos[1] <= player.pos[1] <= (mazeExit.pos[1] + mazeExit.wallDimensions[1])):
                #if the player goes into the maze exit, it setsup the win screen (gameState = 2)
                gameState = 2
                score = round((time.time()-startTimer)*100)/100
                if highScore == None or score < highScore:
                    #if the highscore is not set yet or if the score is less than high score then it updates the highscore
                    #also saves highscore to file
                    highScore = score
                    data["highscore"] = highScore
                    with open(r"assets/data.json", "w") as file:
                        json.dump(data, file)
                        file.close()
                        
                buttons = [Button("QUIT", textIn = "QUIT", posIn = (620*scaling[0],650*scaling[1])),
                           Button("PLAY", textIn = "Play Again", posIn = (600*scaling[0],500*scaling[1]))]
                texts = [TextBox(textIn = "You Win!", fontSizeIn = 40, posIn = (560*scaling[0],150*scaling[1])),
                         TextBox(textIn = "Your score is:", fontSizeIn = 20, posIn = (525*scaling[0],300*scaling[1])),
                         TextBox(textIn = f"{score}", fontSizeIn = 20, posIn = (700*scaling[0],300*scaling[1])),
                         TextBox(textIn = "Your highscore is:", fontSizeIn = 14, posIn = (545*scaling[0],400*scaling[1])),
                         TextBox(textIn = f"{highScore}", fontSizeIn = 14, posIn = (700*scaling[0],400*scaling[1]))]
                continue
            if ev.type == pygame.MOUSEBUTTONDOWN and buttons[0].buttonHit() == "QUIT":
                gameState = -1
            #draws all elements on screen
            mazeExit.drawWall()
            player.drawBall()
            for wall in walls:
                wall.drawWall()
            buttons[0].draw(mainGame)
            for text in texts:
                text.draw(mainGame)
            score = round((time.time()-startTimer)*100)/100
            texts[1].changeText(score)
            #This is where the camera is created
            #The camera works by creating a surface, and blitting a small portion of the rendered world
            #to the camera surface, then blitting the camera surface onto the main display surface
            camera = pygame.Surface((100,100))
            camera.blit(world,(0,0),(player.pos[0]-50,player.pos[1]-50,100,100))
            camera = pygame.transform.scale(camera,(round(500*scaling[0]),round(500*scaling[1])))
            mainGame.blit(camera,(390*scaling[0],110*scaling[1]))
        elif gameState == 2:
            #gamestate for the win screen
            mainGame.blit(backgrounds[1],(0,0))
            for button in buttons:
                button.draw(mainGame)
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if button.buttonHit() == "QUIT":
                        gameState = -1
                        break
                    if button.buttonHit() == "PLAY":
                        #sets the game up again if the user wants to play again
                        gameState = 1
                        walls = generateMap(world)
                        mazeExit = walls[len(walls)-1]
                        del walls[len(walls)-1]
                        buttons = [Button("QUIT", textIn = "QUIT", posIn = (630*scaling[0],650*scaling[1]))]
                        texts = [TextBox(textIn = "Score:", posIn = (1000*scaling[0],100*scaling[1])),
                                 TextBox(textIn = f"{score}", posIn = (1000*scaling[0],160*scaling[1]))]
                        player.setPos((30,360))
                        startTimer = time.time()
            for text in texts:
                text.draw(mainGame)
        elif gameState == 3:
            #gameState for the settings screen
            mainGame.blit(backgrounds[1],(0,0))
            for button in buttons:
                button.draw(mainGame)
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if button.buttonHit() == "RESOLUTION":
                        #if the user clicks on the resolution button, it cycles to the next text in the multibutton,
                        #then it stores the selected resolution into the json file
                        #restarting the game is needed to changes to take effect
                        button.changeState()
                        if button.getText() == "1280x720":
                            data["resolution"] = [1280,720]
                        elif button.getText() == "1920x1080":
                            data["resolution"] = [1920,1080]
                        elif button.getText() == "Fullscreen":
                            data["resolution"] = [0,0]
                        with open(r"assets/data.json", "w") as file:
                            json.dump(data,file)
                            file.close()
                    elif button.buttonHit() == "BALLCOLOR":
                        #if the user clicks on the ballcolor button, it cycles to the next option in the multibutton
                        #stores the color into the json file
                        button.changeState()
                        if button.getText() == "Red":
                            data["ballcolor"] = [255,0,0]
                        elif button.getText() == "Green":
                            data["ballcolor"] = [0,255,0]
                        elif button.getText() == "Blue":
                            data["ballcolor"] = [0,0,255]
                        with open(r"assets/data.json", "w") as file:
                            json.dump(data,file)
                            file.close()
                    elif button.buttonHit() == "RESET":
                        #if the user clicks the reset button, it resets all the data in the data file back to original settings
                        #and clears highscore
                        data["resolution"] = [1280,720]
                        data["highscore"] = -1
                        data["ballcolor"] = [255,0,0]
                        with open(r"assets/data.json","w") as file:
                            json.dump(data,file)
                            file.close()
                    elif button.buttonHit() == "QUIT":
                        gameState = -1
                        break
                    elif button.buttonHit() == "BACK":
                        gameState = 0
                        buttons = [Button("QUIT", textIn = "QUIT", posIn = (700*scaling[0],500*scaling[1])),
                                   Button("PLAY", textIn = "Play", posIn = (500*scaling[0],500*scaling[1])),
                                   Button("TUTORIAL", textIn = "How to Play", posIn = (575*scaling[0],600*scaling[1])),
                                   Button("SETTINGS", textIn = "Settings", posIn = (1200*scaling[0],680*scaling[1]), fontSizeIn = 14)]
            for text in texts:
                text.draw(mainGame)
        #framerate
        clock.tick(60)
        mainGame.blit(updateFps(clock),(0,0))
        pygame.display.update()
    pygame.quit()
main()