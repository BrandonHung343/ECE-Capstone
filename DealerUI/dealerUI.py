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

    def run(self, playerList, potSize, gameMode):
        # General Intialization
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.title)

        self._keys = dict()

        # Poker Game Intialization
        self.init(playerList, potSize, gameMode)
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
    def init(self, playerList, potSize, gameMode):
        # General
        self.gameMode = gameMode
        self.myFont = pygame.font.SysFont("Impact", 35)
        folder = os.path.dirname(os.path.realpath(__file__))

        # Config Screen 
        self.startButton = pygame.Rect(self.width/2-self.width/5, self.height/2-self.width/5, self.width/5, self.width/5)
        self.addDelButton = pygame.Rect(self.width/2, self.height/2-self.width/5, self.width/5, self.width/5)
        self.chipColorButton = pygame.Rect(self.width/2-self.width/5, self.height/2, self.width/5, self.width/5)
        self.stackSizeButton = pygame.Rect(self.width/2, self.height/2, self.width/5, self.width/5)

        # Back Button 
        self.backRect = pygame.Rect(self.width/20, self.height/20, self.width/15, self.width/15)

        # Chip Values
        self.whiteValue = 1
        self.redValue = 2
        self.greenValue = 5
        self.blueValue = 10
        self.blackValue = 20

        self.whiteChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "whitechip.jpg")),(self.width//10, self.width//10))
        self.redChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "redchip.jpg")),(self.width//10, self.width//10))
        self.greenChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "greenchip.jpg")),(self.width//10, self.width//10))
        self.blueChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "bluechip.jpg")),(self.width//10, self.width//10))
        self.blackChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "blackchip.jpg")),(self.width//10, self.width//10))

        # Play Game
        self.potSize = potSize
        self.dealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//10, self.width//10))
        self.pokerTable = pygame.Rect(self.width/10, self.height/10, self.width-self.width/5, self.height-self.height/5) 

        # Players 
        self.playerList = playerList

        self.player8Rect = pygame.Rect(self.width/3-self.width/20, self.height/6-self.width/20, self.width/10, self.width/10)
        self.player7Rect = pygame.Rect(self.width/6-self.width/20, self.height/3-self.width/20, self.width/10, self.width/10)
        self.player6Rect = pygame.Rect(self.width/6-self.width/20, self.height*2/3-self.width/20, self.width/10, self.width/10)
        self.player5Rect = pygame.Rect(self.width/3-self.width/20, self.height*5/6-self.width/20, self.width/10, self.width/10)
        self.player4Rect = pygame.Rect(self.width*2/3-self.width/20, self.height*5/6-self.width/20, self.width/10, self.width/10)
        self.player3Rect = pygame.Rect(self.width*5/6-self.width/20, self.height*2/3-self.width/20, self.width/10, self.width/10)
        self.player2Rect = pygame.Rect(self.width*5/6-self.width/20, self.height/3-self.width/20, self.width/10, self.width/10)
        self.player1Rect = pygame.Rect(self.width*2/3-self.width/20, self.height/6-self.width/20, self.width/10, self.width/10)

        # Add/Del Screen
        self.player1InputActive = False
        self.player2InputActive = False
        self.player3InputActive = False
        self.player4InputActive = False
        self.player5InputActive = False
        self.player6InputActive = False
        self.player7InputActive = False
        self.player8InputActive = False

    # Choose which Screen 
    def mousePressed(self, x, y):
        
        if (self.gameMode == "config"): 
            PokerGame.configScreenMousePressed(self, x, y)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameMousePressed(self, x, y)
        elif (self.gameMode == "addDel"):
            PokerGame.addDelMousePressed(self, x, y)
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigMousePressed(self, x, y)
    
    def keyPressed(self, code, mod):
        if (self.gameMode == "config"): 
            PokerGame.configScreenKeyPressed(self, code, mod)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameKeyPressed(self, code, mod)
        elif (self.gameMode == "addDel"):
            PokerGame.addDelKeyPressed(self, code, mod)
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigKeyPressed(self, code, mod)
    
    def timerFired(self, dt):
        if (self.gameMode == "config"): 
            PokerGame.configScreenTimerFired(self, dt)
        elif (self.gameMode == "playGame"):
            PokerGame.playGameTimerFired(self, dt)   
        elif (self.gameMode == "addDel"):
            PokerGame.addDelTimerFired(self, dt) 
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigTimerFired(self, dt)
    
    def redrawAll(self, screen):
        if (self.gameMode == "config"):
            PokerGame.configScreenRedrawAll(self, screen)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameRedrawAll(self, screen)
        elif (self.gameMode == "addDel"):
            PokerGame.addDelRedrawAll(self, screen)
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigRedrawAll(self, screen)
    
    # Configuartion Screen Functions
    def configScreenMousePressed(self, x, y):
        if self.startButton.collidepoint(x, y):
            self.gameMode = "playGame"
        elif self.addDelButton.collidepoint(x, y):
            self.gameMode = "addDel"
        elif self.chipColorButton.collidepoint(x, y):
            self.gameMode = "chipConfig"
    
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
            self.gameMode = "config"

        elif self.player1Rect.collidepoint(x, y):
            self.playerList[0].name = ""
            if self.playerList[0].isPlaying:
                self.playerList[0].isPlaying = False
                self.playerList[0].stackSize = 0
            else:
                self.player1InputActive = True
        
        elif self.player2Rect.collidepoint(x, y):
            self.playerList[1].name = ""
            if self.playerList[1].isPlaying:
                self.playerList[1].isPlaying = False
                self.playerList[1].stackSize = 0
            else:
                self.player2InputActive = True
        
        elif self.player3Rect.collidepoint(x, y):
            self.playerList[2].name = ""
            if self.playerList[2].isPlaying:
                self.playerList[2].isPlaying = False
                self.playerList[2].stackSize = 0
            else:
                self.player3InputActive = True
        
        elif self.player4Rect.collidepoint(x, y):
            self.playerList[3].name = ""
            if self.playerList[3].isPlaying:
                self.playerList[3].isPlaying = False
                self.playerList[3].stackSize = 0
            else:
                self.player4InputActive = True
        
        elif self.player5Rect.collidepoint(x, y):
            self.playerList[4].name = ""
            if self.playerList[4].isPlaying:
                self.playerList[4].isPlaying = False
                self.playerList[4].stackSize = 0
            else:
                self.player5InputActive = True

        elif self.player6Rect.collidepoint(x, y):
            self.playerList[5].name = ""
            if self.playerList[5].isPlaying:
                self.playerList[5].isPlaying = False
                self.playerList[5].stackSize = 0
            else:
                self.player6InputActive = True

        elif self.player7Rect.collidepoint(x, y):
            self.playerList[6].name = ""
            if self.playerList[6].isPlaying:
                self.playerList[6].isPlaying = False
                self.playerList[6].stackSize = 0
            else:
                self.player7InputActive = True

        elif self.player8Rect.collidepoint(x, y):
            self.playerList[7].name = ""
            if self.playerList[7].isPlaying:
                self.playerList[7].isPlaying = False
                self.playerList[7].stackSize = 0
            else:
                self.player8InputActive = True

    def addDelKeyPressed(self, code, mod):
        # Lower Case Letter
        if  len(pygame.key.name(code)) == 1: 
            if ord(pygame.key.name(code)) >= 97 and ord(pygame.key.name(code)) <= 122:
                letter = pygame.key.name(code)
                if self.player1InputActive:
                    self.playerList[0].name += letter
                if self.player2InputActive:
                    self.playerList[1].name += letter
                if self.player3InputActive:
                    self.playerList[2].name += letter
                if self.player4InputActive:
                    self.playerList[3].name += letter
                if self.player5InputActive:
                    self.playerList[4].name += letter
                if self.player6InputActive:
                    self.playerList[5].name += letter
                if self.player7InputActive:
                    self.playerList[6].name += letter
                if self.player8InputActive:
                    self.playerList[7].name += letter

        # Enter/Return
        elif code == pygame.K_RETURN:
            if self.player1InputActive:
                self.playerList[0].isPlaying = True
                self.player1InputActive = False

            elif self.player2InputActive:
                self.playerList[1].isPlaying = True
                self.player2InputActive = False

            elif self.player3InputActive:
                self.playerList[2].isPlaying = True
                self.player3InputActive = False

            elif self.player4InputActive:
                self.playerList[3].isPlaying = True
                self.player4InputActive = False

            elif self.player5InputActive:
                self.playerList[4].isPlaying = True
                self.player5InputActive = False

            elif self.player6InputActive:
                self.playerList[5].isPlaying = True
                self.player6InputActive = False

            elif self.player7InputActive:
                self.playerList[6].isPlaying = True
                self.player7InputActive = False

            elif self.player8InputActive:
                self.playerList[7].isPlaying = True
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
        dealerRect = self.dealerChip.get_rect(center=(self.width/2,self.height/10))
        screen.blit(self.dealerChip, dealerRect)

        # Players 
        if self.player1InputActive: 
            pygame.draw.circle(screen, (100, 150, 100), self.player1Rect.center,self.width/20)
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width/20)

        if self.player2InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player2Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width/20)

        if self.player3InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player3Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width/20)

        if self.player4InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player4Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width/20)
        
        if self.player5InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player5Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width/20)
        
        if self.player6InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player6Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width/20)
        
        if self.player7InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player7Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width/20)

        if self.player8InputActive:
            pygame.draw.circle(screen, (100, 150, 100), self.player8Rect.center, self.width/20) 
        else:
            pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width/20)
        

        removePlayer1 = self.myFont.render("Remove "+self.playerList[0].name, True, (0,0,0))
        removePlayer2 = self.myFont.render("Remove "+self.playerList[1].name, True, (0,0,0))
        removePlayer3 = self.myFont.render("Remove "+self.playerList[2].name, True, (0,0,0))
        removePlayer4 = self.myFont.render("Remove "+self.playerList[3].name, True, (0,0,0))
        removePlayer5 = self.myFont.render("Remove "+self.playerList[4].name, True, (0,0,0))
        removePlayer6 = self.myFont.render("Remove "+self.playerList[5].name, True, (0,0,0))
        removePlayer7 = self.myFont.render("Remove "+self.playerList[6].name, True, (0,0,0))
        removePlayer8 = self.myFont.render("Remove "+self.playerList[7].name, True, (0,0,0))

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

        inputText1 = self.myFont.render("Input Name : "+self.playerList[0].name, True, (0,0,0))
        inputText2 = self.myFont.render("Input Name : "+self.playerList[1].name, True, (0,0,0))
        inputText3 = self.myFont.render("Input Name : "+self.playerList[2].name, True, (0,0,0))
        inputText4 = self.myFont.render("Input Name : "+self.playerList[3].name, True, (0,0,0))
        inputText5 = self.myFont.render("Input Name : "+self.playerList[4].name, True, (0,0,0))
        inputText6 = self.myFont.render("Input Name : "+self.playerList[5].name, True, (0,0,0))
        inputText7 = self.myFont.render("Input Name : "+self.playerList[6].name, True, (0,0,0))
        inputText8 = self.myFont.render("Input Name : "+self.playerList[7].name, True, (0,0,0))

        inputBox1 = inputText1.get_rect(center = self.player1Rect.center)
        inputBox2 = inputText2.get_rect(center = self.player2Rect.center)
        inputBox3 = inputText3.get_rect(center = self.player3Rect.center)
        inputBox4 = inputText4.get_rect(center = self.player4Rect.center)
        inputBox5 = inputText5.get_rect(center = self.player5Rect.center)
        inputBox6 = inputText6.get_rect(center = self.player6Rect.center)
        inputBox7 = inputText7.get_rect(center = self.player7Rect.center)
        inputBox8 = inputText8.get_rect(center = self.player8Rect.center)

        if self.playerList[0].isPlaying: 
            screen.blit(removePlayer1, removePlayer1Box)
        elif self.player1InputActive:
            screen.blit(inputText1, inputBox1)
        else: 
            screen.blit(addText, player1AddBox)

        if self.playerList[1].isPlaying: 
            screen.blit(removePlayer2, removePlayer2Box)
        elif self.player2InputActive:
            screen.blit(inputText2, inputBox2)
        else: 
            screen.blit(addText, player2AddBox)

        if self.playerList[2].isPlaying: 
            screen.blit(removePlayer3, removePlayer3Box)
        elif self.player3InputActive:
            screen.blit(inputText3, inputBox3)
        else: 
            screen.blit(addText, player3AddBox)
            
        if self.playerList[3].isPlaying: 
            screen.blit(removePlayer4, removePlayer4Box)
        elif self.player4InputActive:
            screen.blit(inputText4, inputBox4)
        else: 
            screen.blit(addText, player4AddBox)
            
        if self.playerList[4].isPlaying: 
            screen.blit(removePlayer5, removePlayer5Box)
        elif self.player5InputActive:
            screen.blit(inputText5, inputBox5)
        else: 
            screen.blit(addText, player5AddBox)
            
        if self.playerList[5].isPlaying: 
            screen.blit(removePlayer6, removePlayer6Box)
        elif self.player6InputActive:
            screen.blit(inputText6, inputBox6)
        else: 
            screen.blit(addText, player6AddBox)
        
        if self.playerList[6].isPlaying: 
            screen.blit(removePlayer7, removePlayer7Box)
        elif self.player7InputActive:
            screen.blit(inputText7, inputBox7)
        else: 
            screen.blit(addText, player7AddBox)
        
        if self.playerList[7].isPlaying: 
            screen.blit(removePlayer8, removePlayer8Box)
        elif self.player8InputActive:
            screen.blit(inputText8, inputBox8)
        else: 
            screen.blit(addText, player8AddBox)

    # Play Game Screen Functions
    def playGameMousePressed(self, x ,y):
        if self.backRect.collidepoint(x, y):
            self.gameMode = "config"

    def playGameKeyPressed(self, code, mod):
        pass
   
    def playGameTimerFired(self, dt):
        pass
  
    def playGameRedrawAll(self, screen):
        screen.fill((120, 120, 120))

        # Back
        pygame.draw.rect(screen, (255, 0, 0), self.backRect)
        backWords = self.myFont.render("Back", True, (0,0,0))
        backBox = backWords.get_rect(center = self.backRect.center)
        screen.blit(backWords, backBox)

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
        player1Name = self.myFont.render(self.playerList[0].name, True, (0,0,0))
        player2Name = self.myFont.render(self.playerList[1].name, True, (0,0,0))
        player3Name = self.myFont.render(self.playerList[2].name, True, (0,0,0))
        player4Name = self.myFont.render(self.playerList[3].name, True, (0,0,0))
        player5Name = self.myFont.render(self.playerList[4].name, True, (0,0,0))
        player6Name = self.myFont.render(self.playerList[5].name, True, (0,0,0))
        player7Name = self.myFont.render(self.playerList[6].name, True, (0,0,0))
        player8Name = self.myFont.render(self.playerList[7].name, True, (0,0,0))

        player1NameBox = player1Name.get_rect(center = self.player1Rect.center)
        player2NameBox = player2Name.get_rect(center = self.player2Rect.center)
        player3NameBox = player3Name.get_rect(center = self.player3Rect.center)
        player4NameBox = player4Name.get_rect(center = self.player4Rect.center)
        player5NameBox = player5Name.get_rect(center = self.player5Rect.center)
        player6NameBox = player6Name.get_rect(center = self.player6Rect.center)
        player7NameBox = player7Name.get_rect(center = self.player7Rect.center)
        player8NameBox = player8Name.get_rect(center = self.player8Rect.center)

        if self.playerList[0].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width/20)
            screen.blit(player1Name, player1NameBox)

        if self.playerList[1].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width/20)
            screen.blit(player2Name, player2NameBox)

        if self.playerList[2].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width/20)
            screen.blit(player3Name, player3NameBox)
            
        if self.playerList[3].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width/20)
            screen.blit(player4Name, player4NameBox)
            
        if self.playerList[4].isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width/20)
            screen.blit(player5Name, player5NameBox)
            
        if self.playerList[5].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width/20)
            screen.blit(player6Name, player6NameBox)
        
        if self.playerList[6].isPlaying:           
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width/20)
            screen.blit(player7Name, player7NameBox)
        
        if self.playerList[7].isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player8Rect.center, self.width/20)
            screen.blit(player8Name, player8NameBox)

    # Chip Colors Config
    def chipConfigMousePressed(self, x, y):
        pass
    
    def chipConfigKeyPressed(self, code, mod):
        pass
  
    def chipConfigTimerFired(self,dt):
        pass   
   
    def chipConfigRedrawAll(self, screen):
        screen.fill((56,79,70))

        whiteRect = self.whiteChip.get_rect(center=(self.width/4,self.height/3))
        redRect = self.redChip.get_rect(center=(self.width/2,self.height/3))
        greenRect = self.greenChip.get_rect(center=(self.width*3/4,self.height/3))
        blueRect = self.blueChip.get_rect(center=(self.width/3,self.height*2/3))
        blackRect = self.blackChip.get_rect(center=(self.width*2/3,self.height*2/3))

        screen.blit(self.whiteChip, whiteRect)
        screen.blit(self.redChip, redRect)
        screen.blit(self.greenChip, greenRect)
        screen.blit(self.blueChip, blueRect)
        screen.blit(self.blackChip, blackRect)

# PokerGame().run()

