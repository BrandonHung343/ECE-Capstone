# Config File
class Player(object):
    def __init__(self, num, degrees):
        self.num = num
        self.degrees = degrees
        self.name = ""
        self.isPlaying = False 
        self.inHand = False 
        self.stackSize = 200
        self.betList = []

playerList = [Player(0, 40), Player(1, 65), Player(2, 90), Player(3, 115), Player(4, 150), Player(5, 175), Player(6, 200), Player(7, 225)]
#playerList = [Player(0, 60), Player(1, 80), Player(2, 100), Player(3, 120), Player(4, 140), Player(5, 160), Player(6, 180), Player(7, 200)]
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
