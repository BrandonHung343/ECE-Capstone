# Dealer UI

import pygame
import random
import math
import os

# Pygame Framework
class PygameGame(object):
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, fps=50, title="Dealer UI"):
        pygame.init()
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)

    def run(self):
        # General Intialization
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.title)

        self._keys = dict()

        # Poker Game Intialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

# Poker Game Class
class PokerGame(PygameGame):
    def init(self):
        # General
        self.gameMode = "configScreen"
        self.myFont = pygame.font.SysFont("Impact", 35)
        folder = os.path.dirname(os.path.realpath(__file__))

        # Config Screen 
        self.startButton = pygame.Rect(self.width/2-self.width/5, self.height/2-self.width/5, self.width/5, self.width/5)
        self.addDelButton = pygame.Rect(self.width/2, self.height/2-self.width/5, self.width/5, self.width/5)
        self.chipColorButton = pygame.Rect(self.width/2-self.width/5, self.height/2, self.width/5, self.width/5)
        self.stackSizeButton = pygame.Rect(self.width/2, self.height/2, self.width/5, self.width/5)

        # Play Game Screen
        self.potSize = 0
        self.dealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//10, self.width//10))
        self.pokerTable = pygame.Rect(self.width/10, self.height/10, self.width-self.width/5, self.height-self.height/5) 

    # Choose which Screen 
    def mousePressed(self, x, y):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenMousePressed(self, x, y)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameMousePressed(self, x, y)
    
    def keyPressed(self, code, mod):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenKeyPressed(self, code, mod)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameKeyPressed(self, code, mod)
    
    def timerFired(self, dt):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenTimerFired(self, dt)
        elif (self.gameMode == "playGame"):
            PokerGame.playGameTimerFired(self, dt)    
    
    def redrawAll(self, screen):
        if (self.gameMode == "configScreen"):
            PokerGame.configScreenRedrawAll(self, screen)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameRedrawAll(self, screen)
    
    # Configuartion Screen Functions
    def configScreenMousePressed(self, x, y):
        if self.startButton.collidepoint(x, y):
            self.gameMode = "playGame"
    
    def configScreenKeyPressed(self, code, mod):
        pass
  
    def configScreenTimerFired(self,dt):
        pass   
   
    def configScreenRedrawAll(self, screen):

        screen.fill((56,79,70))

        pygame.draw.rect(screen, (170, 25, 25), self.startButton)
        startGame = self.myFont.render("Start Game", True, (0,0,0))
        startGameBox = startGame.get_rect(center = self.startButton.center)
        screen.blit(startGame, startGameBox)

        pygame.draw.rect(screen, (25, 170, 25), self.addDelButton)
        addDel = self.myFont.render("Add/Del Players", True, (0,0,0))
        addDelBox = addDel.get_rect(center = self.addDelButton.center)
        screen.blit(addDel, addDelBox)

        pygame.draw.rect(screen, (25, 25, 170), self.chipColorButton)
        chipColor = self.myFont.render("Chip Colors", True, (0,0,0))
        chipColorBox = chipColor.get_rect(center = self.chipColorButton.center)
        screen.blit(chipColor, chipColorBox)

        pygame.draw.rect(screen, (170, 170, 170), self.stackSizeButton)
        stackSize = self.myFont.render("Stack Sizes", True, (0,0,0))
        stackSizeBox = stackSize.get_rect(center = self.stackSizeButton.center)
        screen.blit(stackSize, stackSizeBox)        
        
    # Play Game Screen Functions
    def playGameMousePressed(self, x ,y):
        pass

    def playGameKeyPressed(self, code, mod):
        if code == pygame.K_r:
            self.gameMode = "configScreen"
   
    def playGameTimerFired(self, dt):
        pass
  
    def playGameRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Table
        pygame.draw.ellipse(screen, (25, 100, 25), self.pokerTable)

        # Pot
        thePot = self.myFont.render("The Pot", True, (0,0,0))
        thePotBox = thePot.get_rect(center = (self.width/2, self.height/2-self.height/25))
        screen.blit(thePot, thePotBox)
        potSizeString = "$%d" % self.potSize
        potSize = self.myFont.render(potSizeString, True, (0,0,0))
        potSizeBox = potSize.get_rect(center = (self.width/2, self.height/2+self.height/25))
        screen.blit(potSize, potSizeBox)
        
        # Dealer 
        dealerRect = self.dealerChip.get_rect(center=(self.width/2,self.height/10))
        screen.blit(self.dealerChip, dealerRect)

        # Players 
        pygame.draw.circle(screen, (75, 75, 75), (self.width/3, self.height/6), self.width/20) # Player 1
        pygame.draw.circle(screen, (75, 75, 75), (self.width/6, self.height/3), self.width/20) # Player 2
        pygame.draw.circle(screen, (75, 75, 75), (self.width/6, self.height*2/3), self.width/20) # Player 3
        pygame.draw.circle(screen, (75, 75, 75), (self.width/3, self.height*5/6), self.width/20) # Player 4
        pygame.draw.circle(screen, (75, 75, 75), (self.width*2/3, self.height*5/6), self.width/20) # Player 5
        pygame.draw.circle(screen, (75, 75, 75), (self.width*5/6, self.height*2/3), self.width/20) # Player 6
        pygame.draw.circle(screen, (75, 75, 75), (self.width*5/6, self.height/3), self.width/20) # Player 7
        pygame.draw.circle(screen, (75, 75, 75), (self.width*2/3, self.height/6), self.width/20) # Player 8

PokerGame().run()