import time

import pygame
from pygame.sprite import Sprite

from Environnement import Environment as GameBoard
from constant import GROUND, ATT_LEFT, ATT_RIGHT, STARTING_LIFE_POINT, LOOP_SPEED, MAX_TIMER, REPEAT_NB
from Player import Player
from utils import spritesheet

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((828, 828))

from constantAssets import background, RED_BASIC_MOVEMENT_LEFT, RED_BASIC_MOVEMENT_RIGHT, BLUE_BASIC_MOVEMENT_LEFT, \
    BLUE_BASIC_MOVEMENT_RIGHT, RED_PUNCH_LEFT_START, RED_PUNCH_LEFT_DONE, RED_PUNCH_DOING, RED_PUNCH_RIGHT_DONE, \
    RED_PUNCH_RIGHT_START, RED_KO_START, RED_KO_DOING, RED_KO_DONE, BLUE_PUNCH_RIGHT_DONE, BLUE_PUNCH_RIGHT_START, \
    BLUE_PUNCH_DOING, BLUE_KO_DONE, BLUE_KO_DOING, BLUE_KO_START, BLUE_PUNCH_RIGHT_HIGH, RED_PUNCH_RIGHT_HIGH, \
    RED_PUNCH_LEFT_HIGH, BLUE_PUNCH_LEFT_HIGH, BLUE_PUNCH_RIGHT_BLOCK, RED_PUNCH_RIGHT_BLOCK, RED_PUNCH_LEFT_BLOCK, \
    BLUE_PUNCH_LEFT_BLOCK

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

def StartPygame():
    screen.blit(background, background.get_rect())
    running = True
    isFinished = False
    listResult = []



    clock.tick(30)
    env = GameBoard(GROUND)
    PlayerOne = Player(env, env.playerOnePosition, "red", STARTING_LIFE_POINT)
    PlayerTwo = Player(env, env.playerTwoPosition, "blue", STARTING_LIFE_POINT)
    forceQuit = False
    for repeat in range(REPEAT_NB):
        timer = 0
        PlayerOne.reset()
        PlayerTwo.reset()
        isFinished = False
        if forceQuit:
            break

        while not isFinished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isFinished = True
                    forceQuit = True
                    continue

            if timer == MAX_TIMER:
                isFinished = True
                continue

            if PlayerOne.isDead():
                isFinished = True
                PlayerTwo.add_win_score()
                continue

            distance = env.getDistance(PlayerOne.state, PlayerTwo.state)
            if PlayerOne.delay > 0:
                bestAction = PlayerOne.lastAction
                print("JOUEUR 1 : " + str(distance) + " -> WAS ALREADY PREPARING " + bestAction)
            else:
                bestAction = PlayerOne.best_action(distance, PlayerTwo.lastAction, PlayerTwo.delay)
                print("JOUEUR 1 : " + str(distance) + " -> " + bestAction)

            displayPosition(PlayerOne, PlayerTwo)
            env.apply(PlayerOne, PlayerTwo, bestAction, distance)
            loopVisualBoxer(PlayerOne, PlayerTwo, screen,timer, repeat)
            time.sleep(float(LOOP_SPEED))

            if PlayerTwo.isDead():
                isFinished = True
                PlayerOne.add_win_score()
                continue

            # print("JOUEUR 2")
            distance = env.getDistance(PlayerTwo.state, PlayerOne.state)
            if PlayerTwo.delay > 0:
                bestAction = PlayerTwo.lastAction
                print("JOUEUR 2 : " + str(distance) + " -> WAS ALREADY PREPARING " + bestAction)
            else:
                bestAction = PlayerTwo.best_action(distance, PlayerOne.lastAction, PlayerOne.delay)
                print("JOUEUR 2 : " + str(distance) + " -> " + bestAction)

            displayPosition(PlayerOne, PlayerTwo)
            env.apply(PlayerTwo, PlayerOne, bestAction, distance)
            loopVisualBoxer(PlayerOne, PlayerTwo, screen, timer, repeat)
            time.sleep(LOOP_SPEED)


            timer = timer + 1

        listResult.append((PlayerOne.score,PlayerTwo.score,timer))
        print("PASSAGE NUMERO " + str(repeat))
        print("JOUEUR 1 : " + str(PlayerOne.score))
        print("JOUEUR 2 : " + str(PlayerTwo.score))

        #print(PlayerOne.qtable[(1, 0)][ATT_LEFT])
        #print(PlayerOne.qtable[(1, 0)][ATT_RIGHT])
        #print(PlayerTwo.qtable[(-1, 0)][ATT_RIGHT])
        #print(PlayerTwo.qtable[(-1, 0)][ATT_LEFT])

    pygame.quit()
    print(listResult)


