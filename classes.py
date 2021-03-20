import pygame
pygame.init()
pygame.font.init()

class Wall():
    def __init__(self, surfaceIn, posIn, wallDimensionsIn, wallColorIn = (0,0,0)):
        '''
        Function initializes wall objects.
        
        Each wall object has a rectangle object
        
        Parameters
        -----------------------------------
        surfaceIn: contains a surface for the wall object
        posIn: contains a tuple that represents the walls position on the surface
        wallDimensionsIn: a tuple that represents the width and height of the wall.
        wallColorIn: contains a tuple that represents the rgb for the walls, defaults to black, was added for future customization in settings.

'''
        self.surface = surfaceIn
        self.pos = posIn
        self.wallDimensions = wallDimensionsIn
        self.wallColor = wallColorIn
        self.wall = pygame.Rect(self.pos,self.wallDimensions)
    
    def drawWall(self):
        '''
        This method draws each rectangle for each wall, it has no returns or parameters. 
'''
        pygame.draw.rect(self.surface, self.wallColor, self.wall)
    
    def checkColl(self,point):
        '''
        Method used for determining if a point is touching the wall. This function is mainly used by the permissionToMove(function).
        
        Parameters
        -----------------------------------
        point: a tuple representing a single point
        
        Returns
        -----------------------------------
        returns a boolean value, True if the point is touching the wall, False if it is not
'''
        return True if self.wall.collidepoint(point) else False

class Ball():
    def __init__(self, surfaceIn, posIn, radiusIn = 10, ballColorIn = (255,0,0)):
        '''
        Initializes the ball object, creates attributes needed for the methods within Ball class
        
        Parameters
        -----------------------------------
        surfaceIn: surface to draw the ball on
        posIn: position on surface to draw the ball
        radiusIn: radius of the ball, defaults to 10
        ballColorIn: a tuple representing the rgb for the ball, defaults to red

'''
        self.surface = surfaceIn
        self.pos = posIn
        self.radius = radiusIn
        self.ballColor = ballColorIn
        
        #speedX and speedY represent the x speed and y speed of the ball
        self.speedX = 3
        self.speedY = 3
    
    def setPos(self,newPos):
        '''
        Method for manually setting the position of the ball
        
        Parameters
        -----------------------------------
        newPos: a tuple representing the newPosition to set the ball to.
'''
        self.pos = newPos
    
    def drawBall(self):
        '''Method for drawing the ball'''
        pygame.draw.circle(self.surface, self.ballColor, self.pos, self.radius)
        
    def moveUp(self):
        '''Method for moving the ball Up'''
        self.pos = (self.pos[0],self.pos[1]-self.speedY)
        
    def moveDown(self):
        '''Method for moving the ball Down'''
        self.pos = (self.pos[0],self.pos[1]+self.speedY)
        
    def moveLeft(self):
        '''Method for moving the ball Left'''
        self.pos = (self.pos[0]-self.speedX,self.pos[1])
        
    def moveRight(self):
        '''Method for moving the ball Right'''
        self.pos = (self.pos[0]+self.speedX,self.pos[1])
    
    def getPoints(self):
        '''
        Method for getting the points on the circle. Used the special value for sin45 and cos45 to determine points.
        Any point on a circle set at 0,0 can be determined by doing (r*sintheta,r*costheta). Adding this value to the
        value of the center point of the circle can determine the value for the point on the circumference.
        
        Returns
        -----------------------------------
        returns a list of points on the circle. 
'''
        pointOnCirc = round(self.radius*((2**0.5)/2))
        points = []
        points.append((self.pos[0] + self.radius, self.pos[1]))
        points.append((self.pos[0] + pointOnCirc, self.pos[1] - pointOnCirc))
        points.append((self.pos[0],self.pos[1] - self.radius))
        points.append((self.pos[0] - pointOnCirc, self.pos[1] - pointOnCirc))
        points.append((self.pos[0] - self.radius, self.pos[1]))
        points.append((self.pos[0] - pointOnCirc, self.pos[1] + pointOnCirc))
        points.append((self.pos[0], self.pos[1] + self.radius))
        points.append((self.pos[0] + pointOnCirc, self.pos[1] + pointOnCirc))
    
        
        return points

