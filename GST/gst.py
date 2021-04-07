# Game State Tracker
import sys
print(sys.path)
sys.path.insert(1, './DealerUI')
sys.path.insert(1, './PlayerUI')
import dealerUI

class PokerStateTracker(object):
    def __init__(self):
        self.playerList = [Player(1), Player(2), Player(3), Player(4), Player(5), Player(6), Player(7), Player(8)]
        self.chipValues = [1, 2, 5, 10, 20] # white, red, green, blue, black 
        self.potSize = 0
        self.gameMode = "config"
        self.dealerGame = dealerUI.PokerGame()

    def run(self):
        # Intialize Poker Game and Player List
        self.dealerGame.run(self.playerList, self.potSize, self.gameMode, self.chipValues)
  
        # Main Loop
        playing = True
        inGame = (self.dealerGame.gameMode == "playGame")
    

class Player(object):
    def __init__(self, num):
        self.num = num
        self.name = ""
        self.isPlaying = False 
        self.inHand = False
        self.stackSize = 0
        self.isBetting = False
        self.betSize = 0

PokerStateTracker().run()



