from constant import PLAYER_ONE_POSITION, PLAYER_TWO_POSITION, HEAVY_ATT_RIGHT, \
    HEAVY_ATT_LEFT, LEFT, RIGHT, UP, DOWN, BLOCK_LEFT, BLOCK_RIGHT, ATT_LEFT, ATT_RIGHT, WALL, RUN_IN_OPPONENT, \
    REWARD_BORDER, REWARD_DIRECT_HIT, REWARD_MISS, REWARD_HIT_IN_BLOCK, NOTHING, \
    REWARD_NOTHING, REWARD_DIRECT_HEAVY_HIT, REWARD_BREAK_BLOCK, REWARD_MOVE, REWARD_INTERRUPT


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

        if player.delay > 0:
            self.applyWithDelay(player,opponent, distance)
            return
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

        elif action == HEAVY_ATT_RIGHT:
            player.delay = 2
            player.opponent_action_on_delay = opponent.lastAction
            player.distance_on_delay = distance
            player.opponent_delay_on_delay = opponent.delay
            reward = 0
        elif action == HEAVY_ATT_LEFT:
            player.delay = 2
            player.opponent_action_on_delay = opponent.lastAction
            player.distance_on_delay = distance
            player.opponent_delay_on_delay = opponent.delay
            reward = 0
        elif action == ATT_RIGHT or action == ATT_LEFT:
            player.delay = 1
            player.opponent_action_on_delay = opponent.lastAction
            player.distance_on_delay = distance
            print("J'enregistre le delai de ladversaire = " + str(opponent.delay))
            player.opponent_delay_on_delay = opponent.delay
            reward = 0
        elif action == BLOCK_RIGHT or action == BLOCK_LEFT:
            player.delay = 1
            player.opponent_action_on_delay = opponent.lastAction
            player.distance_on_delay = distance
            player.opponent_delay_on_delay = opponent.delay
            print("JE PREPARE LE BLOCK LORSQUE " + opponent.lastAction + " " + str(opponent.delay) + " " + str(distance))
            print(player.qtable[distance][opponent.lastAction][opponent.delay])
            reward = -5

        if new_state is not None and new_state in self.__states:
            if new_state[0] == opponent.state[0] and new_state[1] == opponent.state[1]:
                reward = RUN_IN_OPPONENT

                player.update(distance, opponent.lastAction, action, reward, opponent.delay)
                new_state = player.state
            elif self.__states[new_state] == WALL:
                reward = REWARD_BORDER
                player.update(distance, opponent.lastAction, action, reward, opponent.delay)
                new_state = player.state
            else:
                reward = REWARD_MOVE
                player.update(distance, opponent.lastAction, action, reward, opponent.delay)

            player.setState(new_state)

        else:
            player.update(distance, opponent.lastAction, action, reward, opponent.delay)

        player.setLastAction(action)

    def applyWithDelay(self, player, opponent, distance):
        opponent_distance = (-distance[0], -distance[1])
        player.delay -= 1

        initialAction = player.lastAction
        opponentAction = player.opponent_action_on_delay
        distanceOnAction = player.distance_on_delay
        opponentDelay = player.opponent_delay_on_delay
        action = player.lastAction
        reward = 0

        if player.delay == 0:
            if player.prepareHeavyAttack():
                if opponent.isNotBlocking() and self.opponentIsTouchable(player, opponent):
                    reward = REWARD_DIRECT_HEAVY_HIT
                    print("JE METS UN GROS COUP")
                    opponent.takeHeavyHit(player.lastAction, opponent_distance)
                elif opponent.isBlocking() and self.opponentIsTouchable(player, opponent):
                    reward = REWARD_BREAK_BLOCK
                    opponent.takeHeavyHitOnBlock(player.lastAction, opponent_distance)
                else:
                    reward = REWARD_MISS
            elif player.prepareSimpleAttack():
                if opponent.isNotBlocking() and self.opponentIsTouchable(player, opponent):
                    if opponent.prepareHeavyAttack() and opponent.delay >= 1 and self.opponentIsTouchable(player, opponent):
                        opponent.cancelPlayerAttack()
                        reward = REWARD_INTERRUPT
                    else:
                        reward = REWARD_DIRECT_HIT
                        opponent.takeHit(player.lastAction, opponent_distance)

                elif opponent.isBlocking() and self.opponentIsTouchable(player, opponent):
                    reward = REWARD_HIT_IN_BLOCK
                    opponent.block_hit(player.lastAction, opponent_distance)
                    player.attack_on_block()
                    action = NOTHING
                else:
                    reward = REWARD_MISS

            if initialAction != BLOCK_LEFT and initialAction != BLOCK_RIGHT and initialAction != NOTHING:
                #print("UPDATE DE " + initialAction + " DISTANCE : " + str(distanceOnAction) + "SUR LACTION : " + opponentAction + "avec un delay de " + str(opponentDelay))
                player.update(distanceOnAction, opponentAction, initialAction, reward, opponentDelay)

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

    def opponentIsTouchable(self, player, opponent):
        return (
                (player.state[0] is opponent.state[0]
                 and (player.state[1] == opponent.state[1] + 1 or player.state[1] == opponent.state[1] - 1))
                or (player.state[1] is opponent.state[1]
                    and (player.state[0] == opponent.state[0] + 1 or player.state[0] == opponent.state[0] - 1)))
