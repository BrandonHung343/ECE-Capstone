# Game State Tracker
import sys
print(sys.path)
sys.path.insert(1, './DealerUI')
import dealerUI

class PokerStateTracker(object):
    def __init__(self):
        self.dealerGame = dealerUI.PokerGame()

    def run(self):
        self.dealerGame.run()
   

PokerStateTracker().run()



