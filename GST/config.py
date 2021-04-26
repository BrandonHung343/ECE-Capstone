# Config File
class Player(object):
    def __init__(self, num):
        self.num = num
        #self.degrees = deg
        self.name = ""
        self.isPlaying = False 
        self.inHand = False 
        self.stackSize = 50
        self.betList = []

playerList = [Player(0), Player(1), Player(2), Player(3), Player(4), Player(5), Player(6), Player(7)]
currPlayers = []
endPlayer = 0
smallBlind = 0
chipValues = [1, 2, 5, 10, 20] # white, red, green, blue, black 
potSize = 0
gameMode = "config"
roundMode = "none"
currAction = ""
rotateTime = 0
maxBet = 2
BBVal = 2