class TextBox():
    def __init__(self, keyIn = None, textIn = "", textColorIn = (255,255,255), posIn = (0,0), fontIn = "Arial", fontSizeIn = 18, textBoxColorIn = (175,175,175)):
        '''
        Initializes the TextBox class. TextBox class is the parent class of button and multiButton class.
        
        Parameters
        -----------------------------------
        keyIn: this parameter is used mainly for the button class and multi button class. It is an idea I got from pysimplegui, each button/multibutton has a key, the key can be used to identify
        which button the user has clicked. It is very useful since all buttons and mutli buttons are stored in an array. Defaults to None, for textBoxes.
        textIn: a string, represents what text is going into the textBox, only works with single line text, no support for multi line text
        textColorIn: a tuple representing the color of the text, defaults to white
        posIn: position on surface to draw the textbox, defaults to origin
        fontIn: a string representing the font to use, added to have multiple texts with different fonts but I don't know which fonts my computer has so right now it default to "Arial"
        fontSizeIn: an integer representing the size of the font, defaults to 18
        textBoxColorIn: a tuple containing the color of the textbox, defaults to grey.
        
        Key attributes
        -----------------------------------
        self.font: this is the font object that is used when drawing and rendering text for the text box.
        self.textDim: this is a tuple, representing the length and width of the rendered text
        self.outline: contains a rectangle object that represents the outline of the text (the box behind the text)
        self.scaling: this representings a scaling factor for the screen size, the textboxes and buttons need to be scaled since they are being
        displayed to the user.
        '''
        self.pos = posIn
        self.text = textIn
        self.textColor = textColorIn
        self.fontChoice = fontIn
        self.fontSize = fontSizeIn
        self.font = pygame.font.SysFont(self.fontChoice, self.fontSize)
        self.key = keyIn
        self.textDim = None
        self.outline = None
        screenSize = pygame.display.get_window_size()
        self.scaling = (screenSize[0]/1280,screenSize[1]/720)
        self.changeText(textIn)
        self.textBoxColor = textBoxColorIn
    
    def draw(self,surface):
        '''
        Method used to draw the textbox
        
        Parameters
        -----------------------------------
        surface: takes in a surface object that represents which surface to draw to. 
'''
        #Because all text is rendered into an image, the image can be rescaled to the screen size. 
        textBoxText = pygame.transform.scale(self.font.render(self.text,1,self.textColor),(round(self.textDim[0]*self.scaling[0]),round(self.textDim[1]*self.scaling[1])))
        pygame.draw.rect(surface,self.textBoxColor,self.outline)
        surface.blit(textBoxText, self.pos)
        
    def changeText(self, textIn):
        '''
        Method for changing the text in a textBox. It is also used during initialization, to create the rectangle and the dimensions for the text
        
        Parameters
        -----------------------------------
        textIn: takes in a string or an integer, represents the new text to be put on the textbox or button. 

'''
        self.text = str(textIn)
        self.textDim = pygame.font.Font.size(self.font,self.text)
        self.outline = pygame.Rect((self.pos[0]-20*(self.fontSize/18)*self.scaling[0], self.pos[1]-11.25*(self.fontSize/18)*self.scaling[1]), ((self.textDim[0] + 40*(self.fontSize/18))*self.scaling[0], (self.textDim[1] + 22.5*(self.fontSize/18))*self.scaling[1]))
    

