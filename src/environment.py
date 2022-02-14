from pickle import FALSE


UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
GOAL = 100

# Set rewards
REWARD_BORDER = -20
REWARD_EMPTY = -3
REWARD_COIN = 10

# Set how many rows and columns we will have
ROW_COUNT = 11
COLUMN_COUNT = 20

# 22 Column - 12 rows - [0] space - [2] Coins - [3] Wall - [4] Boost - [5] Bot one - [6] Bot two
MAZE = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
    [3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3],
    [3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 3, 5, 0, 0, 6, 3, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 2, 3, 3, 2, 3, 3, 0, 0, 3, 3, 2, 3, 3, 2, 3, 2, 3],
    [3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3],
    [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

# MAZE = [
#     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#     [3, 3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#     [3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#     [3, 2, 2, 2, 2, 2, 2, 3, 5, 0, 0, 6, 3, 3, 2, 2, 2, 2, 2, 3],
#     [3, 2, 3, 2, 3, 3, 2, 3, 3, 0, 0, 3, 3, 2, 3, 3, 2, 3, 2, 3],
#     [3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3],
#     [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
#     [3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3],
#     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
# ]

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
                    self.__player_start = (row, column, False)

    @property
    def goal(self):
        return self.__goal

    @property
    def player_start(self):
        return self.__player_start

    @property
    def states(self):
        return self.__states

    def get_content(self, state):
        return self.__states[state]

    def start(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                self.__states[(row, column)] = MAZE[row][column]

    def apply(self, agent, action):
        state = (agent.state[0], agent.state[1])
        new_state = None
        reward = None

        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)

        is_gem = False
        if new_state in self.__states:
            if self.__states[new_state] == 3:
                reward = REWARD_BORDER
                new_state = state
            elif self.__states[new_state] == 2:
                reward = REWARD_COIN
                is_gem = True
                self.__states[new_state] = 0
            else:
                reward = REWARD_EMPTY
        new_state += (is_gem,)
        
        agent.update(action, new_state, reward)
