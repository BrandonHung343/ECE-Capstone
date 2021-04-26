# Game State Tracker
import sys
sys.path.insert(1, '../DealerUI')
sys.path.insert(1, '../CompVision')
import dealerUI
import config

dealerGame = dealerUI.PokerGame()
dealerGame.run()


'''[1, 2, 3, 4, 5, 7]
smallBlind = 4
# Call at beginning of each game
def initCurrPlayers():
    start = config.smallBlind 
    newCurrPlayers = []
    for i in range(start, 8):
        if config.playerList[i].isPlaying:
            newCurrPlayers.append(i)

    for j in range(0, start)
        if config.playerList[j].isPlaying:
            newCurrPlayers.append(j)

    config.currPlayers = newCurrPlayers

    # should return [7, 1, 2, 3, 4, 5]

    # people may fold [7, 1, 3]
def preflopUpdate():
    [0, 1, 4, 5, 7] -> '''





