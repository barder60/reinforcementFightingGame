from Player import Player
from Environnement import Environment as GameBoard
from constant import GROUND

if __name__ == '__main__':
    env = GameBoard(GROUND)
    PlayerOne = Player(env, env.playerOnePosition)
    PlayerTwo = Player(env, env.playerTwoPosition)


    print(env.states)
    print(PlayerOne.qtable)
    print(PlayerTwo.qtable)
    print(env.playerOnePosition)
    print(env.playerTwoPosition)