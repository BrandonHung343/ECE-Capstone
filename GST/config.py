# Config File
class Player(object):
    def __init__(self, num, degrees):
        self.num = num
        self.degrees = degrees
        self.name = ""
        self.isPlaying = False 
        self.inHand = False 
        self.stackSize = 50
        self.betList = []

playerList = [Player(0, 60), Player(1, 90), Player(2, 120), Player(3, 140), Player(4, 220), Player(5, 240), Player(6, 270), Player(7, 300)]
currPlayers = []
endPlayer = 0
smallBlind = 0
bigBlind = 1
chipValues = [1, 2, 5, 10, 20] # white, red, green, blue, black 
potSize = 0
gameMode = "config"
roundMode = "none"
rotateTime = 0
maxBet = 2
BBVal = 2
winState = False
