from Player import LEFT, RIGHT, ATT_UP, DEF_UP, ATT_MID, DEF_MID, ATT_DOWN, DEF_DOWN

PLAYER_ONE_POSITION = '1'
PLAYER_TWO_POSITION = '2'


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
