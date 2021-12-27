UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

# Set rewards
REWARD_BORDER = -10
REWARD_EMPTY = -2
REWARD_GOAL = 10
REWARD_COIN = 5

# Set how many rows and columns we will have
ROW_COUNT = 13
COLUMN_COUNT = 22


class Environment:
    def __init__(self, grid):
        self.__states = {}
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                self.__states[(row, column)] = grid[row][column]
                if grid[row][column] == 5:
                    self.__start = (row, column)

    @property
    def start(self):
        return self.__start

    @property
    def states(self):
        return self.__states.keys()

    def get_content(self, state):
        return self.__states[state]

    def apply(self, agent, action):
        state = agent.state
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)

        # Calculer la récompense pour l'agent et la lui transmettre
        if new_state in self.__states:
            if self.__states[new_state] == 3:
                reward = REWARD_BORDER
            elif self.__states[new_state] == 2:
                reward = REWARD_COIN
                self.__states[new_state] = 0
            else:
                reward = REWARD_EMPTY
            state = new_state

        agent.update(action, state, reward)
        return reward

