from pygameEngine import StartPygame
from Player import Player
from Environnement import Environment as GameBoard
from constant import GROUND, NOTHING

if __name__ == '__main__':


    env = GameBoard(GROUND)
    PlayerOne = Player(env, env.playerOnePosition)
    PlayerTwo = Player(env, env.playerTwoPosition)

    StartPygame()


    print(env.states)
    print(PlayerOne.qtable)
    print(PlayerTwo.qtable)
    print(PlayerOne.best_action((0,1),NOTHING))
    print(env.playerOnePosition)
    print(env.playerTwoPosition)