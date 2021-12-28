UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
GOAL = 97

# Set rewards
REWARD_BORDER = -100
REWARD_EMPTY = -2
REWARD_GOAL = 10
REWARD_COIN = 5

# Set how many rows and columns we will have
ROW_COUNT = 12
COLUMN_COUNT = 20

# 22 Column - 12 rows - [0] space - [2] Coins - [3] Wall - [4] Boost - [5] Bot one - [6] Bot two
MAZE = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 4, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 4, 3],
    [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
    [3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3],
    [3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 3, 5, 0, 0, 6, 3, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 2, 3, 3, 2, 3, 3, 0, 0, 3, 3, 2, 3, 3, 2, 3, 2, 3],
    [3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3],
    [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
    [3, 4, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 4, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class Environment:
    def __init__(self):
        self.__states = {}
        self.__goal = GOAL
        self.width = COLUMN_COUNT
        self.height = ROW_COUNT

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                self.__states[(row, column)] = MAZE[row][column]
                if MAZE[row][column] == 5:
                    self.__start = (row, column)

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

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

        if new_state in self.__states:
            if self.__states[new_state] == 3:
                reward = REWARD_BORDER
            elif self.__states[new_state] in [2, 4]:
                reward = REWARD_COIN
                self.__states[new_state] = 0
            else:
                reward = REWARD_EMPTY

        agent.update(action, new_state, reward)