def positionVisual(player):
    #print(player.state)
    return (player.state[1] * 200, player.state[0] * 200)


def loopVisualBoxer(player, playerTwo, screen, remainingTime, repeat):
    screen.blit(background, background.get_rect())
    scorePlayerOne = myfont.render(str(player.score), False, (255, 0, 0))
    scorePlayerTwo = myfont.render(str(playerTwo.score), False, (0, 0, 255))
    timer = myfont.render("temps restant : " + str(MAX_TIMER - remainingTime), False, (0, 0, 0))
    repeatNumber = myfont.render(str(repeat) + " sur " + str(REPEAT_NB), False, (0, 0, 0))
    screen.blit(scorePlayerOne, (25,15))
    screen.blit(scorePlayerTwo, (700, 15))
    screen.blit(repeatNumber, (400, 5))
    screen.blit(timer, (350, 20))

    draw_health_bar_player_one = pygame.Rect(0, 0, STARTING_LIFE_POINT, 7)
    pygame.draw.rect(screen, (255, 0, 0), draw_health_bar_player_one)
    draw_health_player_one = pygame.Rect(0, 0, player.lifePoint, 7)
    pygame.draw.rect(screen, (0, 255, 0), draw_health_player_one)

    draw_health_bar_player_two = pygame.Rect(700, 0, STARTING_LIFE_POINT, 7)
    pygame.draw.rect(screen, (255, 0, 0), draw_health_bar_player_two)
    draw_health_player_two = pygame.Rect(700, 0, playerTwo.lifePoint, 7)
    pygame.draw.rect(screen, (0, 255, 0), draw_health_player_two)

    displayPlayer(player, screen)
    displayPlayer(playerTwo, screen)


    pygame.display.update()



def displayPlayer(player, screen):
    if player.isDead() == True:
        if player.color == "red":
            player.last_animation = screen.blit(RED_KO_ANIMATIONS[2], positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_KO_ANIMATIONS[2], positionVisual(player))
    elif player.lastAction == "ATT_LEFT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_LEFT_ANIMATION[2], positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_LEFT_ANIMATION[2], positionVisual(player))
    elif player.lastAction == "ATT_RIGHT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_RIGHT_ANIMATION[2], positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_RIGHT_ANIMATION[2], positionVisual(player))
    elif player.lastAction == "H_ATT_LEFT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_LEFT_HIGH, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_LEFT_HIGH, positionVisual(player))
    elif player.lastAction == "H_ATT_RIGHT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_RIGHT_HIGH, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_RIGHT_HIGH, positionVisual(player))
    elif player.lastAction == "BLOCK_LEFT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_LEFT_BLOCK, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_LEFT_BLOCK, positionVisual(player))
    elif player.lastAction == "BLOCK_RIGHT":
        if player.color == "red":
            player.last_animation = screen.blit(RED_PUNCH_RIGHT_BLOCK, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_PUNCH_RIGHT_BLOCK, positionVisual(player))
    else:
        if player.color == "red":
            player.last_animation = screen.blit(RED_BASIC_MOVEMENT_RIGHT, positionVisual(player))
        else:
            player.last_animation = screen.blit(BLUE_BASIC_MOVEMENT_LEFT, positionVisual(player))

