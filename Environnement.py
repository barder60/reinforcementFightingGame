from Player import LEFT, RIGHT, UP, DOWN, BLOCK_LEFT, BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT
PLAYER_ONE_POSITION = '1'
PLAYER_TWO_POSITION = '2'

# REWARDS
REWARD_WIN = 100
REWARD_LOSE = -100
REWARD_BORDER = -10
REWARD_NOTHING = -1
REWARD_GET_HIT = -5
REWARD_DIRECT_HIT = 10
REWARD_BLOCKED_HIT = 5


class Environment:
    def __init__(self, text):
        self.__states = {}
        lines = list(map(lambda x: x.strip(), text.strip().split('\n')))
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
            return
        elif action == ATT_RIGHT:
            if opponent.__last_action is not BLOCK_LEFT:
                reward = REWARD_GET_HIT
            return

        if new_state in self.__states:
            state = new_state
        else:
            reward = REWARD_LOSE

        player.lastAction = action
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
