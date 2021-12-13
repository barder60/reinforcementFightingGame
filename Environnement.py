from constant import PLAYER_ONE_POSITION, PLAYER_TWO_POSITION, REWARD_GET_HIT, REWARD_LOSE, HEAVY_ATT_RIGHT, \
    HEAVY_ATT_LEFT, LEFT, RIGHT, UP, DOWN, BLOCK_LEFT, BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT


class Environment:
    def __init__(self, text):
        self.__states = {}
        lines = list(map(lambda x: x.strip(), text.strip().split('\n')))
        self.__lineLength = len(lines) - 2
        print(self.__lineLength)
        self.__rowLength = len(lines[0]) - 2
        print(self.__rowLength)
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]
                if lines[row][col] == PLAYER_ONE_POSITION:
                    self.__playerOnePosition = (row, col)
                elif lines[row][col] == PLAYER_TWO_POSITION:
                    self.__playerTwoPosition = (row, col)


    def apply(self, player, opponent, action):
        if action == LEFT:
            new_state = (player.state[0], player.state[1] - 1)
        elif action == RIGHT:
            new_state = (player.state[0], player.state[1] + 1)
        elif action == UP:
            new_state = (player.state[0] - 1, player.state[1])
        elif action == DOWN:
            new_state = (player.state[0] + 1, player.state[1])
        elif action == BLOCK_LEFT:
            # TODO : TRAITEMENT DE BLOCK

            return
        elif action == BLOCK_RIGHT:
            # TODO : TRAITEMENT DE BLOCK
            return
        elif action == ATT_LEFT:
            # TODO : TRAITEMENT DE BLOCK POSITION
            if opponent.__last_action is not BLOCK_RIGHT and player.state[0] is opponent.state[0]:
                reward = REWARD_GET_HIT
                opponent.takeHit()
            return
        elif action == ATT_RIGHT:
            if opponent.__last_action is not BLOCK_LEFT:
                reward = REWARD_GET_HIT
                opponent.takeHit()
            return
        elif action == HEAVY_ATT_RIGHT:
            reward = REWARD_GET_HIT
            opponent.takeHit()
        elif action == HEAVY_ATT_LEFT:
            reward = REWARD_GET_HIT
            opponent.takeHit()

        if new_state in self.__states:
            state = new_state
        else:
            reward = REWARD_LOSE

        player.lastAction = action
        player.update((1,2), opponent.last_action, action, state, reward) #TODO RECUPERER LA DISTANCE
        print(self.__states)


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
