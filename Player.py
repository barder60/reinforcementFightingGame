from constant import NOTHING, ACTIONS, HIT_DMG, HEAVY_HIT_DMG


class Player:
    def __init__(self, environment, start, color, learning_rate=1, discount_factor=0.5, life_point=100, last_action=NOTHING):
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

        for line in range(-self.__environment.lineLength, self.__environment.lineLength):
            for row in range(-self.__environment.rowLength, self.__environment.rowLength):
                distance = (line, row)
                self.__qtable[distance] = {}
                for other_player_action in ACTIONS:
                    self.__qtable[distance][other_player_action] = {}
                    for player_action in ACTIONS:
                        self.__qtable[distance][other_player_action][player_action] = 0.0

        self.reset()

    def reset(self):
        self.__state = self.__start
        self.__score = 0

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
    def delay(self,delay):
        self.__delay = delay

    def takeHit(self):
        self.__life_point = self.__life_point - HIT_DMG

    def takeHeavyHit(self):
        self.__life_point = self.__life_point - HEAVY_HIT_DMG

    def isDead(self):
        return self.__life_point <= 0

    @property
    def lastAction(self):
        return self.__last_action

    @property
    def score(self):
        return self.__score

    @property
    def color(self):
        return self.__color

    @property
    def last_animation(self):
        return self.__last_animation

    @last_animation.setter
    def last_animation(self, last_animation):
        self.__last_animation = last_animation

    def best_action(self, distance, other_player_last_action):
        best = None
        #print(self.__qtable[distance][other_player_last_action])
        for a in self.__qtable[distance][other_player_last_action]:
            if not best \
                    or self.__qtable[distance][other_player_last_action][a] > self.__qtable[distance][other_player_last_action][best]:
                best = a
        return best

    def update(self, distance, other_player_action, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        maxQ = max(self.__qtable[distance][other_player_action].values())
        self.__qtable[distance][other_player_action][action] += self.__learning_rate * \
                                               (reward + self.__discount_factor * \
                                                maxQ - self.__qtable[distance][other_player_action][action])
        #print(self.__qtable[distance][other_player_action][action])

        self.__score += reward

    def setState(self, newState):
        self.__state = newState

    def setLastAction(self, newLastAction):
        self.__last_action = newLastAction