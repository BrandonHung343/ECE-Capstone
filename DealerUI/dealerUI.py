# Dealer UI
import sys
import pygame
import random
import math
import os
sys.path.insert(1, '../CompVision')
import CompVision
import config
from config import *
import serial


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

    def __init__(self, fps=50, title="Smart Poker"):
        pygame.init()
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)

    def run(self):
        # General Initialization
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.title)

        self._keys = dict()

        # Poker Game Initialization
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
        self.myFont = pygame.font.SysFont("Impact", self.width//40)
        self.smallFont = pygame.font.SysFont("Impact", self.width//80)
        self.titleFont = pygame.font.SysFont("Rubik", self.width//15)
        self.winFont = pygame.font.SysFont("Rubik", self.width//20)
        folder = os.path.dirname(os.path.realpath(__file__))

        # Servo
        #self.ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

        # Config Screen 
        self.startButton = pygame.Rect(self.width//2-self.width//5, self.height//2-self.width//5, self.width//5, self.width//5)
        self.addDelButton = pygame.Rect(self.width//2, self.height//2-self.width//5, self.width//5, self.width//5)
        self.chipColorButton = pygame.Rect(self.width//2-self.width//5, self.height//2, self.width//5, self.width//5)
        self.stackSizeButton = pygame.Rect(self.width//2, self.height//2, self.width//5, self.width//5)

        # Back Button 
        self.backRect = pygame.Rect(self.width//20, self.height//20, self.width//15, self.width//15)

        # Calibrate Button
        self.calibrateRect = pygame.Rect(self.width-self.width//10, self.height//20, self.width//15, self.width//15)

        # Chip Values
        self.whiteChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "whitechip.jpg")),(self.width//10, self.width//10))
        self.redChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "redchip.jpg")),(self.width//10, self.width//10))
        self.greenChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "greenchip.jpg")),(self.width//10, self.width//10))
        self.blueChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "bluechip.jpg")),(self.width//10, self.width//10))
        self.blackChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "blackchip.jpg")),(self.width//10, self.width//10))

        # Play Game
        self.bigDealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//10, self.width//10))
        self.dealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//30, self.width//30))
        self.pokerTable = pygame.Rect(self.width//10, self.height//10, self.width-self.width//5, self.height-self.height//5) 
        self.rotateButton = pygame.Rect(self.width-self.width//10, self.height//20, self.width//15, self.width//15)
        self.smallChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "small-blind.jpg")),(self.width//30, self.width//30))
        self.bigChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "bigblind.jpg")),(self.width//30, self.width//30))

        self.foldRect = pygame.Rect(self.width-self.width//10-self.width//15, self.height//8-self.width//15, self.width//15, self.width//15)
        self.raiseRect =pygame.Rect(self.width-self.width//10, self.height//8-self.width//15, self.width//15, self.width//15)
        self.checkRect = pygame.Rect(self.width-self.width//10-self.width//15, self.height//8, self.width//15, self.width//15)
        self.callRect = pygame.Rect(self.width-self.width//10, self.height//8, self.width//15, self.width//15)

        # Players
        self.player8Rect = pygame.Rect(self.width//3-self.width//20, self.height//6-self.width//20, self.width//10, self.width//10)
        self.player7Rect = pygame.Rect(self.width//6-self.width//20, self.height//3-self.width//20, self.width//10, self.width//10)
        self.player6Rect = pygame.Rect(self.width//6-self.width//20, self.height*2//3-self.width//20, self.width//10, self.width//10)
        self.player5Rect = pygame.Rect(self.width//3-self.width//20, self.height*5//6-self.width//20, self.width//10, self.width//10)
        self.player4Rect = pygame.Rect(self.width*2//3-self.width//20, self.height*5//6-self.width//20, self.width//10, self.width//10)
        self.player3Rect = pygame.Rect(self.width*5//6-self.width//20, self.height*2//3-self.width//20, self.width//10, self.width//10)
        self.player2Rect = pygame.Rect(self.width*5//6-self.width//20, self.height//3-self.width//20, self.width//10, self.width//10)
        self.player1Rect = pygame.Rect(self.width*2//3-self.width//20, self.height//6-self.width//20, self.width//10, self.width//10)

        # Add/Del Screen
        self.player1InputActive = False
        self.player2InputActive = False
        self.player3InputActive = False
        self.player4InputActive = False
        self.player5InputActive = False
        self.player6InputActive = False
        self.player7InputActive = False
        self.player8InputActive = False

        # Chip Color Screen
        self.whiteRect = self.whiteChip.get_rect(center=(self.width//4,self.height//3))
        self.redRect = self.redChip.get_rect(center=(self.width//2,self.height//3))
        self.greenRect = self.greenChip.get_rect(center=(self.width*3//4,self.height//3))
        self.blueRect = self.blueChip.get_rect(center=(self.width//4,self.height*2//3))
        self.blackRect = self.blackChip.get_rect(center=(self.width//2,self.height*2//3))
        self.BBRect = self.blackChip.get_rect(center=(self.width*3//4,self.height*2//3))

        self.whiteInputActive = False
        self.redInputActive = False
        self.greenInputActive = False
        self.blueInputActive = False
        self.blackInputActive = False
        self.BBInputActive = False

        self.tempWhiteNum = ""
        self.tempRedNum = ""
        self.tempGreenNum = ""
        self.tempBlueNum = ""
        self.tempBlackNum = ""
        self.tempBBNum = ""

        self.cvdat = CompVision.CVData(0, 2, 13.5, 120, config.chipValues)

        # Stack Sizes 
        self.tempStack1 = ""
        self.tempStack2 = ""
        self.tempStack3 = ""
        self.tempStack4 = "" 
        self.tempStack5 = ""
        self.tempStack6 = "" 
        self.tempStack7 = ""
        self.tempStack8 = ""

        self.stack1InputActive = False
        self.stack2InputActive = False
        self.stack3InputActive = False
        self.stack4InputActive = False
        self.stack5InputActive = False
        self.stack6InputActive = False
        self.stack7InputActive = False
        self.stack8InputActive = False

    # Choose which Screen 
    def mousePressed(self, x, y):      
        if (config.gameMode == "config"): 
            PokerGame.configScreenMousePressed(self, x, y)
        elif (config.gameMode == "playGame"):       
            PokerGame.playGameMousePressed(self, x, y)
        elif (config.gameMode == "addDel"):
            PokerGame.addDelMousePressed(self, x, y)
        elif (config.gameMode == "chipConfig"):
            PokerGame.chipConfigMousePressed(self, x, y)
        elif (config.gameMode == "stackSizes"):
            PokerGame.stackSizesMousePressed(self, x, y)
    
    def keyPressed(self, code, mod):
        if (config.gameMode == "config"): 
            PokerGame.configScreenKeyPressed(self, code, mod)
        elif (config.gameMode == "playGame"):       
            PokerGame.playGameKeyPressed(self, code, mod)
        elif (config.gameMode == "addDel"):
            PokerGame.addDelKeyPressed(self, code, mod)
        elif (config.gameMode == "chipConfig"):
            PokerGame.chipConfigKeyPressed(self, code, mod)
        elif (config.gameMode == "stackSizes"):
            PokerGame.stackSizesKeyPressed(self, code, mod)

    def timerFired(self, dt):
        if (config.gameMode == "config"): 
            PokerGame.configScreenTimerFired(self, dt)
        elif (config.gameMode == "playGame"):
            PokerGame.playGameTimerFired(self, dt)   
        elif (config.gameMode == "addDel"):
            PokerGame.addDelTimerFired(self, dt) 
        elif (config.gameMode == "chipConfig"):
            PokerGame.chipConfigTimerFired(self, dt)
        elif (config.gameMode == "stackSizes"):
            PokerGame.stackSizesTimerFired(self, dt)
    
    def redrawAll(self, screen):
        if (config.gameMode == "config"):
            PokerGame.configScreenRedrawAll(self, screen)
        elif (config.gameMode == "playGame"):       
            PokerGame.playGameRedrawAll(self, screen)
        elif (config.gameMode == "addDel"):
            PokerGame.addDelRedrawAll(self, screen)
        elif (config.gameMode == "chipConfig"):
            PokerGame.chipConfigRedrawAll(self, screen)
        elif (config.gameMode == "stackSizes"):
            PokerGame.stackSizesRedrawAll(self, screen)
    
    # Configuartion Screen Functions
    def configScreenMousePressed(self, x, y):
        if self.startButton.collidepoint(x, y):
            config.playerList[0].isPlaying
            listPlayers = [config.playerList[0].isPlaying, config.playerList[1].isPlaying, 
                             config.playerList[2].isPlaying, config.playerList[3].isPlaying,
                             config.playerList[4].isPlaying, config.playerList[5].isPlaying,
                             config.playerList[6].isPlaying, config.playerList[7].isPlaying]
            numPlayers = sum(listPlayers)
            if (numPlayers >= 3):
                config.gameMode = "playGame"
                self.initializeGame()

        elif self.addDelButton.collidepoint(x, y):
            config.gameMode = "addDel"
        elif self.chipColorButton.collidepoint(x, y):
            config.gameMode = "chipConfig"
        elif self.stackSizeButton.collidepoint(x, y):
            config.gameMode = "stackSizes"
    
    def configScreenKeyPressed(self, code, mod):
        pass
  
    def configScreenTimerFired(self,dt):
        pass   
   
    def configScreenRedrawAll(self, screen):
        screen.fill((56,79,70))

        # Title
        titleWords = self.titleFont.render("Smart Poker", True, (0,0,0))
        titleBox = titleWords.get_rect(center = (self.width//2, self.height//10))
        screen.blit(titleWords, titleBox)

        errorWords = self.smallFont.render("*Need at Least 3 Players to Start Game*", True, (255,0,0))
        errorBox = errorWords.get_rect(center = (self.width//2, self.height//6))
        listPlayers = [config.playerList[0].isPlaying, config.playerList[1].isPlaying, 
                             config.playerList[2].isPlaying, config.playerList[3].isPlaying,
                             config.playerList[4].isPlaying, config.playerList[5].isPlaying,
                             config.playerList[6].isPlaying, config.playerList[7].isPlaying]
        numPlayers = sum(listPlayers)
        if (numPlayers <= 2): screen.blit(errorWords, errorBox)

        # Start
        pygame.draw.rect(screen, (170, 25, 25), self.startButton)
        startGame = self.myFont.render("Start Game", True, (0,0,0))
        startGameBox = startGame.get_rect(center = self.startButton.center)
        screen.blit(startGame, startGameBox)

        # Add/Del
        pygame.draw.rect(screen, (25, 170, 25), self.addDelButton)
        addDel = self.myFont.render("Add/Del Players", True, (0,0,0))
        addDelBox = addDel.get_rect(center = self.addDelButton.center)
        screen.blit(addDel, addDelBox)

        # Chip Color
        pygame.draw.rect(screen, (25, 25, 170), self.chipColorButton)
        chipColor = self.myFont.render("Chip Configuartion", True, (0,0,0))
        chipColorBox = chipColor.get_rect(center = self.chipColorButton.center)
        screen.blit(chipColor, chipColorBox)

        # Stack Sizes
        pygame.draw.rect(screen, (170, 170, 170), self.stackSizeButton)
        stackSize = self.myFont.render("Stack Sizes", True, (0,0,0))
        stackSizeBox = stackSize.get_rect(center = self.stackSizeButton.center)
        screen.blit(stackSize, stackSizeBox)        

    # Add Delete Players
    def addDelMousePressed(self, x, y):
        self.player1InputActive = False
        self.player2InputActive = False
        self.player3InputActive = False
        self.player4InputActive = False
        self.player5InputActive = False
        self.player6InputActive = False
        self.player7InputActive = False
        self.player8InputActive = False

        if self.backRect.collidepoint(x, y):
            config.gameMode = "config"

        elif self.player1Rect.collidepoint(x, y):
            config.playerList[0].name = ""
            if config.playerList[0].isPlaying:
                config.playerList[0].isPlaying = False
                config.playerList[0].stackSize = 200
            else:
                self.player1InputActive = True
        
        elif self.player2Rect.collidepoint(x, y):
            config.playerList[1].name = ""
            if config.playerList[1].isPlaying:
                config.playerList[1].isPlaying = False
                config.playerList[1].stackSize = 200
            else:
                self.player2InputActive = True
        
        elif self.player3Rect.collidepoint(x, y):
            config.playerList[2].name = ""
            if config.playerList[2].isPlaying:
                config.playerList[2].isPlaying = False
                config.playerList[2].stackSize = 200
            else:
                self.player3InputActive = True
        
        elif self.player4Rect.collidepoint(x, y):
            config.playerList[3].name = ""
            if config.playerList[3].isPlaying:
                config.playerList[3].isPlaying = False
                config.playerList[3].stackSize = 200
            else:
                self.player4InputActive = True
        
        elif self.player5Rect.collidepoint(x, y):
            config.playerList[4].name = ""
            if config.playerList[4].isPlaying:
                config.playerList[4].isPlaying = False
                config.playerList[4].stackSize = 200
            else:
                self.player5InputActive = True

        elif self.player6Rect.collidepoint(x, y):
            config.playerList[5].name = ""
            if config.playerList[5].isPlaying:
                config.playerList[5].isPlaying = False
                config.playerList[5].stackSize = 200
            else:
                self.player6InputActive = True

        elif self.player7Rect.collidepoint(x, y):
            config.playerList[6].name = ""
            if config.playerList[6].isPlaying:
                config.playerList[6].isPlaying = False
                config.playerList[6].stackSize = 200
            else:
                self.player7InputActive = True

        elif self.player8Rect.collidepoint(x, y):
            config.playerList[7].name = ""
            if config.playerList[7].isPlaying:
                config.playerList[7].isPlaying = False
                config.playerList[7].stackSize = 200
            else:
                self.player8InputActive = True

    def addDelKeyPressed(self, code, mod):
        # Lower Case Letter
        if  len(pygame.key.name(code)) == 1: 
            if ord(pygame.key.name(code)) >= 97 and ord(pygame.key.name(code)) <= 122:
                letter = pygame.key.name(code)
                if self.player1InputActive:
                    config.playerList[0].name += letter
                if self.player2InputActive:
                    config.playerList[1].name += letter
                if self.player3InputActive:
                    config.playerList[2].name += letter
                if self.player4InputActive:
                    config.playerList[3].name += letter
                if self.player5InputActive:
                    config.playerList[4].name += letter
                if self.player6InputActive:
                    config.playerList[5].name += letter
                if self.player7InputActive:
                    config.playerList[6].name += letter
                if self.player8InputActive:
                    config.playerList[7].name += letter

        # Enter/Return
        elif code == pygame.K_RETURN:
            if self.player1InputActive:
                config.playerList[0].isPlaying = True
                self.player1InputActive = False

            elif self.player2InputActive:
                config.playerList[1].isPlaying = True
                self.player2InputActive = False

            elif self.player3InputActive:
                config.playerList[2].isPlaying = True
                self.player3InputActive = False

            elif self.player4InputActive:
                config.playerList[3].isPlaying = True
                self.player4InputActive = False

            elif self.player5InputActive:
                config.playerList[4].isPlaying = True
                self.player5InputActive = False

            elif self.player6InputActive:
                config.playerList[5].isPlaying = True
                self.player6InputActive = False

            elif self.player7InputActive:
                config.playerList[6].isPlaying = True
                self.player7InputActive = False

            elif self.player8InputActive:
                config.playerList[7].isPlaying = True
                self.player8InputActive = False
  
    def addDelTimerFired(self,dt):
        pass   
   
    def addDelRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Back
        pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("Back", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        screen.blit(backWords, backBox)

        # Table
        pygame.draw.ellipse(screen, (25, 100, 25), self.pokerTable)

        # Dealer 
        dealerRect = self.bigDealerChip.get_rect(center=(self.width//2,self.height//10))
        screen.blit(self.bigDealerChip, dealerRect)

        # Players 
        if self.player1InputActive: 
            pygame.draw.circle(screen, (100, 150, 100), self.player1Rect.center,self.width//20)
        elif config.playerList[0].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player1Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width//20)

        if self.player2InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player2Rect.center, self.width//20)
        elif config.playerList[1].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player2Rect.center,self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width//20)

        if self.player3InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player3Rect.center, self.width//20)
        elif config.playerList[2].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player3Rect.center,self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width//20)

        if self.player4InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player4Rect.center, self.width//20) 
        elif config.playerList[3].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player4Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width//20)
        
        if self.player5InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player5Rect.center, self.width//20)
        elif config.playerList[4].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player5Rect.center,self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width//20)
        
        if self.player6InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player6Rect.center, self.width//20) 
        elif config.playerList[5].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player6Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width//20)
        
        if self.player7InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player7Rect.center, self.width//20) 
        elif config.playerList[6].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player7Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width//20)

        if self.player8InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player8Rect.center, self.width//20) 
        elif config.playerList[7].isPlaying:
            pygame.draw.circle(screen, (255, 0, 0), self.player8Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width//20)
        

        removePlayer1 = self.myFont.render("Remove "+config.playerList[0].name, True, (0,0,0))
        removePlayer2 = self.myFont.render("Remove "+config.playerList[1].name, True, (0,0,0))
        removePlayer3 = self.myFont.render("Remove "+config.playerList[2].name, True, (0,0,0))
        removePlayer4 = self.myFont.render("Remove "+config.playerList[3].name, True, (0,0,0))
        removePlayer5 = self.myFont.render("Remove "+config.playerList[4].name, True, (0,0,0))
        removePlayer6 = self.myFont.render("Remove "+config.playerList[5].name, True, (0,0,0))
        removePlayer7 = self.myFont.render("Remove "+config.playerList[6].name, True, (0,0,0))
        removePlayer8 = self.myFont.render("Remove "+config.playerList[7].name, True, (0,0,0))

        removePlayer1Box = removePlayer1.get_rect(center = self.player1Rect.center)
        removePlayer2Box = removePlayer2.get_rect(center = self.player2Rect.center)
        removePlayer3Box = removePlayer3.get_rect(center = self.player3Rect.center)
        removePlayer4Box = removePlayer4.get_rect(center = self.player4Rect.center)
        removePlayer5Box = removePlayer5.get_rect(center = self.player5Rect.center)
        removePlayer6Box = removePlayer6.get_rect(center = self.player6Rect.center)
        removePlayer7Box = removePlayer7.get_rect(center = self.player7Rect.center)
        removePlayer8Box = removePlayer8.get_rect(center = self.player8Rect.center)

        addText = self.myFont.render("Add Player", True, (0,0,0))
        player1AddBox = addText.get_rect(center = self.player1Rect.center)
        player2AddBox = addText.get_rect(center = self.player2Rect.center)
        player3AddBox = addText.get_rect(center = self.player3Rect.center)
        player4AddBox = addText.get_rect(center = self.player4Rect.center)
        player5AddBox = addText.get_rect(center = self.player5Rect.center)
        player6AddBox = addText.get_rect(center = self.player6Rect.center)
        player7AddBox = addText.get_rect(center = self.player7Rect.center)
        player8AddBox = addText.get_rect(center = self.player8Rect.center)

        inputText1 = self.myFont.render("Input Name : "+config.playerList[0].name, True, (0,0,0))
        inputText2 = self.myFont.render("Input Name : "+config.playerList[1].name, True, (0,0,0))
        inputText3 = self.myFont.render("Input Name : "+config.playerList[2].name, True, (0,0,0))
        inputText4 = self.myFont.render("Input Name : "+config.playerList[3].name, True, (0,0,0))
        inputText5 = self.myFont.render("Input Name : "+config.playerList[4].name, True, (0,0,0))
        inputText6 = self.myFont.render("Input Name : "+config.playerList[5].name, True, (0,0,0))
        inputText7 = self.myFont.render("Input Name : "+config.playerList[6].name, True, (0,0,0))
        inputText8 = self.myFont.render("Input Name : "+config.playerList[7].name, True, (0,0,0))

        inputBox1 = inputText1.get_rect(center = self.player1Rect.center)
        inputBox2 = inputText2.get_rect(center = self.player2Rect.center)
        inputBox3 = inputText3.get_rect(center = self.player3Rect.center)
        inputBox4 = inputText4.get_rect(center = self.player4Rect.center)
        inputBox5 = inputText5.get_rect(center = self.player5Rect.center)
        inputBox6 = inputText6.get_rect(center = self.player6Rect.center)
        inputBox7 = inputText7.get_rect(center = self.player7Rect.center)
        inputBox8 = inputText8.get_rect(center = self.player8Rect.center)

        if config.playerList[0].isPlaying: 
            screen.blit(removePlayer1, removePlayer1Box)
        elif self.player1InputActive:
            screen.blit(inputText1, inputBox1)
        else: 
            screen.blit(addText, player1AddBox)

        if config.playerList[1].isPlaying: 
            screen.blit(removePlayer2, removePlayer2Box)
        elif self.player2InputActive:
            screen.blit(inputText2, inputBox2)
        else: 
            screen.blit(addText, player2AddBox)

        if config.playerList[2].isPlaying: 
            screen.blit(removePlayer3, removePlayer3Box)
        elif self.player3InputActive:
            screen.blit(inputText3, inputBox3)
        else: 
            screen.blit(addText, player3AddBox)
            
        if config.playerList[3].isPlaying: 
            screen.blit(removePlayer4, removePlayer4Box)
        elif self.player4InputActive:
            screen.blit(inputText4, inputBox4)
        else: 
            screen.blit(addText, player4AddBox)
            
        if config.playerList[4].isPlaying: 
            screen.blit(removePlayer5, removePlayer5Box)
        elif self.player5InputActive:
            screen.blit(inputText5, inputBox5)
        else: 
            screen.blit(addText, player5AddBox)
            
        if config.playerList[5].isPlaying: 
            screen.blit(removePlayer6, removePlayer6Box)
        elif self.player6InputActive:
            screen.blit(inputText6, inputBox6)
        else: 
            screen.blit(addText, player6AddBox)
        
        if config.playerList[6].isPlaying: 
            screen.blit(removePlayer7, removePlayer7Box)
        elif self.player7InputActive:
            screen.blit(inputText7, inputBox7)
        else: 
            screen.blit(addText, player7AddBox)
        
        if config.playerList[7].isPlaying: 
            screen.blit(removePlayer8, removePlayer8Box)
        elif self.player8InputActive:
            screen.blit(inputText8, inputBox8)
        else: 
            screen.blit(addText, player8AddBox)

    # Play Game Screen Functions
    def playGameMousePressed(self, x ,y):
        # Regular Game
        if not config.winState:  
            # End Game Button
            if self.backRect.collidepoint(x, y):
                for player in config.playerList:
                    if (len(player.betList) != 0):
                        player.stackSize += player.betList[-1]

                config.gameMode = "config"

            # Fold
            if self.foldRect.collidepoint(x, y):
                currP = config.currPlayers[0]
                config.playerList[currP].inHand = False
                config.currPlayers = config.currPlayers[1:]

                # End of Game 
                if (len(config.currPlayers) == 1):
                    config.playerList[config.currPlayers[0]].stackSize += config.potSize
                    self.initializeGame()

                # Not End of Game
                else:
                    # Check End Round
                    if (config.currPlayers[0] == config.endPlayer):
                        self.endRound()

                    # If End Player Folds (Edge Case)
                    if (currP == config.endPlayer):
                        config.endPlayer = config.currPlayers[0]

                    # Rotate Servo 
                    self.rotateServo()


            # Raise   
            if self.raiseRect.collidepoint(x, y):
                currP = config.currPlayers[0]

                # Update Bets
                bet = 2 if (config.maxBet == 0) else 2*config.maxBet # Will change with CV
                config.maxBet = bet
                self.updateBetList(currP, bet)

                # Update Order of Curr Players
                tmpList = config.currPlayers[1:]+config.currPlayers[:1]
                config.currPlayers = tmpList
                config.endPlayer = currP

                # Rotate Servo
                self.rotateServo()

            # Check
            if self.checkRect.collidepoint(x, y): 
                currP = config.currPlayers[0]
                playerBetList = config.playerList[currP].betList

                # Empty Bet List
                if (len(playerBetList) == 0):
                    if (config.maxBet == 0):
                        tmpList = config.currPlayers[1:]+config.currPlayers[:1]
                        config.currPlayers = tmpList

                        if (config.currPlayers[0] == config.endPlayer):
                            self.endRound()
                # Not Empty Bet List
                else: 
                    if (playerBetList[-1] == config.maxBet):
                        tmpList = config.currPlayers[1:]+config.currPlayers[:1]
                        config.currPlayers = tmpList

                        if (config.currPlayers[0] == config.endPlayer):
                            self.endRound()

                # Rotate Servo
                self.rotateServo()

            # Call    
            if self.callRect.collidepoint(x, y):
                currP = config.currPlayers[0]

                # Update Bets
                self.updateBetList(currP, config.maxBet)

                # Update Order of Curr Players
                tmpList = config.currPlayers[1:]+config.currPlayers[:1]
                config.currPlayers = tmpList

                if (config.currPlayers[0] == config.endPlayer):
                    self.endRound()

                # Rotate Servo
                self.rotateServo()
        
        # Win State
        else:
            if self.player1Rect.collidepoint(x, y) and config.playerList[0].inHand:
                config.playerList[0].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player2Rect.collidepoint(x, y) and config.playerList[1].inHand:
                config.playerList[1].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player3Rect.collidepoint(x, y) and config.playerList[2].inHand:
                config.playerList[2].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player4Rect.collidepoint(x, y) and config.playerList[3].inHand:
                config.playerList[3].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player5Rect.collidepoint(x, y) and config.playerList[4].inHand:
                config.playerList[4].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player6Rect.collidepoint(x, y) and config.playerList[5].inHand:
                config.playerList[5].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player7Rect.collidepoint(x, y) and config.playerList[6].inHand:
                config.playerList[6].stackSize += config.potSize
                config.winState = False
                self.initializeGame()

            if self.player8Rect.collidepoint(x, y) and config.playerList[7].inHand:
                config.playerList[7].stackSize += config.potSize
                config.winState = False
                self.initializeGame()


    def playGameKeyPressed(self, code, mod):
        pass
   
    def playGameTimerFired(self, dt):
        pass
  
    def playGameRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Actions 
        if not config.winState: pygame.draw.rect(screen, (170, 25, 25), self.foldRect)
        if not config.winState: pygame.draw.rect(screen, (25, 170, 25), self.raiseRect)
        if not config.winState: pygame.draw.rect(screen, (25, 25, 170), self.checkRect)
        if not config.winState: pygame.draw.rect(screen, (170, 170, 170), self.callRect)
        foldWords = self.smallFont.render("Fold", True, (0,0,0))
        raiseWords = self.smallFont.render("Raise", True, (0,0,0))
        checkWords = self.smallFont.render("Check", True, (0,0,0))
        callWords = self.smallFont.render("Call", True, (0,0,0))
        foldBox = foldWords.get_rect(center = self.foldRect.center)
        raiseBox = raiseWords.get_rect(center = self.raiseRect.center)
        checkBox = checkWords.get_rect(center = self.checkRect.center)
        callBox = callWords.get_rect(center = self.callRect.center)
        if not config.winState: screen.blit(foldWords, foldBox)
        if not config.winState: screen.blit(raiseWords, raiseBox)
        if not config.winState: screen.blit(checkWords, checkBox)
        if not config.winState: screen.blit(callWords, callBox)

        # Back
        if not config.winState: pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("End Game", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        if not config.winState: screen.blit(backWords, backBox)

        # Rotate Button
        '''pygame.draw.rect(screen, (75, 50, 150), self.rotateButton)
        rotateWords = self.myFont.render("Rotate", True, (0,0,0))
        rotateBox = rotateWords.get_rect(center = self.rotateButton.center)
        screen.blit(rotateWords, rotateBox)'''
        
        # Table
        pygame.draw.ellipse(screen, (25, 100, 25), self.pokerTable)

        # Round
        gameWords = self.myFont.render(config.roundMode, True, (0,0,0))
        gameBox = gameWords.get_rect(center = (self.width//2, self.height//2-(4*self.height//25)))
        if not config.winState: screen.blit(gameWords, gameBox)
        
        '''# Debug
        debugStuff = ""
        for x in config.currPlayers:
            debugStuff+=str(x)
        debugStuff+= " Small Blind = "+str(config.smallBlind)+" End Player = "+str(config.endPlayer)+" Round = "+config.roundMode
        thePot = self.myFont.render(debugStuff, True, (0,0,0))
        thePotBox = thePot.get_rect(center = (self.width//2, self.height//2-self.height//25))
        screen.blit(thePot, thePotBox)
        potSizeString = "$%d" % config.potSize
        potSize = self.myFont.render(potSizeString, True, (0,0,0))
        potSizeBox = potSize.get_rect(center = (self.width//2, self.height//2+self.height//25))
        screen.blit(potSize, potSizeBox)'''

        # Pot
        potWords = "Pot"
        thePot = self.myFont.render(potWords, True, (0,0,0))
        thePotBox = thePot.get_rect(center = (self.width//2, self.height//2-self.height//25))
        screen.blit(thePot, thePotBox)

        potSizeString = "$%d" % config.potSize
        potSize = self.myFont.render(potSizeString, True, (0,0,0))
        potSizeBox = potSize.get_rect(center = (self.width//2, self.height//2+self.height//25))
        screen.blit(potSize, potSizeBox)

        # Win State
        winWords = "Round Over! Select Winner"
        theWin = self.winFont.render(winWords, True, (0, 150, 250))
        theWinBox = theWin.get_rect(center = (self.width//2, self.height//2-(4*self.height//25)))
        if config.winState: screen.blit(theWin, theWinBox)
        
        # Dealer 
        dealerRect = self.bigDealerChip.get_rect(center=(self.width//2,self.height//10))
        screen.blit(self.bigDealerChip, dealerRect)

        dealer1Rect = self.dealerChip.get_rect(center = (self.player1Rect.x, self.player1Rect.y+self.player1Rect.h))
        dealer2Rect = self.dealerChip.get_rect(center = (self.player2Rect.x, self.player2Rect.y+self.player2Rect.h))
        dealer3Rect = self.dealerChip.get_rect(center = (self.player3Rect.x, self.player3Rect.y+self.player3Rect.h))
        dealer4Rect = self.dealerChip.get_rect(center = (self.player4Rect.x, self.player4Rect.y+self.player4Rect.h))
        dealer5Rect = self.dealerChip.get_rect(center = (self.player5Rect.x, self.player5Rect.y+self.player5Rect.h))
        dealer6Rect = self.dealerChip.get_rect(center = (self.player6Rect.x, self.player6Rect.y+self.player6Rect.h))
        dealer7Rect = self.dealerChip.get_rect(center = (self.player7Rect.x, self.player7Rect.y+self.player7Rect.h))
        dealer8Rect = self.dealerChip.get_rect(center = (self.player8Rect.x, self.player8Rect.y+self.player8Rect.h))
        
        # Players
        player1Name = self.myFont.render(config.playerList[0].name, True, (0,0,0))
        player2Name = self.myFont.render(config.playerList[1].name, True, (0,0,0))
        player3Name = self.myFont.render(config.playerList[2].name, True, (0,0,0))
        player4Name = self.myFont.render(config.playerList[3].name, True, (0,0,0))
        player5Name = self.myFont.render(config.playerList[4].name, True, (0,0,0))
        player6Name = self.myFont.render(config.playerList[5].name, True, (0,0,0))
        player7Name = self.myFont.render(config.playerList[6].name, True, (0,0,0))
        player8Name = self.myFont.render(config.playerList[7].name, True, (0,0,0))

        player1Stack = self.myFont.render("$"+str(config.playerList[0].stackSize), True, (0,0,0))
        player2Stack = self.myFont.render("$"+str(config.playerList[1].stackSize), True, (0,0,0))
        player3Stack = self.myFont.render("$"+str(config.playerList[2].stackSize), True, (0,0,0))
        player4Stack = self.myFont.render("$"+str(config.playerList[3].stackSize), True, (0,0,0))
        player5Stack = self.myFont.render("$"+str(config.playerList[4].stackSize), True, (0,0,0))
        player6Stack = self.myFont.render("$"+str(config.playerList[5].stackSize), True, (0,0,0))
        player7Stack = self.myFont.render("$"+str(config.playerList[6].stackSize), True, (0,0,0))
        player8Stack = self.myFont.render("$"+str(config.playerList[7].stackSize), True, (0,0,0))

        player1NameBox = player1Name.get_rect(center = (self.player1Rect.x+self.player1Rect.w//2, self.player1Rect.y+self.player1Rect.h//4))
        player2NameBox = player2Name.get_rect(center = (self.player2Rect.x+self.player2Rect.w//2, self.player2Rect.y+self.player2Rect.h//4))
        player3NameBox = player3Name.get_rect(center = (self.player3Rect.x+self.player3Rect.w//2, self.player3Rect.y+self.player3Rect.h//4))
        player4NameBox = player4Name.get_rect(center = (self.player4Rect.x+self.player4Rect.w//2, self.player4Rect.y+self.player4Rect.h//4))
        player5NameBox = player5Name.get_rect(center = (self.player5Rect.x+self.player5Rect.w//2, self.player5Rect.y+self.player5Rect.h//4))
        player6NameBox = player6Name.get_rect(center = (self.player6Rect.x+self.player6Rect.w//2, self.player6Rect.y+self.player6Rect.h//4))
        player7NameBox = player7Name.get_rect(center = (self.player7Rect.x+self.player7Rect.w//2, self.player7Rect.y+self.player7Rect.h//4))
        player8NameBox = player8Name.get_rect(center = (self.player8Rect.x+self.player8Rect.w//2, self.player8Rect.y+self.player8Rect.h//4))

        stack1Box = player1Stack.get_rect(center = (self.player1Rect.x+self.player1Rect.w//2, self.player1Rect.y+self.player1Rect.h*3//4))
        stack2Box = player2Stack.get_rect(center = (self.player2Rect.x+self.player2Rect.w//2, self.player2Rect.y+self.player2Rect.h*3//4))
        stack3Box = player3Stack.get_rect(center = (self.player3Rect.x+self.player3Rect.w//2, self.player3Rect.y+self.player3Rect.h*3//4))
        stack4Box = player4Stack.get_rect(center = (self.player4Rect.x+self.player4Rect.w//2, self.player4Rect.y+self.player4Rect.h*3//4))
        stack5Box = player5Stack.get_rect(center = (self.player5Rect.x+self.player5Rect.w//2, self.player5Rect.y+self.player5Rect.h*3//4))
        stack6Box = player6Stack.get_rect(center = (self.player6Rect.x+self.player6Rect.w//2, self.player6Rect.y+self.player6Rect.h*3//4))
        stack7Box = player7Stack.get_rect(center = (self.player7Rect.x+self.player7Rect.w//2, self.player7Rect.y+self.player7Rect.h*3//4))
        stack8Box = player8Stack.get_rect(center = (self.player8Rect.x+self.player8Rect.w//2, self.player8Rect.y+self.player8Rect.h*3//4))

        if config.playerList[0].isPlaying: 
            if (config.currPlayers[0] == 0): 
                pygame.draw.circle(screen, (100, 150, 100), self.player1Rect.center, self.width//20)
            elif (config.playerList[0].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width//20)    
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player1Rect.center, self.width//20)
            screen.blit(player1Name, player1NameBox)
            screen.blit(player1Stack, stack1Box)

        if config.playerList[1].isPlaying:
            if (config.currPlayers[0] == 1): 
                pygame.draw.circle(screen, (100, 150, 100), self.player2Rect.center, self.width//20)
            elif (config.playerList[1].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player2Rect.center, self.width//20)
            screen.blit(player2Name, player2NameBox)
            screen.blit(player2Stack, stack2Box)

        if config.playerList[2].isPlaying: 
            if (config.currPlayers[0] == 2): 
                pygame.draw.circle(screen, (100, 150, 100), self.player3Rect.center, self.width//20)
            elif (config.playerList[2].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player3Rect.center, self.width//20)
            screen.blit(player3Name, player3NameBox)
            screen.blit(player3Stack, stack3Box)
            
        if config.playerList[3].isPlaying: 
            if (config.currPlayers[0] == 3): 
                pygame.draw.circle(screen, (100, 150, 100), self.player4Rect.center, self.width//20)
            elif (config.playerList[3].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player4Rect.center, self.width//20)
            screen.blit(player4Name, player4NameBox)
            screen.blit(player4Stack, stack4Box)
            
        if config.playerList[4].isPlaying: 
            if (config.currPlayers[0] == 4): 
                pygame.draw.circle(screen, (100, 150, 100), self.player5Rect.center, self.width//20)
            elif (config.playerList[4].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player5Rect.center, self.width//20)
            screen.blit(player5Name, player5NameBox)
            screen.blit(player5Stack, stack5Box)
            
        if config.playerList[5].isPlaying:
            if (config.currPlayers[0] == 5): 
                pygame.draw.circle(screen, (100, 150, 100), self.player6Rect.center, self.width//20)
            elif (config.playerList[5].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player6Rect.center, self.width//20)
            screen.blit(player6Name, player6NameBox)
            screen.blit(player6Stack, stack6Box)
        
        if config.playerList[6].isPlaying:           
            if (config.currPlayers[0] == 6): 
                pygame.draw.circle(screen, (100, 150, 100), self.player7Rect.center, self.width//20)
            elif (config.playerList[6].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player7Rect.center, self.width//20)
            screen.blit(player7Name, player7NameBox)
            screen.blit(player7Stack, stack7Box)
        
        if config.playerList[7].isPlaying:
            if (config.currPlayers[0] == 7): 
                pygame.draw.circle(screen, (100, 150, 100), self.player8Rect.center, self.width//20)
            elif (config.playerList[7].inHand):
                pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width//20)
            else:
                pygame.draw.circle(screen, (170, 25, 25), self.player8Rect.center, self.width//20)
            screen.blit(player8Name, player8NameBox)
            screen.blit(player8Stack, stack8Box)

        # Small Blind Chip
        if config.smallBlind == 0: screen.blit(self.smallChip, dealer1Rect)
        if config.smallBlind == 1: screen.blit(self.smallChip, dealer2Rect)
        if config.smallBlind == 2: screen.blit(self.smallChip, dealer3Rect)
        if config.smallBlind == 3: screen.blit(self.smallChip, dealer4Rect)
        if config.smallBlind == 4: screen.blit(self.smallChip, dealer5Rect)
        if config.smallBlind == 5: screen.blit(self.smallChip, dealer6Rect)
        if config.smallBlind == 6: screen.blit(self.smallChip, dealer7Rect)
        if config.smallBlind == 7: screen.blit(self.smallChip, dealer8Rect)

        # Big Blind Chip  
        if config.bigBlind == 0: screen.blit(self.bigChip, dealer1Rect)
        if config.bigBlind == 1: screen.blit(self.bigChip, dealer2Rect)
        if config.bigBlind == 2: screen.blit(self.bigChip, dealer3Rect)
        if config.bigBlind == 3: screen.blit(self.bigChip, dealer4Rect)
        if config.bigBlind == 4: screen.blit(self.bigChip, dealer5Rect)
        if config.bigBlind == 5: screen.blit(self.bigChip, dealer6Rect)
        if config.bigBlind == 6: screen.blit(self.bigChip, dealer7Rect)
        if config.bigBlind == 7: screen.blit(self.bigChip, dealer8Rect)


    # Chip Config
    def chipConfigMousePressed(self, x, y):
        self.whiteInputActive = False
        self.redInputActive = False
        self.greenInputActive = False
        self.blueInputActive = False
        self.blackInputActive = False
        self.BBInputActive = False

        if self.backRect.collidepoint(x, y):
            config.gameMode = "config"

        elif self.calibrateRect.collidepoint(x, y):
            # Call calibrate function
            self.cvdat = CompVision.CVData(0, 2, 13.5, 120, config.chipValues)
            self.cvdat = CompVision.calibrate(self.cvdat)

        elif self.whiteRect.collidepoint(x, y):
            self.tempWhiteNum = ""
            self.whiteInputActive = True

        elif self.redRect.collidepoint(x, y):
            self.tempRedNum = ""
            self.redInputActive = True

        elif self.greenRect.collidepoint(x, y):
            self.tempGreenNum = ""
            self.greenInputActive = True
        
        elif self.blueRect.collidepoint(x, y):
            self.tempBlueNum = ""
            self.blueInputActive = True
        
        elif self.blackRect.collidepoint(x, y):
            self.tempBlackNum = ""
            self.blackInputActive = True
        
        elif self.BBRect.collidepoint(x, y):
            self.tempBBNum = ""
            self.BBInputActive = True

    
    def chipConfigKeyPressed(self, code, mod):
        # Numbers
        if  len(pygame.key.name(code)) == 1: 
            if ord(pygame.key.name(code)) >= 48 and ord(pygame.key.name(code)) <= 57:
                number = pygame.key.name(code)
                if self.whiteInputActive:
                    self.tempWhiteNum += number
                if self.redInputActive:
                    self.tempRedNum += number
                if self.greenInputActive:
                    self.tempGreenNum += number
                if self.blueInputActive:
                    self.tempBlueNum += number
                if self.blackInputActive:
                    self.tempBlackNum += number
                if self.BBInputActive:
                    self.tempBBNum += number
                

        # Enter/Return
        elif code == pygame.K_RETURN:
            if self.whiteInputActive:
                self.whiteInputActive = False
                config.chipValues[0] = int(self.tempWhiteNum)
                self.tempWhiteNum = ""

            elif self.redInputActive:
                self.redInputActive = False
                config.chipValues[1] = int(self.tempRedNum)
                self.tempRedNum = ""

            elif self.greenInputActive:
                self.greenInputActive = False
                config.chipValues[2] = int(self.tempGreenNum)
                self.tempGreenNum = ""

            elif self.blueInputActive:
                self.blueInputActive = False
                config.chipValues[3] = int(self.tempBlueNum)
                self.tempBlueNum = ""

            elif self.blackInputActive:
                self.blackInputActive = False
                config.chipValues[4] = int(self.tempBlackNum)
                self.tempBlackNum = ""

            elif self.BBInputActive:
                self.BBInputActive = False
                config.BBVal = int(self.tempBBNum)
                self.tempBBNum = ""

           
    def chipConfigTimerFired(self,dt):
        pass   
   
    def chipConfigRedrawAll(self, screen):
        screen.fill((56,79,70))

        # Back
        pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("Back", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        screen.blit(backWords, backBox)

        # Calibrate
        pygame.draw.rect(screen, (100, 60, 50), self.calibrateRect)
        calibrateWords = self.myFont.render("Calibrate", True, (0,0,0))
        calibrateBox = calibrateWords.get_rect(center = self.calibrateRect.center)
        screen.blit(calibrateWords, calibrateBox)

        # Edit
        color1 = (115, 115, 115)
        color2 = (115, 115, 115)
        color3 = (115, 115, 115)
        color4 = (115, 115, 115)
        color5 = (115, 115, 115) 
        color6 = (115, 115, 115)
        if self.whiteInputActive: color1 = (100, 150, 100)
        if self.redInputActive: color2 = (100, 150, 100)
        if self.greenInputActive: color3 = (100, 150, 100)
        if self.blueInputActive: color4 = (100, 150, 100)
        if self.blackInputActive: color5 = (100, 150, 100)
        if self.BBInputActive: color6 = (100, 150, 100)
        pygame.draw.rect(screen, color1, self.whiteRect)
        pygame.draw.rect(screen, color2, self.redRect)
        pygame.draw.rect(screen, color3, self.greenRect)
        pygame.draw.rect(screen, color4, self.blueRect)
        pygame.draw.rect(screen, color5, self.blackRect)
        pygame.draw.rect(screen, color6, self.BBRect)

        clickWords = self.titleFont.render("Click to Edit Chip Values", True, (0,0,0))
        clickBox = clickWords.get_rect(center = (self.width//2, self.height//8))
        screen.blit(clickWords, clickBox)

        whiteNum = self.myFont.render(str(config.chipValues[0]), True, (0,0,175))
        redNum = self.myFont.render(str(config.chipValues[1]), True, (0,0,175))
        greenNum = self.myFont.render(str(config.chipValues[2]), True, (0,0,175))
        blueNum = self.myFont.render(str(config.chipValues[3]), True, (0,0,175))
        blackNum = self.myFont.render(str(config.chipValues[4]), True, (0,0,175))
        BBNum = self.myFont.render(str(config.BBVal), True, (0,0,175))

        tempWhite = self.myFont.render(self.tempWhiteNum, True, (0,0,175))
        tempRed = self.myFont.render(self.tempRedNum, True, (0,0,175))
        tempGreen = self.myFont.render(self.tempGreenNum, True, (0,0,175))
        tempBlue = self.myFont.render(self.tempBlueNum, True, (0,0,175))
        tempBlack = self.myFont.render(self.tempBlackNum, True, (0,0,175))
        tempBB = self.myFont.render(self.tempBBNum, True, (0,0,175))
        
        whiteWords = self.myFont.render("Chip 1 Value:", True, (0,0,0))
        redWords = self.myFont.render("Chip 2 Value:", True, (0,0,0))
        greenWords = self.myFont.render("Chip 3 Value:", True, (0,0,0))
        blueWords = self.myFont.render("Chip 4 Value:", True, (0,0,0))
        blackWords = self.myFont.render("Chip 5 Value:", True, (0,0,0))
        BBWords = self.myFont.render("Big Blind Value:", True, (0,0,0))

        whiteBox2 = whiteWords.get_rect(center = (self.whiteRect.x+self.whiteRect.w//2, self.whiteRect.y+self.whiteRect.h//4))
        whiteBox = whiteNum.get_rect(center = (self.whiteRect.x+self.whiteRect.w//2, self.whiteRect.y+self.whiteRect.h*3//4))
        redBox2 = redWords.get_rect(center = (self.redRect.x+self.redRect.w//2, self.redRect.y+self.redRect.h//4))
        redBox = redNum.get_rect(center = (self.redRect.x+self.redRect.w//2, self.redRect.y+self.redRect.h*3//4))
        greenBox2 = greenWords.get_rect(center = (self.greenRect.x+self.greenRect.w//2, self.greenRect.y+self.greenRect.h//4))
        greenBox = greenNum.get_rect(center = (self.greenRect.x+self.greenRect.w//2, self.greenRect.y+self.greenRect.h*3//4))
        blueBox2 = blueWords.get_rect(center = (self.blueRect.x+self.blueRect.w//2, self.blueRect.y+self.blueRect.h//4))
        blueBox = blueNum.get_rect(center = (self.blueRect.x+self.blueRect.w//2, self.blueRect.y+self.blueRect.h*3//4))
        blackBox2 = blackWords.get_rect(center = (self.blackRect.x+self.blackRect.w//2, self.blackRect.y+self.blackRect.h//4))
        blackBox = blackNum.get_rect(center = (self.blackRect.x+self.blackRect.w//2, self.blackRect.y+self.blackRect.h*3//4))
        BBBox2 = BBWords.get_rect(center = (self.BBRect.x+self.BBRect.w//2, self.BBRect.y+self.BBRect.h//4))
        BBBox = BBNum.get_rect(center = (self.BBRect.x+self.BBRect.w//2, self.BBRect.y+self.BBRect.h*3//4))

        screen.blit(whiteWords, whiteBox2)
        screen.blit(redWords, redBox2)
        screen.blit(greenWords, greenBox2)
        screen.blit(blueWords, blueBox2)
        screen.blit(blackWords, blackBox2)
        screen.blit(BBWords, BBBox2)

        if self.whiteInputActive:
            screen.blit(tempWhite, whiteBox)
        else:
            screen.blit(whiteNum, whiteBox)

        if self.redInputActive:
            screen.blit(tempRed, redBox)
        else:
            screen.blit(redNum, redBox)

        if self.greenInputActive:
            screen.blit(tempGreen, greenBox)
        else:
            screen.blit(greenNum, greenBox)

        if self.blueInputActive:
            screen.blit(tempBlue, blueBox)
        else:
            screen.blit(blueNum, blueBox)

        if self.blackInputActive:
            screen.blit(tempBlack, blackBox)
        else:
            screen.blit(blackNum, blackBox)

        if self.BBInputActive:
            screen.blit(tempBB, BBBox)
        else:
            screen.blit(BBNum, BBBox)

    # Stack Sizes
    def stackSizesMousePressed(self, x, y):
        self.stack1InputActive = False
        self.stack2InputActive = False
        self.stack3InputActive = False
        self.stack4InputActive = False
        self.stack5InputActive = False
        self.stack6InputActive = False
        self.stack7InputActive = False
        self.stack8InputActive = False

        if self.backRect.collidepoint(x, y):
            config.gameMode = "config"

        elif self.player1Rect.collidepoint(x, y) and config.playerList[0].isPlaying:
            self.tempStack1 = ""
            self.stack1InputActive = True
        
        elif self.player2Rect.collidepoint(x, y) and config.playerList[1].isPlaying:
            self.tempStack2 = ""
            self.stack2InputActive = True
        
        elif self.player3Rect.collidepoint(x, y) and config.playerList[2].isPlaying:
            self.tempStack3 = ""
            self.stack3InputActive = True
        
        elif self.player4Rect.collidepoint(x, y) and config.playerList[3].isPlaying:
            self.tempStack4 = ""
            self.stack4InputActive = True
        
        elif self.player5Rect.collidepoint(x, y) and config.playerList[4].isPlaying:
            self.tempStack5 = ""
            self.stack5InputActive = True
        
        elif self.player6Rect.collidepoint(x, y) and config.playerList[5].isPlaying:
            self.tempStack6 = ""
            self.stack6InputActive = True
        
        elif self.player7Rect.collidepoint(x, y) and config.playerList[6].isPlaying:
            self.tempStack7 = ""
            self.stack7InputActive = True

        elif self.player8Rect.collidepoint(x, y) and config.playerList[7].isPlaying:
            self.tempStack8 = ""
            self.stack8InputActive = True
    
    def stackSizesKeyPressed(self, code, mod):
        # Numbers
        if  len(pygame.key.name(code)) == 1: 
            if ord(pygame.key.name(code)) >= 48 and ord(pygame.key.name(code)) <= 57:
                number = pygame.key.name(code)
                if self.stack1InputActive:
                    self.tempStack1 += number
                if self.stack2InputActive:
                    self.tempStack2 += number
                if self.stack3InputActive:
                    self.tempStack3 += number
                if self.stack4InputActive:
                    self.tempStack4 += number
                if self.stack5InputActive:
                    self.tempStack5 += number
                if self.stack6InputActive:
                    self.tempStack6 += number
                if self.stack7InputActive:
                    self.tempStack7 += number
                if self.stack8InputActive:
                    self.tempStack8 += number
                
        # Enter/Return
        elif code == pygame.K_RETURN:
            if self.stack1InputActive:
                self.stack1InputActive = False
                if (self.tempStack1 != ""): config.playerList[0].stackSize = int(self.tempStack1)
                self.tempStack1 = ""

            elif self.stack2InputActive:
                self.stack2InputActive = False
                if (self.tempStack2 != ""): config.playerList[1].stackSize = int(self.tempStack2)
                self.tempStack2 = ""

            elif self.stack3InputActive:
                self.stack3InputActive = False
                if (self.tempStack3 != ""): config.playerList[2].stackSize = int(self.tempStack3)
                self.tempStack3 = ""

            elif self.stack4InputActive:
                self.stack4InputActive = False
                if (self.tempStack4 != ""): config.playerList[3].stackSize = int(self.tempStack4)
                self.tempStack4 = ""

            elif self.stack5InputActive:
                self.stack5InputActive = False
                if (self.tempStack5 != ""): config.playerList[4].stackSize = int(self.tempStack5)
                self.tempStack5 = ""

            elif self.stack6InputActive:
                self.stack6InputActive = False
                if (self.tempStack6 != ""): config.playerList[5].stackSize = int(self.tempStack6)
                self.tempStack6 = ""

            elif self.stack7InputActive:
                self.stack7InputActive = False
                if (self.tempStack7 != ""): config.playerList[6].stackSize = int(self.tempStack7)
                self.tempStack7 = ""
            
            elif self.stack8InputActive:
                self.stack8InputActive = False
                if (self.tempStack8 != ""): config.playerList[7].stackSize = int(self.tempStack8)
                self.tempStack8 = ""

    def stackSizesTimerFired(self,dt):
        pass   
   
    def stackSizesRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Back
        pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("Back", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        screen.blit(backWords, backBox)

        # Table
        pygame.draw.ellipse(screen, (25, 100, 25), self.pokerTable)

        # Pot
        editStack = self.myFont.render("Click to Edit Stack Sizes", True, (0,0,0))
        editBox = editStack.get_rect(center = (self.width//2, self.height//2))
        screen.blit(editStack, editBox)    

        # Players
        player1Stack = self.myFont.render("$"+str(config.playerList[0].stackSize), True, (0,0,0))
        player2Stack = self.myFont.render("$"+str(config.playerList[1].stackSize), True, (0,0,0))
        player3Stack = self.myFont.render("$"+str(config.playerList[2].stackSize), True, (0,0,0))
        player4Stack = self.myFont.render("$"+str(config.playerList[3].stackSize), True, (0,0,0))
        player5Stack = self.myFont.render("$"+str(config.playerList[4].stackSize), True, (0,0,0))
        player6Stack = self.myFont.render("$"+str(config.playerList[5].stackSize), True, (0,0,0))
        player7Stack = self.myFont.render("$"+str(config.playerList[6].stackSize), True, (0,0,0))
        player8Stack = self.myFont.render("$"+str(config.playerList[7].stackSize), True, (0,0,0))

        temp1Stack = self.myFont.render("$"+self.tempStack1, True, (0,0,0))
        temp2Stack = self.myFont.render("$"+self.tempStack2, True, (0,0,0))
        temp3Stack = self.myFont.render("$"+self.tempStack3, True, (0,0,0))
        temp4Stack = self.myFont.render("$"+self.tempStack4, True, (0,0,0))
        temp5Stack = self.myFont.render("$"+self.tempStack5, True, (0,0,0))
        temp6Stack = self.myFont.render("$"+self.tempStack6, True, (0,0,0))
        temp7Stack = self.myFont.render("$"+self.tempStack7, True, (0,0,0))
        temp8Stack = self.myFont.render("$"+self.tempStack8, True, (0,0,0))
        
        stack1Box = player1Stack.get_rect(center = (self.player1Rect.x+self.player1Rect.w//2, self.player1Rect.y+self.player1Rect.h*3//4))
        stack2Box = player2Stack.get_rect(center = (self.player2Rect.x+self.player2Rect.w//2, self.player2Rect.y+self.player2Rect.h*3//4))
        stack3Box = player3Stack.get_rect(center = (self.player3Rect.x+self.player3Rect.w//2, self.player3Rect.y+self.player3Rect.h*3//4))
        stack4Box = player4Stack.get_rect(center = (self.player4Rect.x+self.player4Rect.w//2, self.player4Rect.y+self.player4Rect.h*3//4))
        stack5Box = player5Stack.get_rect(center = (self.player5Rect.x+self.player5Rect.w//2, self.player5Rect.y+self.player5Rect.h*3//4))
        stack6Box = player6Stack.get_rect(center = (self.player6Rect.x+self.player6Rect.w//2, self.player6Rect.y+self.player6Rect.h*3//4))
        stack7Box = player7Stack.get_rect(center = (self.player7Rect.x+self.player7Rect.w//2, self.player7Rect.y+self.player7Rect.h*3//4))
        stack8Box = player8Stack.get_rect(center = (self.player8Rect.x+self.player8Rect.w//2, self.player8Rect.y+self.player8Rect.h*3//4))

        player1Name = self.myFont.render(config.playerList[0].name, True, (0,0,0))
        player2Name = self.myFont.render(config.playerList[1].name, True, (0,0,0))
        player3Name = self.myFont.render(config.playerList[2].name, True, (0,0,0))
        player4Name = self.myFont.render(config.playerList[3].name, True, (0,0,0))
        player5Name = self.myFont.render(config.playerList[4].name, True, (0,0,0))
        player6Name = self.myFont.render(config.playerList[5].name, True, (0,0,0))
        player7Name = self.myFont.render(config.playerList[6].name, True, (0,0,0))
        player8Name = self.myFont.render(config.playerList[7].name, True, (0,0,0))

        player1NameBox = player1Name.get_rect(center = (self.player1Rect.x+self.player1Rect.w//2, self.player1Rect.y+self.player1Rect.h//4))
        player2NameBox = player2Name.get_rect(center = (self.player2Rect.x+self.player2Rect.w//2, self.player2Rect.y+self.player2Rect.h//4))
        player3NameBox = player3Name.get_rect(center = (self.player3Rect.x+self.player3Rect.w//2, self.player3Rect.y+self.player3Rect.h//4))
        player4NameBox = player4Name.get_rect(center = (self.player4Rect.x+self.player4Rect.w//2, self.player4Rect.y+self.player4Rect.h//4))
        player5NameBox = player5Name.get_rect(center = (self.player5Rect.x+self.player5Rect.w//2, self.player5Rect.y+self.player5Rect.h//4))
        player6NameBox = player6Name.get_rect(center = (self.player6Rect.x+self.player6Rect.w//2, self.player6Rect.y+self.player6Rect.h//4))
        player7NameBox = player7Name.get_rect(center = (self.player7Rect.x+self.player7Rect.w//2, self.player7Rect.y+self.player7Rect.h//4))
        player8NameBox = player8Name.get_rect(center = (self.player8Rect.x+self.player8Rect.w//2, self.player8Rect.y+self.player8Rect.h//4))

        if config.playerList[0].isPlaying: 
            color = (75, 75, 75)
            if (self.stack1InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player1Rect.center, self.width//20)
            screen.blit(player1Name, player1NameBox)
            if (self.stack1InputActive):
                screen.blit(temp1Stack, stack1Box)
            else:
                screen.blit(player1Stack, stack1Box)

        if config.playerList[1].isPlaying:
            color = (75, 75, 75)
            if (self.stack2InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player2Rect.center, self.width//20)
            screen.blit(player2Name, player2NameBox)
            if (self.stack2InputActive):
                screen.blit(temp2Stack, stack2Box)
            else:
                screen.blit(player2Stack, stack2Box)

        if config.playerList[2].isPlaying: 
            color = (75, 75, 75)
            if (self.stack3InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player3Rect.center, self.width//20)
            screen.blit(player3Name, player3NameBox)
            if (self.stack3InputActive):
                screen.blit(temp3Stack, stack3Box)
            else:
                screen.blit(player3Stack, stack3Box)
            
        if config.playerList[3].isPlaying: 
            color = (75, 75, 75)
            if (self.stack4InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player4Rect.center, self.width//20)
            screen.blit(player4Name, player4NameBox)
            if (self.stack4InputActive):
                screen.blit(temp4Stack, stack4Box)
            else:
                screen.blit(player4Stack, stack4Box)
            
        if config.playerList[4].isPlaying: 
            color = (75, 75, 75)
            if (self.stack5InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player5Rect.center, self.width//20)
            screen.blit(player5Name, player5NameBox)
            if (self.stack5InputActive):
                screen.blit(temp5Stack, stack5Box)
            else:
                screen.blit(player5Stack, stack5Box)
            
        if config.playerList[5].isPlaying:
            color = (75, 75, 75)
            if (self.stack6InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player6Rect.center, self.width//20)
            screen.blit(player6Name, player6NameBox)
            if (self.stack6InputActive):
                screen.blit(temp6Stack, stack6Box)
            else:
                screen.blit(player6Stack, stack6Box)
        
        if config.playerList[6].isPlaying:  
            color = (75, 75, 75)
            if (self.stack7InputActive): color = (100, 150, 100)         
            pygame.draw.circle(screen, color, self.player7Rect.center, self.width//20)
            screen.blit(player7Name, player7NameBox)
            if (self.stack7InputActive):
                screen.blit(temp7Stack, stack7Box)
            else:
                screen.blit(player7Stack, stack7Box)
        
        if config.playerList[7].isPlaying:
            color = (75, 75, 75)
            if (self.stack8InputActive): color = (100, 150, 100)
            pygame.draw.circle(screen, color, self.player8Rect.center, self.width//20)
            screen.blit(player8Name, player8NameBox)
            if (self.stack8InputActive):
                screen.blit(temp8Stack, stack8Box)
            else:
                screen.blit(player8Stack, stack8Box)

    # After Play Game is Pressed
    def initializeGame(self):
        config.roundMode = "Preflop"

        flag = False
        # Update Small Blind
        for i in range((config.smallBlind+1)%8, 8):
            if (flag): break         
            if (config.playerList[i].isPlaying):
                config.smallBlind = config.playerList[i].num
                flag = True

        for j in range(0, (config.smallBlind+1)%8):
            if (flag): break
            if (config.playerList[j].isPlaying):
                config.smallBlind = config.playerList[j].num
                flag = True

        # Update Big BLind
        flag2 = False
        for k in range((config.smallBlind+1)%8, 8):
            if (flag2): break         
            if (config.playerList[k].isPlaying):
                config.bigBlind = config.playerList[k].num
                flag2 = True

        for l in range(0, (config.smallBlind+1)%8):
            if (flag2): break
            if (config.playerList[l].isPlaying):
                config.bigBlind = config.playerList[l].num
                flag2 = True
         
        # Initialize Curr Player List (Prelop)
        config.currPlayers = []
        for i in range(config.smallBlind, 8):
            if config.playerList[i].isPlaying:
                config.currPlayers.append(i)
                config.playerList[i].inHand = True
            else:
                config.playerList[i].inHand = False

        for j in range(0, config.smallBlind):
            if config.playerList[j].isPlaying:
                config.currPlayers.append(j)
                config.playerList[j].inHand = True
            else:
                config.playerList[j].inHand = False

        # Update Bet Lists       
        for player in config.playerList:
            player.betList = []

        config.playerList[config.currPlayers[0]].betList.append(config.BBVal//2) # SB
        config.playerList[config.currPlayers[0]].stackSize -= config.BBVal//2

        config.playerList[config.currPlayers[1]].betList.append(config.BBVal) # BB
        config.playerList[config.currPlayers[1]].stackSize -= config.BBVal

        config.potSize = (config.BBVal + config.BBVal//2)
        config.maxBet = config.BBVal

        # Adjust for UTG
        tmpList = config.currPlayers[2:]+config.currPlayers[:2]  
        config.currPlayers = tmpList

        config.endPlayer = config.currPlayers[0]

        # Rotate Servo
        self.rotateServo()

    def endRound(self):
        # Reset Bet Lists and Update Player Order
        config.currPlayers = []
        
        for i in range(config.smallBlind, 8):
            config.playerList[i].betList = []
            if config.playerList[i].isPlaying and config.playerList[i].inHand:
                config.currPlayers.append(i)

        for j in range(0, config.smallBlind):
            config.playerList[j].betList = []
            if config.playerList[j].isPlaying and config.playerList[j].inHand:
                config.currPlayers.append(j)

        config.endPlayer = config.currPlayers[0]
        config.maxBet = 0

        # Update Round
        if (config.roundMode == "Preflop"):
            config.roundMode = "Flop"

        elif (config.roundMode == "Flop"):
            config.roundMode = "Turn"

        elif (config.roundMode == "Turn"):
            config.roundMode = "River"

        else: 
            config.winState = True

    def updateBetList(self, currP, bet):
        config.playerList[currP].betList.append(bet)

        # First Bet
        if len(config.playerList[currP].betList) == 1:
            config.potSize += bet
            config.playerList[currP].stackSize -= bet

        # Already Made a Bet
        else:
            diff = bet - config.playerList[currP].betList[-2]
            config.potSize += diff 
            config.playerList[currP].stackSize -= diff

    def rotateServo(self): 
        num = config.currPlayers[0]
        degrees = config.playerList[num].degrees
        print(degrees)
        '''string = str(degrees)
        string_encode = string.encode()
        self.ser.write(string_encode)'''

        '''
        elif ord(pygame.key.name(code)) == 115:
            CompVision.get_stack_value(self.cvdat, debug=True)'''




    



