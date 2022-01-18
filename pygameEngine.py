import time

import pygame

from Environnement import Environment as GameBoard
from constant import GROUND, ATT_LEFT, ATT_RIGHT
from Player import Player
from utils import spritesheet

pygame.init()
screen = pygame.display.set_mode((828, 828))

from constantAssets import background, RED_BASIC_MOVEMENT_LEFT, RED_BASIC_MOVEMENT_RIGHT, BLUE_BASIC_MOVEMENT_LEFT, \
    BLUE_BASIC_MOVEMENT_RIGHT, RED_PUNCH_LEFT_START, RED_PUNCH_LEFT_DONE, RED_PUNCH_DOING, RED_PUNCH_RIGHT_DONE, \
    RED_PUNCH_RIGHT_START, RED_KO_START, RED_KO_DOING, RED_KO_DONE, BLUE_PUNCH_RIGHT_DONE, BLUE_PUNCH_RIGHT_START, \
    BLUE_PUNCH_DOING, BLUE_KO_DONE, BLUE_KO_DOING, BLUE_KO_START

RED_ANIMATIONS = [
    RED_BASIC_MOVEMENT_RIGHT,
    RED_BASIC_MOVEMENT_LEFT
]

RED_KO_ANIMATIONS = [
    RED_KO_START,
    RED_KO_DOING,
    RED_KO_DONE
]

BLUE_KO_ANIMATIONS = [
    BLUE_KO_START,
    BLUE_KO_DOING,
    BLUE_KO_DONE
]

BLUE_PUNCH_RIGHT_ANIMATION = [
    BLUE_PUNCH_RIGHT_START,
    BLUE_PUNCH_DOING,
    BLUE_PUNCH_RIGHT_DONE
]

BLUE_PUNCH_LEFT_ANIMATION = [
    BLUE_PUNCH_RIGHT_START,
    BLUE_PUNCH_DOING,
    BLUE_PUNCH_RIGHT_DONE
]

RED_PUNCH_RIGHT_ANIMATION = [
    RED_PUNCH_RIGHT_START,
    RED_PUNCH_DOING,
    RED_PUNCH_RIGHT_DONE
]

RED_PUNCH_LEFT_ANIMATION = [
    RED_PUNCH_LEFT_START,
    RED_PUNCH_DOING,
    RED_PUNCH_LEFT_DONE
]

clock = pygame.time.Clock()
lastUpdated = pygame.time.get_ticks()


def getDistance(playerPosition: Player, oponentPosition: Player):
    return playerPosition.state[0] - oponentPosition.state[0], playerPosition.state[1] - oponentPosition.state[1]


def displayPosition(PlayerOne, PlayerTwo):
    for i in range(5):
        string = ""
        for y in range(5):
            if i == 0 or y == 0 or i == 4 or y == 4:
                string = string + '#'
            elif PlayerOne.state[0] == i and PlayerOne.state[1] == y:
                string = string + '1'
            elif PlayerTwo.state[0] == i and PlayerTwo.state[1] == y:
                string = string + '2'
            else:
                string = string + ' '
        print(string)


def StartPygame():
    screen.blit(background, background.get_rect())
    running = True
    isFinished = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)

        if isFinished:
            running = False

        env = GameBoard(GROUND)
        print(env.playerOnePosition)
        print(env.playerTwoPosition)
        PlayerOne = Player(env, env.playerOnePosition, "red")
        PlayerTwo = Player(env, env.playerTwoPosition, "blue")
        running = False
        for i in range(20):
            time.sleep(1)
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
                    loopVisualBoxer(PlayerOne, screen, dead=True)
                    continue

                playerDoesAction(PlayerOne, PlayerTwo, env)

                loopVisualBoxer(PlayerOne, screen)

                if PlayerTwo.isDead():
                    isFinished = True
                    loopVisualBoxer(PlayerTwo, screen, dead=True)
                    continue

                playerDoesAction(PlayerTwo, PlayerOne, env)

                loopVisualBoxer(PlayerTwo, screen)

                count = count + 1

            print("PASSAGE NUMERO " + str(i))
            print("JOUEUR 1 : " + str(PlayerOne.score))
            print("JOUEUR 2 : " + str(PlayerTwo.score))

        print(PlayerOne.qtable[(1, 0)][ATT_LEFT])
        print(PlayerOne.qtable[(1, 0)][ATT_RIGHT])
        print(PlayerTwo.qtable[(-1, 0)][ATT_RIGHT])
        print(PlayerTwo.qtable[(-1, 0)][ATT_LEFT])

    pygame.quit()


def positionVisual(player):
    return (player.state[0] * 200, player.state[1] * 200)


def loopVisualBoxer(player, screen, dead=False):
    if player.last_animation != "":
        player.last_animation = player.last_animation.move(2000, 2000)
    if dead == True:
        if player.color == "red":
            player.last_animation = screen.blit(RED_KO_ANIMATIONS[2], positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_KO_ANIMATIONS[2], positionVisual(player))
    elif player.lastAction == "ATT_RIGHT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_RIGHT_ANIMATION[2], positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_RIGHT_ANIMATION[2], positionVisual(player))
    elif player.lastAction == "DOWN":
        if player.color == "red":
            player.last_animation = screen.blit(RED_BASIC_MOVEMENT_RIGHT, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_BASIC_MOVEMENT_RIGHT, positionVisual(player))
    elif player.lastAction == "UP":
        if player.color == "red":
            player.last_animation = screen.blit(RED_BASIC_MOVEMENT_RIGHT, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_BASIC_MOVEMENT_RIGHT, positionVisual(player))

    pygame.display.update()
    print(player.color, player.lastAction)

    pygame.display.update()
