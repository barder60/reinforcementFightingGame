from pygameEngine import StartPygame
from Player import Player
from Environnement import Environment as GameBoard
from constant import GROUND


def getDistance(playerPosition: Player, oponentPosition: Player):
    return playerPosition.state[0] - oponentPosition.state[0], playerPosition.state[1] - oponentPosition.state[1]


if __name__ == '__main__':
    env = GameBoard(GROUND)
    PlayerOne = Player(env, env.playerOnePosition)
    PlayerTwo = Player(env, env.playerTwoPosition)

    #StartPygame()

    isFinished = False

    for i in range(90):
        count = 0
        PlayerOne.reset()
        PlayerTwo.reset()
        isFinished = False
        while not isFinished:

            if count == 90:
                isFinished = True
                continue

            if PlayerOne.isDead():
                isFinished = True
                continue

            #print("JOUEUR 1 POSITION COURANTE : " + str(PlayerOne.state))
            distance = getDistance(PlayerOne, PlayerTwo)
            bestAction = PlayerOne.best_action(distance, PlayerTwo.lastAction)
            #print(bestAction)

            env.apply(PlayerOne, PlayerTwo, bestAction, distance)

            if PlayerTwo.isDead():
                isFinished = True
                continue

            #print("JOUEUR 2")
            distance = getDistance(PlayerTwo, PlayerOne)
            bestAction = PlayerTwo.best_action(distance, PlayerOne.lastAction)
            #print(bestAction)
            env.apply(PlayerTwo, PlayerOne, bestAction, distance)

            count = count + 1
        print("PASSAGE NUMERO " + str(i))
        print("JOUEUR 1 : " + str(PlayerOne.score))
        print("JOUEUR 2 : " + str(PlayerTwo.score))

    print(PlayerOne.qtable)
