# Dealer UI
import sys
import pygame
import random
import math
import os
sys.path.insert(1, './GST')
import config
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
        self.myFont = pygame.font.SysFont("Impact", self.width//20)
        folder = os.path.dirname(os.path.realpath(__file__))

        # Servo
        self.ser = serial.Serial('/dev/ttyACM0',9600)

        # Config Screen 
        self.startButton = pygame.Rect(self.width//2-self.width//5, self.height//2-self.width//5, self.width//5, self.width//5)
        self.addDelButton = pygame.Rect(self.width//2, self.height//2-self.width//5, self.width//5, self.width//5)
        self.chipColorButton = pygame.Rect(self.width//2-self.width//5, self.height//2, self.width//5, self.width//5)
        self.stackSizeButton = pygame.Rect(self.width//2, self.height//2, self.width//5, self.width//5)

        # Back Button 
        self.backRect = pygame.Rect(self.width//20, self.height//20, self.width//15, self.width//15)

        # Chip Values
        self.whiteChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "whitechip.jpg")),(self.width//10, self.width//10))
        self.redChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "redchip.jpg")),(self.width//10, self.width//10))
        self.greenChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "greenchip.jpg")),(self.width//10, self.width//10))
        self.blueChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "bluechip.jpg")),(self.width//10, self.width//10))
        self.blackChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "blackchip.jpg")),(self.width//10, self.width//10))

        # Play Game
        self.dealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//10, self.width//10))
        self.pokerTable = pygame.Rect(self.width//10, self.height//10, self.width-self.width//5, self.height-self.height//5) 
        self.rotateButton = pygame.Rect(self.width-self.width//10, self.height//20, self.width//15, self.width//15)

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
        self.blueRect = self.blueChip.get_rect(center=(self.width//3,self.height*2//3))
        self.blackRect = self.blackChip.get_rect(center=(self.width*2//3,self.height*2//3))

        self.whiteInputActive = False
        self.redInputActive = False
        self.greenInputActive = False
        self.blueInputActive = False
        self.blackInputActive = False

        self.tempWhiteNum = ""
        self.tempRedNum = ""
        self.tempGreenNum = ""
        self.tempBlueNum = ""
        self.tempBlackNum = ""

        # Stack Sizes

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
            config.gameMode = "playGame"
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
                config.playerList[0].stackSize = 0
            else:
                self.player1InputActive = True
        
        elif self.player2Rect.collidepoint(x, y):
            config.playerList[1].name = ""
            if config.playerList[1].isPlaying:
                config.playerList[1].isPlaying = False
                config.playerList[1].stackSize = 0
            else:
                self.player2InputActive = True
        
        elif self.player3Rect.collidepoint(x, y):
            config.playerList[2].name = ""
            if config.playerList[2].isPlaying:
                config.playerList[2].isPlaying = False
                config.playerList[2].stackSize = 0
            else:
                self.player3InputActive = True
        
        elif self.player4Rect.collidepoint(x, y):
            config.playerList[3].name = ""
            if config.playerList[3].isPlaying:
                config.playerList[3].isPlaying = False
                config.playerList[3].stackSize = 0
            else:
                self.player4InputActive = True
        
        elif self.player5Rect.collidepoint(x, y):
            config.playerList[4].name = ""
            if config.playerList[4].isPlaying:
                config.playerList[4].isPlaying = False
                config.playerList[4].stackSize = 0
            else:
                self.player5InputActive = True

        elif self.player6Rect.collidepoint(x, y):
            config.playerList[5].name = ""
            if config.playerList[5].isPlaying:
                config.playerList[5].isPlaying = False
                config.playerList[5].stackSize = 0
            else:
                self.player6InputActive = True

        elif self.player7Rect.collidepoint(x, y):
            config.playerList[6].name = ""
            if config.playerList[6].isPlaying:
                config.playerList[6].isPlaying = False
                config.playerList[6].stackSize = 0
            else:
                self.player7InputActive = True

        elif self.player8Rect.collidepoint(x, y):
            config.playerList[7].name = ""
            if config.playerList[7].isPlaying:
                config.playerList[7].isPlaying = False
                config.playerList[7].stackSize = 0
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
        dealerRect = self.dealerChip.get_rect(center=(self.width//2,self.height//10))
        screen.blit(self.dealerChip, dealerRect)

        # Players 
        if self.player1InputActive: 
            pygame.draw.circle(screen, (100, 150, 100), self.player1Rect.center,self.width//20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width//20)

        if self.player2InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player2Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width//20)

        if self.player3InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player3Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width//20)

        if self.player4InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player4Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width//20)
        
        if self.player5InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player5Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width//20)
        
        if self.player6InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player6Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width//20)
        
        if self.player7InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player7Rect.center, self.width//20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width//20)

        if self.player8InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player8Rect.center, self.width//20) 
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
        if self.backRect.collidepoint(x, y):
            config.gameMode = "config"
        
        if self.rotateButton.collidepoint(x,y):
            config.currAction = "rotate"
            string = "rotate\n"
            string_encode = string.encode()
            self.ser.write(string_encode)

    def playGameKeyPressed(self, code, mod):
        pass
   
    def playGameTimerFired(self, dt):
        while config.currAction == "rotate":
            config.rotateTime += dt
            if config.rotateTime >= 20000: # 20 seconds
                config.currAction = ""
                config.rotateTime = 0
  
    def playGameRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Back
        pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("Back", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        screen.blit(backWords, backBox)

        # Rotate Button
        pygame.draw.rect(screen, (75, 50, 150), self.rotateButton)
        rotateWords = self.myFont.render("Rotate", True, (0,0,0))
        rotateBox = rotateWords.get_rect(center = self.rotateButton.center)
        screen.blit(rotateWords, rotateBox)
        
        # Table
        pygame.draw.ellipse(screen, (25, 100, 25), self.pokerTable)

        # Pot
        thePot = self.myFont.render("The Pot", True, (0,0,0))
        thePotBox = thePot.get_rect(center = (self.width//2, self.height//2-self.height//25))
        screen.blit(thePot, thePotBox)
        potSizeString = "$%d" % config.potSize
        potSize = self.myFont.render(potSizeString, True, (0,0,0))
        potSizeBox = potSize.get_rect(center = (self.width//2, self.height//2+self.height//25))
        screen.blit(potSize, potSizeBox)
        
        # Dealer 
        dealerRect = self.dealerChip.get_rect(center=(self.width//2,self.height//10))
        screen.blit(self.dealerChip, dealerRect)

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
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width//20)
            screen.blit(player1Name, player1NameBox)
            screen.blit(player1Stack, stack1Box)

        if config.playerList[1].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width//20)
            screen.blit(player2Name, player2NameBox)
            screen.blit(player2Stack, stack2Box)

        if config.playerList[2].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width//20)
            screen.blit(player3Name, player3NameBox)
            screen.blit(player3Stack, stack3Box)
            
        if config.playerList[3].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width//20)
            screen.blit(player4Name, player4NameBox)
            screen.blit(player4Stack, stack4Box)
            
        if config.playerList[4].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width//20)
            screen.blit(player5Name, player5NameBox)
            screen.blit(player5Stack, stack5Box)
            
        if config.playerList[5].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width//20)
            screen.blit(player6Name, player6NameBox)
            screen.blit(player6Stack, stack6Box)
        
        if config.playerList[6].isPlaying:           
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width//20)
            screen.blit(player7Name, player7NameBox)
            screen.blit(player7Stack, stack7Box)
        
        if config.playerList[7].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width//20)
            screen.blit(player8Name, player8NameBox)
            screen.blit(player8Stack, stack8Box)

    # Chip Colors Config
    def chipConfigMousePressed(self, x, y):
        self.whiteInputActive = False
        self.redInputActive = False
        self.greenInputActive = False
        self.blueInputActive = False
        self.blackInputActive = False

        if self.backRect.collidepoint(x, y):
            config.gameMode = "config"

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

           
    def chipConfigTimerFired(self,dt):
        pass   
   
    def chipConfigRedrawAll(self, screen):
        screen.fill((56,79,70))

        clickWords = self.myFont.render("Click to Edit Chip Values", True, (0,0,0))
        clickBox = clickWords.get_rect(center = (self.width//2, self.height//8))
        screen.blit(clickWords, clickBox)

        whiteNum = self.myFont.render(str(config.chipValues[0]), True, (0,0,0))
        redNum = self.myFont.render(str(config.chipValues[1]), True, (0,0,0))
        greenNum = self.myFont.render(str(config.chipValues[2]), True, (0,0,0))
        blueNum = self.myFont.render(str(config.chipValues[3]), True, (0,0,0))
        blackNum = self.myFont.render(str(config.chipValues[4]), True, (0,0,0))

        tempWhite = self.myFont.render(self.tempWhiteNum, True, (0,0,0))
        tempRed = self.myFont.render(self.tempRedNum, True, (0,0,0))
        tempGreen = self.myFont.render(self.tempGreenNum, True, (0,0,0))
        tempBlue = self.myFont.render(self.tempBlueNum, True, (0,0,0))
        tempBlack = self.myFont.render(self.tempBlackNum, True, (0,0,0))

        whiteBox = whiteNum.get_rect(center = self.whiteRect.center)
        redBox = redNum.get_rect(center = self.redRect.center)
        greenBox = greenNum.get_rect(center = self.greenRect.center)
        blueBox = blueNum.get_rect(center = self.blueRect.center)
        blackBox = blackNum.get_rect(center = self.blackRect.center)

        screen.blit(self.whiteChip, self.whiteRect)
        screen.blit(self.redChip, self.redRect)
        screen.blit(self.greenChip, self.greenRect)
        screen.blit(self.blueChip, self.blueRect)
        screen.blit(self.blackChip, self.blackRect)

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
                config.playerList[0].stackSize = int(self.tempStack1)
                self.tempStack1 = ""

            elif self.stack2InputActive:
                self.stack2InputActive = False
                config.playerList[1].stackSize = int(self.tempStack2)
                self.tempStack2 = ""

            elif self.stack3InputActive:
                self.stack3InputActive = False
                config.playerList[2].stackSize = int(self.tempStack3)
                self.tempStack3 = ""

            elif self.stack4InputActive:
                self.stack4InputActive = False
                config.playerList[3].stackSize = int(self.tempStack4)
                self.tempStack4 = ""

            elif self.stack5InputActive:
                self.stack5InputActive = False
                config.playerList[4].stackSize = int(self.tempStack5)
                self.tempStack5 = ""

            elif self.stack6InputActive:
                self.stack6InputActive = False
                config.playerList[5].stackSize = int(self.tempStack6)
                self.tempStack6 = ""

            elif self.stack7InputActive:
                self.stack7InputActive = False
                config.playerList[6].stackSize = int(self.tempStack7)
                self.tempStack7 = ""
            
            elif self.stack8InputActive:
                self.stack8InputActive = False
                config.playerList[7].stackSize = int(self.tempStack8)
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
        player1Name = self.myFont.render(config.playerList[0].name, True, (0,0,0))
        player2Name = self.myFont.render(config.playerList[1].name, True, (0,0,0))
        player3Name = self.myFont.render(config.playerList[2].name, True, (0,0,0))
        player4Name = self.myFont.render(config.playerList[3].name, True, (0,0,0))
        player5Name = self.myFont.render(config.playerList[4].name, True, (0,0,0))
        player6Name = self.myFont.render(config.playerList[5].name, True, (0,0,0))
        player7Name = self.myFont.render(config.playerList[6].name, True, (0,0,0))
        player8Name = self.myFont.render(config.playerList[7].name, True, (0,0,0))

        player1NameBox = player1Name.get_rect(center = self.player1Rect.center)
        player2NameBox = player2Name.get_rect(center = self.player2Rect.center)
        player3NameBox = player3Name.get_rect(center = self.player3Rect.center)
        player4NameBox = player4Name.get_rect(center = self.player4Rect.center)
        player5NameBox = player5Name.get_rect(center = self.player5Rect.center)
        player6NameBox = player6Name.get_rect(center = self.player6Rect.center)
        player7NameBox = player7Name.get_rect(center = self.player7Rect.center)
        player8NameBox = player8Name.get_rect(center = self.player8Rect.center)

        if config.playerList[0].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width//20)
            screen.blit(player1Name, player1NameBox)

        if config.playerList[1].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width//20)
            screen.blit(player2Name, player2NameBox)

        if config.playerList[2].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width//20)
            screen.blit(player3Name, player3NameBox)
            
        if config.playerList[3].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width//20)
            screen.blit(player4Name, player4NameBox)
            
        if config.playerList[4].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width//20)
            screen.blit(player5Name, player5NameBox)
            
        if config.playerList[5].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width//20)
            screen.blit(player6Name, player6NameBox)
        
        if config.playerList[6].isPlaying:           
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width//20)
            screen.blit(player7Name, player7NameBox)
        
        if config.playerList[7].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width//20)
            screen.blit(player8Name, player8NameBox)

