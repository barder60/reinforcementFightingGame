import pickle
from random import random, choice

from constant import NOTHING, ACTIONS, HIT_DMG, HEAVY_HIT_DMG, HEAVY_HIT_ON_BLOCK_DMG, REWARD_GET_HIT, \
    REWARD_GET_HEAVY_HIT, REWARD_BLOCKED_HIT, REWARD_GET_BREAK, HEAVY_ATT_LEFT, HEAVY_ATT_RIGHT, BLOCK_LEFT, \
    BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT, MAX_DELAY, REWARD_INTERRUPT, REWARD_WIN, REWARD_GET_INTERRUPT, MID_DELAY


class Player:
    def __init__(self, environment, start, color, life_point, learning_rate=1, discount_factor=0.5,
                 last_action=NOTHING):
        self.__life_point = life_point
        self.__last_action = last_action
        self.__delay = 0
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        self.__start = start
        self.__color = color
        self.__last_animation = ""
        self.__exploration = 1.0

        self.__opponent_action_on_delay = None
        self.__distance_on_delay = None
        self.__opponent_delay_on_delay = 0

        for line in range(-self.__environment.lineLength, self.__environment.lineLength):
            for row in range(-self.__environment.rowLength, self.__environment.rowLength):
                distance = (line, row)
                self.__qtable[distance] = {}
                for other_player_action in ACTIONS:
                    self.__qtable[distance][other_player_action] = {}
                    for oponent_delay in range(MAX_DELAY + 1):
                        self.__qtable[distance][other_player_action][oponent_delay] = {}
                        for player_action in ACTIONS:
                            self.__qtable[distance][other_player_action][oponent_delay][player_action] = 0.0

        self.reset()

    def reset(self):
        self.__state = self.__start
        self.__score = 0
        self.__life_point = 100
        self.__delay = 0
        self.__opponent_action_on_delay \
            = None

    @property
    def start_position(self):
        return self.start_position

    @property
    def state(self):
        return self.__state

    @property
    def qtable(self):
        return self.__qtable

    @property
    def lifePoint(self):
        return self.__life_point

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, delay):
        self.__delay = delay

    def takeHit(self, hit, distance):
        self.__life_point = self.__life_point - HIT_DMG
        print("JE PREND LE COUP " + self.__last_action + " DISTANCE : " + str(self.__distance_on_delay) + "SUR LACTION : " + str(hit) + " avec delay : " + str(MID_DELAY))
        self.update(distance, hit, self.__last_action, REWARD_GET_HIT, MID_DELAY)
        print(self.qtable[distance][hit][MID_DELAY])

    def cancelPlayerAttack(self):
        print("INTERUPTION " + self.__last_action + " DISTANCE : " + str(self.__distance_on_delay) + "SUR LACTION : " + self.__opponent_action_on_delay)
        self.update(self.__distance_on_delay, self.__opponent_action_on_delay, self.__last_action, REWARD_GET_INTERRUPT, self.opponent_delay_on_delay)
        self.__delay = 1
        self.__last_action = NOTHING

    def takeHeavyHit(self, heavy_hit, distance):
        self.__life_point = self.__life_point - HEAVY_HIT_DMG
        self.update(distance, heavy_hit, self.__last_action, REWARD_GET_HEAVY_HIT, MID_DELAY)

    def takeHeavyHitOnBlock(self, heavy_hit, distance):
        self.__life_point = self.__life_point - HEAVY_HIT_ON_BLOCK_DMG
        print("JE ME PREND l'attaque suivante " + heavy_hit + " " + str(MID_DELAY) + " " + str(distance) +
              "avec REWARD = " + str(REWARD_GET_BREAK) + " MON ACTION = " + self.lastAction)
        self.update(distance, heavy_hit, self.lastAction, REWARD_GET_BREAK, MID_DELAY)

    def block_hit(self, hit, distance):
        print("SOMEONE BLOCK")
        self.update(distance, hit, self.lastAction, REWARD_BLOCKED_HIT, MAX_DELAY)

    def attack_on_block(self):
        self.delay = 1

    def isDead(self):
        return self.__life_point <= 0

    @property
    def lastAction(self):
        return self.__last_action

    @property
    def score(self):
        return self.__score

    def add_win_score(self):
        self.__score += REWARD_WIN

    @property
    def color(self):
        return self.__color

    @property
    def last_animation(self):
        return self.__last_animation

    @last_animation.setter
    def last_animation(self, last_animation):
        self.__last_animation = last_animation

    def best_action(self, distance, other_player_last_action, other_player_delay):

        if random() < self.__exploration:
            best = choice(ACTIONS)  # une action au hasard
            self.__exploration *= 0.99
        else:
            best = None
            print(other_player_last_action + " avec " + str(other_player_delay))
            print(self.__qtable[distance][other_player_last_action][other_player_delay])
            for a in self.__qtable[distance][other_player_last_action][other_player_delay]:
                if not best \
                        or self.__qtable[distance][other_player_last_action][other_player_delay][a] > \
                        self.__qtable[distance][other_player_last_action][other_player_delay][best]:
                    best = a
        return best

    def update(self, distance, other_player_action, action, reward, opponent_delay):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        maxQ = max(self.__qtable[distance][other_player_action][opponent_delay].values())
        self.__qtable[distance][other_player_action][opponent_delay][action] += self.__learning_rate * \
                                                                                (reward + self.__discount_factor *
                                                                                 maxQ - self.__qtable[distance][
                                                                                     other_player_action]
                                                                                 [opponent_delay][action])

        self.__score += reward

    def setState(self, newState):
        self.__state = newState

    def setLastAction(self, newLastAction):
        self.__last_action = newLastAction

    @property
    def opponent_action_on_delay(self):
        return self.__opponent_action_on_delay

    @opponent_action_on_delay.setter
    def opponent_action_on_delay(self, value):
        self.__opponent_action_on_delay = value

    @property
    def distance_on_delay(self):
        return self.__distance_on_delay

    @distance_on_delay.setter
    def distance_on_delay(self, value):
        self.__distance_on_delay = value

    @property
    def opponent_delay_on_delay(self):
        return self.__opponent_delay_on_delay

    @opponent_delay_on_delay.setter
    def opponent_delay_on_delay(self, value):
        self.__opponent_delay_on_delay = value



    def prepareHeavyAttack(self):
        return self.lastAction == HEAVY_ATT_LEFT or self.lastAction == HEAVY_ATT_RIGHT

    def prepareSimpleAttack(self):
        return self.lastAction == ATT_LEFT or self.lastAction == ATT_RIGHT

    def isBlocking(self):
        return self.lastAction is BLOCK_LEFT or self.lastAction is BLOCK_RIGHT

    def isNotBlocking(self):
        return not self.isBlocking()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)