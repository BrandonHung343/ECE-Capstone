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
        self.potSize = 0
        self.dealerChip = pygame.transform.scale(pygame.image.load(os.path.join(folder, "dealer_chip.jpg")),(self.width//10, self.width//10))
        self.pokerTable = pygame.Rect(self.width/10, self.height/10, self.width-self.width/5, self.height-self.height/5) 

        # Players 
        self.player1Rect = pygame.Rect(self.width/3-self.width/20, self.height/6-self.width/20, self.width/10, self.width/10)
        self.player2Rect = pygame.Rect(self.width/6-self.width/20, self.height/3-self.width/20, self.width/10, self.width/10)
        self.player3Rect = pygame.Rect(self.width/6-self.width/20, self.height*2/3-self.width/20, self.width/10, self.width/10)
        self.player4Rect = pygame.Rect(self.width/3-self.width/20, self.height*5/6-self.width/20, self.width/10, self.width/10)
        self.player5Rect = pygame.Rect(self.width*2/3-self.width/20, self.height*5/6-self.width/20, self.width/10, self.width/10)
        self.player6Rect = pygame.Rect(self.width*5/6-self.width/20, self.height*2/3-self.width/20, self.width/10, self.width/10)
        self.player7Rect = pygame.Rect(self.width*5/6-self.width/20, self.height/3-self.width/20, self.width/10, self.width/10)
        self.player8Rect = pygame.Rect(self.width*2/3-self.width/20, self.height/6-self.width/20, self.width/10, self.width/10)

        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.player3 = Player("Player 3")
        self.player4 = Player("Player 4")
        self.player5 = Player("Player 5")
        self.player6 = Player("Player 6")
        self.player7 = Player("Player 7")
        self.player8 = Player("Player 8")
        self.temp1Name = ""
        self.temp2Name = ""
        self.temp3Name = ""
        self.temp4Name = ""
        self.temp5Name = ""
        self.temp6Name = ""
        self.temp7Name = ""
        self.temp8Name = ""

        self.player1InputActive = False
        self.player2InputActive = False
        self.player3InputActive = False
        self.player4InputActive = False
        self.player5InputActive = False
        self.player6InputActive = False
        self.player7InputActive = False
        self.player8InputActive = False

        self.numPlayers = sum([self.player1.isPlaying,self.player2.isPlaying,self.player3.isPlaying,self.player4.isPlaying,
            self.player5.isPlaying,self.player6.isPlaying,self.player7.isPlaying,self.player8.isPlaying])

        '''
        pygame.draw.circle(screen, (75, 75, 75), (self.width/3, self.height/6), self.width/20) # Player 1
        pygame.draw.circle(screen, (75, 75, 75), (self.width/6, self.height/3), self.width/20) # Player 2
        pygame.draw.circle(screen, (75, 75, 75), (self.width/6, self.height*2/3), self.width/20) # Player 3
        pygame.draw.circle(screen, (75, 75, 75), (self.width/3, self.height*5/6), self.width/20) # Player 4
        pygame.draw.circle(screen, (75, 75, 75), (self.width*2/3, self.height*5/6), self.width/20) # Player 5
        pygame.draw.circle(screen, (75, 75, 75), (self.width*5/6, self.height*2/3), self.width/20) # Player 6
        pygame.draw.circle(screen, (75, 75, 75), (self.width*5/6, self.height/3), self.width/20) # Player 7
        pygame.draw.circle(screen, (75, 75, 75), (self.width*2/3, self.height/6), self.width/20) # Player 8'''

    # Choose which Screen 
    def mousePressed(self, x, y):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenMousePressed(self, x, y)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameMousePressed(self, x, y)
        elif (self.gameMode == "addDel"):
            PokerGame.addDelMousePressed(self, x, y)
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigMousePressed(self, x, y)
    
    def keyPressed(self, code, mod):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenKeyPressed(self, code, mod)
        elif (self.gameMode == "playGame"):       
            PokerGame.playGameKeyPressed(self, code, mod)
        elif (self.gameMode == "addDel"):
            PokerGame.addDelKeyPressed(self, code, mod)
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigKeyPressed(self, code, mod)
    
    def timerFired(self, dt):
        if (self.gameMode == "configScreen"): 
            PokerGame.configScreenTimerFired(self, dt)
        elif (self.gameMode == "playGame"):
            PokerGame.playGameTimerFired(self, dt)   
        elif (self.gameMode == "addDel"):
            PokerGame.addDelTimerFired(self, dt) 
        elif (self.gameMode == "chipConfig"):
            PokerGame.chipConfigTimerFired(self, dt)
    
    def redrawAll(self, screen):
        if (self.gameMode == "configScreen"):
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
            self.gameMode = "configScreen"

        elif self.player1Rect.collidepoint(x, y):
            if self.player1.isPlaying:
                self.player1.isPlaying = False
                self.player1.name = "Player 1"
                self.player1.stackSize = 0
            else:
                self.player1InputActive = True
                self.player1.name = ""
        
        elif self.player2Rect.collidepoint(x, y):
            if self.player2.isPlaying:
                self.player2.isPlaying = False
                self.player2.name = "Player 2"
                self.player2.stackSize = 0
            else:
                self.player2InputActive = True
                self.player2.name = ""
        
        elif self.player3Rect.collidepoint(x, y):
            if self.player3.isPlaying:
                self.player3.isPlaying = False
                self.player3.name = "Player 3"
                self.player3.stackSize = 0
            else:
                self.player3InputActive = True
                self.player3.name = ""
        
        elif self.player4Rect.collidepoint(x, y):
            if self.player4.isPlaying:
                self.player4.isPlaying = False
                self.player4.name = "Player 4"
                self.player4.stackSize = 0
            else:
                self.player4InputActive = True
                self.player4.name = ""
        
        elif self.player5Rect.collidepoint(x, y):
            if self.player5.isPlaying:
                self.player5.isPlaying = False
                self.player5.name = "Player 5"
                self.player5.stackSize = 0
            else:
                self.player5InputActive = True
                self.player5.name = ""

        elif self.player6Rect.collidepoint(x, y):
            if self.player6.isPlaying:
                self.player6.isPlaying = False
                self.player6.name = "Player 6"
                self.player6.stackSize = 0
            else:
                self.player6InputActive = True
                self.player6.name = ""

        elif self.player7Rect.collidepoint(x, y):
            if self.player7.isPlaying:
                self.player7.isPlaying = False
                self.player7.name = "Player 7"
                self.player7.stackSize = 0
            else:
                self.player7InputActive = True
                self.player7.name = ""

        elif self.player8Rect.collidepoint(x, y):
            if self.player8.isPlaying:
                self.player8.isPlaying = False
                self.player8.name = "Player 8"
                self.player8.stackSize = 0
            else:
                self.player8InputActive = True
                self.player8.name = ""
    
    def addDelKeyPressed(self, code, mod):
        # Lower Case LEtter
        if  len(pygame.key.name(code)) == 1: 
            if ord(pygame.key.name(code)) >= 97 and ord(pygame.key.name(code)) <= 122:
                letter = pygame.key.name(code)
                if self.player1InputActive:
                    self.player1.name += letter
                if self.player2InputActive:
                    self.player2.name += letter
                if self.player3InputActive:
                    self.player3.name += letter
                if self.player4InputActive:
                    self.player4.name += letter
                if self.player5InputActive:
                    self.player5.name += letter
                if self.player6InputActive:
                    self.player6.name += letter
                if self.player7InputActive:
                    self.player7.name += letter
                if self.player8InputActive:
                    self.player8.name += letter

        # Enter/Return
        elif code == pygame.K_RETURN:
            if self.player1InputActive:
                self.player1.isPlaying = True
                self.player1InputActive = False

            elif self.player2InputActive:
                self.player2.isPlaying = True
                self.player2InputActive = False

            elif self.player3InputActive:
                self.player3.isPlaying = True
                self.player3InputActive = False

            elif self.player4InputActive:
                self.player4.isPlaying = True
                self.player4InputActive = False

            elif self.player5InputActive:
                self.player5.isPlaying = True
                self.player5InputActive = False

            elif self.player6InputActive:
                self.player6.isPlaying = True
                self.player6InputActive = False

            elif self.player7InputActive:
                self.player7.isPlaying = True
                self.player7InputActive = False

            elif self.player8InputActive:
                self.player8.isPlaying = True
                self.player8.InputActive = False
  
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
        

        removePlayer1 = self.myFont.render("Remove "+self.player1.name, True, (0,0,0))
        removePlayer2 = self.myFont.render("Remove "+self.player2.name, True, (0,0,0))
        removePlayer3 = self.myFont.render("Remove "+self.player3.name, True, (0,0,0))
        removePlayer4 = self.myFont.render("Remove "+self.player4.name, True, (0,0,0))
        removePlayer5 = self.myFont.render("Remove "+self.player5.name, True, (0,0,0))
        removePlayer6 = self.myFont.render("Remove "+self.player6.name, True, (0,0,0))
        removePlayer7 = self.myFont.render("Remove "+self.player7.name, True, (0,0,0))
        reomvePlayer8 = self.myFont.render("Remove "+self.player8.name, True, (0,0,0))

        removePlayer1Box = removePlayer1.get_rect(center = self.player1Rect.center)
        removePlayer2Box = removePlayer2.get_rect(center = self.player2Rect.center)
        removePlayer3Box = removePlayer3.get_rect(center = self.player3Rect.center)
        removePlayer4Box = removePlayer4.get_rect(center = self.player4Rect.center)
        removePlayer5Box = removePlayer5.get_rect(center = self.player5Rect.center)
        removePlayer6Box = removePlayer6.get_rect(center = self.player6Rect.center)
        removePlayer7Box = removePlayer7.get_rect(center = self.player7Rect.center)
        reomvePlayer8Box = reomvePlayer8.get_rect(center = self.player8Rect.center)

        addText = self.myFont.render("Add Player", True, (0,0,0))
        player1AddBox = addText.get_rect(center = self.player1Rect.center)
        player2AddBox = addText.get_rect(center = self.player2Rect.center)
        player3AddBox = addText.get_rect(center = self.player3Rect.center)
        player4AddBox = addText.get_rect(center = self.player4Rect.center)
        player5AddBox = addText.get_rect(center = self.player5Rect.center)
        player6AddBox = addText.get_rect(center = self.player6Rect.center)
        player7AddBox = addText.get_rect(center = self.player7Rect.center)
        player8AddBox = addText.get_rect(center = self.player8Rect.center)

        inputText1 = self.myFont.render("Input Name : "+self.player1.name, True, (0,0,0))
        inputText2 = self.myFont.render("Input Name : "+self.player2.name, True, (0,0,0))
        inputText3 = self.myFont.render("Input Name : "+self.player3.name, True, (0,0,0))
        inputText4 = self.myFont.render("Input Name : "+self.player4.name, True, (0,0,0))
        inputText5 = self.myFont.render("Input Name : "+self.player5.name, True, (0,0,0))
        inputText6 = self.myFont.render("Input Name : "+self.player6.name, True, (0,0,0))
        inputText7 = self.myFont.render("Input Name : "+self.player7.name, True, (0,0,0))
        inputText8 = self.myFont.render("Input Name : "+self.player8.name, True, (0,0,0))

        inputBox1 = inputText1.get_rect(center = self.player1Rect.center)
        inputBox2 = inputText2.get_rect(center = self.player2Rect.center)
        inputBox3 = inputText3.get_rect(center = self.player3Rect.center)
        inputBox4 = inputText4.get_rect(center = self.player4Rect.center)
        inputBox5 = inputText5.get_rect(center = self.player5Rect.center)
        inputBox6 = inputText6.get_rect(center = self.player6Rect.center)
        inputBox7 = inputText7.get_rect(center = self.player7Rect.center)
        inputBox8 = inputText8.get_rect(center = self.player8Rect.center)

        if self.player1.isPlaying: 
            screen.blit(removePlayer1, removePlayer1Box)
        elif self.player1InputActive:
            screen.blit(inputText1, inputBox1)
        else: 
            screen.blit(addText, player1AddBox)

        if self.player2.isPlaying: 
            screen.blit(removePlayer2, removePlayer2Box)
        elif self.player2InputActive:
            screen.blit(inputText2, inputBox2)
        else: 
            screen.blit(addText, player2AddBox)

        if self.player3.isPlaying: 
            screen.blit(removePlayer3, removePlayer3Box)
        elif self.player3InputActive:
            screen.blit(inputText3, inputBox3)
        else: 
            screen.blit(addText, player3AddBox)
            
        if self.player4.isPlaying: 
            screen.blit(removePlayer4, removePlayer4Box)
        elif self.player4InputActive:
            screen.blit(inputText4, inputBox4)
        else: 
            screen.blit(addText, player4AddBox)
            
        if self.player5.isPlaying: 
            screen.blit(removePlayer5, removePlayer5Box)
        elif self.player5InputActive:
            screen.blit(inputText5, inputBox5)
        else: 
            screen.blit(addText, player5AddBox)
            
        if self.player6.isPlaying: 
            screen.blit(removePlayer6, removePlayer6Box)
        elif self.player6InputActive:
            screen.blit(inputText6, inputBox6)
        else: 
            screen.blit(addText, player6AddBox)
        
        if self.player7.isPlaying: 
            screen.blit(removePlayer7, removePlayer7Box)
        elif self.player7InputActive:
            screen.blit(inputText7, inputBox7)
        else: 
            screen.blit(addText, player7AddBox)
        
        if self.player8.isPlaying: 
            screen.blit(removePlayer8, removePlayer8Box)
        elif self.player8InputActive:
            screen.blit(inputText8, inputBox8)
        else: 
            screen.blit(addText, player8AddBox)

    # Play Game Screen Functions
    def playGameMousePressed(self, x ,y):
        if self.backRect.collidepoint(x, y):
            self.gameMode = "configScreen"

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
        player1Name = self.myFont.render(self.player1.name, True, (0,0,0))
        player2Name = self.myFont.render(self.player2.name, True, (0,0,0))
        player3Name = self.myFont.render(self.player3.name, True, (0,0,0))
        player4Name = self.myFont.render(self.player4.name, True, (0,0,0))
        player5Name = self.myFont.render(self.player5.name, True, (0,0,0))
        player6Name = self.myFont.render(self.player6.name, True, (0,0,0))
        player7Name = self.myFont.render(self.player7.name, True, (0,0,0))
        player8Name = self.myFont.render(self.player8.name, True, (0,0,0))

        player1NameBox = player1Name.get_rect(center = self.player1Rect.center)
        player2NameBox = player2Name.get_rect(center = self.player2Rect.center)
        player3NameBox = player3Name.get_rect(center = self.player3Rect.center)
        player4NameBox = player4Name.get_rect(center = self.player4Rect.center)
        player5NameBox = player5Name.get_rect(center = self.player5Rect.center)
        player6NameBox = player6Name.get_rect(center = self.player6Rect.center)
        player7NameBox = player7Name.get_rect(center = self.player7Rect.center)
        player8NameBox = player8Name.get_rect(center = self.player8Rect.center)

        if self.player1.isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player1Rect.center, self.width/20)
            screen.blit(player1Name, player1NameBox)


        if self.player2.isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player2Rect.center, self.width/20)
            screen.blit(player2Name, player2NameBox)

        if self.player3.isPlaying: 

            pygame.draw.circle(screen, (75, 75, 75), self.player3Rect.center, self.width/20)
            screen.blit(player3Name, player3NameBox)
            
        if self.player4.isPlaying: 

            pygame.draw.circle(screen, (75, 75, 75), self.player4Rect.center, self.width/20)
            screen.blit(player4Name, player4NameBox)
            
        if self.player5.isPlaying: 
            pygame.draw.circle(screen, (75, 75, 75), self.player5Rect.center, self.width/20)
            screen.blit(player5Name, player5NameBox)
            
        if self.player6.isPlaying:
            pygame.draw.circle(screen, (75, 75, 75), self.player6Rect.center, self.width/20)
            screen.blit(player6Name, player6NameBox)
        
        if self.player7.isPlaying:           
            pygame.draw.circle(screen, (75, 75, 75), self.player7Rect.center, self.width/20)
            screen.blit(player7Name, player7NameBox)
        
        if self.player8.isPlaying:
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

class Player(object):
    def __init__(self, name):
        self.isPlaying = False
        self.stackSize = 0
        self.name = name


PokerGame().run()