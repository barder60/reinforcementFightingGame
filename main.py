from pygameEngine import StartPygame
from Player import Player
from Environnement import Environment as GameBoard
from constant import GROUND


def getDistance(playerPosition: Player, oponentPosition: Player):
    return playerPosition.state[0] - oponentPosition.state[0], playerPosition.state[1] - oponentPosition.state[1]


if __name__ == '__main__':
    StartPygame()

