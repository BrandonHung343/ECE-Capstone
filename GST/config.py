# Config File
class Player(object):
    def __init__(self, num):
        self.num = num
        self.name = ""
        self.isPlaying = False 
        self.inHand = False
        self.stackSize = 0
        self.isBetting = False
        self.betSize = 0

playerList = [Player(1), Player(2), Player(3), Player(4), Player(5), Player(6), Player(7), Player(8)]
chipValues = [1, 2, 5, 10, 20] # white, red, green, blue, black 
potSize = 0
gameMode = "config"
currAction = ""
rotateTime = 0