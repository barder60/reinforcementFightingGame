from constant import PLAYER_ONE_POSITION, PLAYER_TWO_POSITION, REWARD_LOSE, HEAVY_ATT_RIGHT, \
    HEAVY_ATT_LEFT, LEFT, RIGHT, UP, DOWN, BLOCK_LEFT, BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT, WALL, RUN_IN_OPPONENT, \
    REWARD_BORDER, REWARD_DIRECT_HIT


class Environment:
    def __init__(self, text):
        self.__states = {}
        lines = list(map(lambda x: x.strip(), text.strip().split('\n')))
        self.__lineLength = len(lines) - 2
        self.__rowLength = len(lines[0]) - 2

        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]
                if lines[row][col] == PLAYER_ONE_POSITION:
                    self.__playerOnePosition = (row, col)
                elif lines[row][col] == PLAYER_TWO_POSITION:
                    self.__playerTwoPosition = (row, col)

    def apply(self, player, opponent, action, distance):
        reward = 0
        new_state = None

        if action == LEFT:
            new_state = (player.state[0], player.state[1] - 1)
        elif action == RIGHT:
            new_state = (player.state[0], player.state[1] + 1)
        elif action == UP:
            new_state = (player.state[0] - 1, player.state[1])
        elif action == DOWN:
            new_state = (player.state[0] + 1, player.state[1])

        elif action == ATT_LEFT:
            if opponent.lastAction is not BLOCK_LEFT \
                    and (player.state[0] is opponent.state[0] or player.state[1] is opponent.state[1]):
                reward = REWARD_DIRECT_HIT
                opponent.takeHit()
        elif action == ATT_RIGHT:
            if opponent.lastAction is not BLOCK_RIGHT \
                    and (player.state[0] is opponent.state[0] or player.state[1] is opponent.state[1]):
                reward = REWARD_DIRECT_HIT
                opponent.takeHit()
        elif action == HEAVY_ATT_RIGHT:
            player.delay = 1  # TODO gestion du delai
            return
        elif action == HEAVY_ATT_LEFT:
            player.delay = 1  # TODO gestion du delai
            return

        if new_state is not None and new_state in self.__states:
            if new_state == opponent.state:
                reward = RUN_IN_OPPONENT
                player.update(distance, opponent.lastAction, action, reward)
                new_state = player.state
            if self.__states[new_state] == WALL:
                #print("JE PREND UN MUR")
                reward = REWARD_BORDER
                player.update(distance, opponent.lastAction, action, reward)
                new_state = player.state
            else:
                reward = -1
                player.update(distance, opponent.lastAction, action, reward)

            player.setState(new_state)

        else:
            reward = REWARD_LOSE
            player.update(distance, opponent.lastAction, action, reward)

        player.setLastAction(action)

    @property
    def playerOnePosition(self):
        return self.__playerOnePosition

    @property
    def playerTwoPosition(self):
        return self.__playerTwoPosition

    @property
    def states(self):
        return self.__states

    @property
    def lineLength(self):
        return self.__lineLength

    @property
    def rowLength(self):
        return self.__rowLength
