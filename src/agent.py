from random import *

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]


class Agent:
    def __init__(self, environment):
        self.__environment = environment
        self.__qtable = {}
        self.__learning_rate = 1
        self.__discount_factor = 1
        self.__last_action = None
        self.__state = environment.start
        for s in environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = random() * 10.0

    @property
    def state(self):
        return self.__state

    @property
    def last_action(self):
        return self.__last_action

    @property
    def qtable(self):
        return self.__qtable

    @property
    def environment(self):
        return self.__environment

    def update(self, action, state, reward):
        # update q-table
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (reward + self.__discount_factor *
                                                                       maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__last_action = action

    def best_action(self):
        rewards = self.__qtable[self.__state]
        best = None
        for a in rewards:
            if best is None or rewards[a] > rewards[best]:
                best = a
        return best

    def do(self, action):
        self.__environment.apply(self, action)

    # def save(self, filename):
    #     with open(filename, 'wb') as file:
    #         pickle.dump(self.__qtable, file)

    # def load(self, filename):
    #     with open(filename, 'rb') as file:
    #         self.__qtable = pickle.load(file)