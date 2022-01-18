from constant import PLAYER_ONE_POSITION, PLAYER_TWO_POSITION, HEAVY_ATT_RIGHT, \
    HEAVY_ATT_LEFT, LEFT, RIGHT, UP, DOWN, BLOCK_LEFT, BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT, WALL, RUN_IN_OPPONENT, \
    REWARD_BORDER, REWARD_DIRECT_HIT, REWARD_RETREAT, REWARD_APPROACH, REWARD_MISS, REWARD_HIT_IN_BLOCK, NOTHING, \
    REWARD_NOTHING, REWARD_DIRECT_HEAVY_HIT, REWARD_BREAK_BLOCK


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

    def rewardForDistance(self, oldDistance, newDistance):
        if abs(oldDistance[0]) < abs(newDistance[0]):
            print("RECULE")
            return REWARD_RETREAT
        if abs(oldDistance[1]) < abs(newDistance[1]):
            print("RECULE")
            return REWARD_RETREAT
        if abs(oldDistance[0]) > abs(newDistance[0]):
            print("AVANCE")
            return REWARD_APPROACH
        if abs(oldDistance[1]) > abs(newDistance[1]):
            print("AVANCE")
            return REWARD_APPROACH

        return 0

    def apply(self, player, opponent, action, distance):
        reward = 0
        new_state = None
        opponent_distance = (-distance[0], -distance[1])

        if player.delay == 1 and (player.lastAction == HEAVY_ATT_LEFT or player.lastAction == HEAVY_ATT_RIGHT):
            player.delay = 0
            if opponent.lastAction is not BLOCK_LEFT and opponent.lastAction is not BLOCK_RIGHT \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_DIRECT_HEAVY_HIT
                opponent.takeHeavyHit(player.lastAction, opponent_distance)
                action = player.lastAction
            elif (opponent.lastAction is BLOCK_LEFT or opponent.lastAction is not BLOCK_RIGHT) \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_BREAK_BLOCK
                opponent.takeHeavyHitOnBlock(player.lastAction, opponent_distance)
                action = player.lastAction
            else:
                action = player.lastAction
                reward = REWARD_MISS
                print("JE RATE")
        elif player.delay == 1:
            player.delay = 0
            action = player.lastAction
            reward = 0
        elif action == NOTHING:
            reward = REWARD_NOTHING
        elif action == LEFT:
            new_state = (player.state[0], player.state[1] - 1)
        elif action == RIGHT:
            new_state = (player.state[0], player.state[1] + 1)
        elif action == UP:
            new_state = (player.state[0] - 1, player.state[1])
        elif action == DOWN:
            new_state = (player.state[0] + 1, player.state[1])

        elif action == ATT_LEFT:
            if opponent.lastAction is not BLOCK_LEFT \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_DIRECT_HIT
                opponent.takeHit(ATT_LEFT, opponent_distance)
            elif opponent.lastAction is BLOCK_LEFT \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_HIT_IN_BLOCK
                opponent.block_hit(ATT_LEFT, opponent_distance)
            else:
                reward = REWARD_MISS


        elif action == ATT_RIGHT:
            if opponent.lastAction is not BLOCK_RIGHT \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_DIRECT_HIT
                opponent.takeHit(ATT_RIGHT, opponent_distance)
            elif opponent.lastAction is BLOCK_RIGHT \
                    and (
                    (player.state[0] is opponent.state[0]
                     and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                    or (player.state[1] is opponent.state[1]
                        and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1))):
                reward = REWARD_HIT_IN_BLOCK
                opponent.block_hit(ATT_RIGHT, opponent_distance)
            else:
                reward = REWARD_MISS
        elif action == HEAVY_ATT_RIGHT:
            player.delay = 1
            reward = 0
        elif action == HEAVY_ATT_LEFT:
            player.delay = 1
            reward = -5
        elif action == BLOCK_RIGHT or action == BLOCK_LEFT:
            player.delay = 1
            player.opponent_action_on_block = opponent.lastAction
            reward = -5

        if new_state is not None and new_state in self.__states:
            print("NOUVELLE POSITION = " + str(new_state))
            print("POSITION ADVERSE = " + str(opponent.state))
            if new_state[0] == opponent.state[0] and new_state[1] == opponent.state[1]:
                reward = RUN_IN_OPPONENT
                print("LES PARAMETRES SONT => " + str(distance) + " " + opponent.lastAction + " " + action + " " + str(
                    reward))
                player.update(distance, opponent.lastAction, action, reward)
                new_state = player.state
            elif self.__states[new_state] == WALL:
                print("JE PREND UN MUR")
                reward = REWARD_BORDER
                print("LA")
                player.update(distance, opponent.lastAction, action, reward)
                new_state = player.state
            else:
                newDistance = self.getDistance(new_state, opponent.state)
                reward = self.rewardForDistance(distance, newDistance)
                print("ICI")
                player.update(distance, opponent.lastAction, action, reward)

            player.setState(new_state)

        else:
            print("LES PARAMETRES SONT => " + str(distance) + " " + opponent.lastAction + " " + action + " " + str(reward))
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

    def getDistance(self, playerState, oponentState):
        return playerState[0] - oponentState[0], playerState[1] - oponentState[1]
