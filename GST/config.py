# Config File
class Player(object):
    def __init__(self, num):
        self.num = num
        #self.deg = deg
        self.name = ""
        self.isPlaying = False  # Sitting at the Table
        self.inHand = False # Folded or not folded
        self.stackSize = 0
        self.isBetting = False
        self.betSize = 0
        self.isDealer = False

playerList = [Player(0), Player(1), Player(2), Player(3), Player(4), Player(5), Player(6), Player(7)]
#currPlayers = [4, 5, 7, 1, 2, 3]
smallBlind = 4
chipValues = [1, 2, 5, 10, 20] # white, red, green, blue, black 
potSize = 0
gameMode = "config"
roundMode = "preflop"
currAction = ""
rotateTime = 0