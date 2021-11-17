LEFT = 'LEFT'
RIGHT = 'RIGHT'
ATT_UP = 'ATT_UP'
DEF_UP = 'DEF_UP'
ATT_MID = 'ATT_MID'
DEF_MID = 'DEF_MID'
ATT_DOWN = 'ATT_DOWN'
DEF_DOWN = 'DEF_DOWN'

ACTIONS = [
    LEFT,
    RIGHT,
    ATT_UP,
    DEF_UP,
    ATT_MID,
    DEF_MID,
    ATT_DOWN,
    DEF_DOWN
]

class Player:
    def __init__(self, environment, start, learning_rate=1, discount_factor=0.5):
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
    def state(self):
        return self.__state

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