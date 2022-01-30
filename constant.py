import pygame

GROUND = """
    #####
    # 2 #
    #   #
    # 1 #
    #####
"""
# SETTING
LOOP_SPEED = 0.01
MAX_DELAY = 2
MID_DELAY = 1
MAX_TIMER = 200
REPEAT_NB = 100
LOAD_QTABLE = False

# POSITION
PLAYER_ONE_POSITION = '1'
PLAYER_TWO_POSITION = '2'
WALL = '#'

# REWARDS
REWARD_WIN = 100
REWARD_LOSE = -100
REWARD_BORDER = -10
REWARD_NOTHING = -20

REWARD_GET_HIT = -15
REWARD_DIRECT_HIT = 10

REWARD_INTERRUPT = 20
REWARD_GET_INTERRUPT = -10

REWARD_GET_HEAVY_HIT = -35
REWARD_DIRECT_HEAVY_HIT = 30

REWARD_BLOCKED_HIT = 10
REWARD_GET_BREAK = -20
REWARD_BREAK_BLOCK = 20

RUN_IN_OPPONENT = -15
REWARD_MOVE = -1

REWARD_MISS = -40
REWARD_HIT_IN_BLOCK = -10


#ACTIONS
LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'
ATT_LEFT = 'ATT_LEFT'
ATT_RIGHT = 'ATT_RIGHT'
HEAVY_ATT_LEFT = 'H_ATT_LEFT'
HEAVY_ATT_RIGHT = 'H_ATT_RIGHT'
BLOCK_LEFT = 'BLOCK_LEFT'
BLOCK_RIGHT = 'BLOCK_RIGHT'
NOTHING = 'NOTHING'

ACTIONS = [
    LEFT,
    RIGHT,
    UP,
    DOWN,
    NOTHING,
    ATT_RIGHT,
    ATT_LEFT,
    HEAVY_ATT_LEFT,
    HEAVY_ATT_RIGHT,
    BLOCK_LEFT,
    BLOCK_RIGHT
]

# STATS
STARTING_LIFE_POINT = 100

#DAMAGE
HIT_DMG = 5
HEAVY_HIT_DMG = 10
HEAVY_HIT_ON_BLOCK_DMG = 7

