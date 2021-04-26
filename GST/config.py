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

'''# After Play Game is Pressed
def initializeGame():
    # Intialize Small Blind
    for player in playerList:
        if player.isPlaying:
            smallBlind = player.num
            break
            
    # Intialize Curr Player List (Prelop)
    currPlayers = []
    for i in range(smallBlind, 8):
        if playerList[i].isPlaying:
            currPlayers.append(i)

    for j in range(0, smallBlind):
        if playerList[j].isPlaying:
            currPlayers.append(j)

    tmpList = currPlayers[2:]+currPlayers[:2] # Adjust for UTG 
    currPlayers = tmpList'''


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