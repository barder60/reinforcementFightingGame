LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'
ATT_LEFT = 'ATT_LEFT'
ATT_RIGHT = 'ATT_RIGHT'
BLOCK_LEFT = 'BLOCK_LEFT'
BLOCK_RIGHT = 'BLOCK_RIGHT'
NOTHING = 'NOTHING'

ACTIONS = [
    LEFT,
    RIGHT,
    NOTHING,
    ATT_LEFT,
    ATT_RIGHT,
    BLOCK_LEFT,
    BLOCK_RIGHT
]

class Player:
    def __init__(self, environment, start, learning_rate=1, discount_factor=0.5, life_point=100, last_action=NOTHING):
        self.__life_point = life_point
        self.__last_action = last_action
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        self.__start = start

        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

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
    def lifePoint(self):
        return self.__life_point

    @property
    def lastAction(self):
        return self.__last_action

    def best_action(self):
        best = None
        for a in self.__qtable[self.__state]:
            if not best \
                    or self.__qtable[self.__state][a] > self.__qtable[self.__state][best]:
                best = a
        return best

    def update(self, state, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * \
                                               (reward + self.__discount_factor * \
                                                maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__score += reward