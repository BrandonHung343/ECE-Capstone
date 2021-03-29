# Game State Tracker
import sys
sys.path.insert(1, './DealerUI/')
from dealerUI import *

class PokerStateTracker(object):
    def __init__(self):
        self.numPlayers = 0 # Number of Players at Table
        self.currDealer = 0 # Where the Dealer Chip is
        self.gameMode = "configuration" # Game Mode (confiugartion, playGame, etc.)

        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player3 = Player(3)
        self.player4 = Player(4)
        self.player5 = Player(5)
        self.player6 = Player(6)
        self.player7 = Player(7)
        self.player8 = Player(8)

dealerUI.PokerGame().run()