class Button(TextBox):
    def __init__(self, keyIn, textIn = "", textColorIn = (255,255,255), posIn = (0,0), fontIn = "Arial", fontSizeIn = 18):
        super().__init__(keyIn, textIn, textColorIn, posIn, fontIn, fontSizeIn)
        '''
        Initializes the button class by using the same initialization as the textbox class
'''

    def draw(self, surface):
        '''
        Method for drawing the buttons, this overrides the draw() method of the textbox class.
        
        Performs in almost the same way as the draw method for the textbox class, except it checks if the users cursor is above the button, if so it changes the color
        to create an effect when the user hovers over the button.
        
        Parameters
        -----------------------------------
        surface: this is a surface object that represents where the button will be drawn.
'''
        buttonTxt = pygame.transform.scale(self.font.render(self.text,1,self.textColor),(round(self.textDim[0]*self.scaling[0]),round(self.textDim[1]*self.scaling[1])))
        if self.buttonHit() == self.key:
            pygame.draw.rect(surface, (125,125,125), self.outline)
        else:
            pygame.draw.rect(surface, (175,175,175), self.outline)
        surface.blit(buttonTxt, self.pos)
        
    def buttonHit(self):
        '''
        Method for determining if the button was hit or not (if the cursor is above the button). Since all the buttons are rectangles, it works by checking if the x position
        of the mouse is inside of the rectangle and if the y position is inside the rectangle.
        
        Returns
        -----------------------------------
        If the mouse is on the button it returns the objects key. If not, it returns false. 

'''
        xOne = self.pos[0]-20*(self.fontSize/18)*self.scaling[0]
        yOne = self.pos[1]-11.25*(self.fontSize/18)*self.scaling[1]
        xTwo = xOne + self.textDim[0] + 40*(self.fontSize/18)*self.scaling[0]
        yTwo = yOne + self.textDim[1] + 22.5*(self.fontSize/18)*self.scaling[1]
        if (xOne <= pygame.mouse.get_pos()[0] <= xTwo) and (yOne <= pygame.mouse.get_pos()[1] <= yTwo):
            return self.key
        else:
            return False

class MultiButton(Button):
    def __init__(self, keyIn, textIn = "", textColorIn = (255,255,255), posIn = (0,0), fontIn = "Arial", fontSizeIn = 18):
        '''
        Initializes Multibutton class. Multibutton class is a child class of button, which is a child of textBox. Uses the same initialization as the button class, but self.outline
        and self.textDim are created differently (look at changeText() of multibutton class). Also two more attributes are created which are self.states and self.state.
        
        Parameters
        -----------------------------------
        textIn: this textIn is an array of strings instead of a single string.
        
        Key Attributes
        -----------------------------------
        self.state: used to determine which element in the array of self.text is displaying
        self.states: represents the length of the array of texts in the multibutton (how many different states)
'''
        self.state = 0
        self.states = len(textIn)
        super().__init__(keyIn, textIn, posIn = posIn, fontSizeIn = 18)
        
    def draw(self, surface):
        '''
        Method used for drawing the multibutton. Overrides the draw() method of Button class. What is different about this one is now it is accessing from an array of texts
        instead of just a single text.
        
        Parameters
        -----------------------------------
        surface: a surface type object that represents where the mutlibutton is drawn to.
'''
        buttonTxt = pygame.transform.scale(self.font.render(self.text[self.state],1,self.textColor),(round(self.textDim[0]*self.scaling[0]),round(self.textDim[1]*self.scaling[1])))
        if self.buttonHit() == self.key:
            pygame.draw.rect(surface,(125,125,125),self.outline)
        else:
            pygame.draw.rect(surface,(175,175,175), self.outline)
        surface.blit(buttonTxt,self.pos)

    def changeState(self):
        '''
        Method for changing the state of the multibutton. Allows for the multibutton to be cycled through
'''
        if self.state == self.states-1:
            self.state = 0
        else:
            self.state += 1
        self.changeText()
        
    def changeText(self, textIn = ""):
        '''Method for changing the text in a multibutton. This is needed since the size of the textbox changes depending on the length of the text
        
        Parameters
        -----------------------------------
        textIn: this parameter is redundant, it is only added to prevent errors happening when super() is called. No matter what text is passed
        into this method, the text will always be changed to self.text[self.state]
'''
        self.textDim = pygame.font.Font.size(self.font,self.text[self.state])
        self.outline = pygame.Rect((self.pos[0]-20*(self.fontSize/18)*self.scaling[0], self.pos[1]-11.25*(self.fontSize/18)*self.scaling[1]), ((self.textDim[0] + 40*(self.fontSize/18))*self.scaling[0], (self.textDim[1] + 22.5*(self.fontSize/18))*self.scaling[1]))
        
    def getText(self):
        '''Method for getting the current text on the multi button.
        
        Returns
        -----------------------------------
        returns a string with the text currently on the button. 
'''
        return self.text[self.state]
    

