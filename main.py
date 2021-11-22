from Player import Player
from Environnement import Environment as GameBoard


GROUND = """
    #####
    # 2 #
    #   #
    # 1 #
    #####
"""

if __name__ == '__main__':
    env = GameBoard(GROUND)
    PlayerOne = Player(env, env.playerOnePosition)
    PlayerTwo = Player(env, env.playerTwoPosition)


    print(env.states)