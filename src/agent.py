import pickle
from random import *

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]

FILE_TABLE = 'agent.dat'

TEMPERATURE_DECAY_FACTOR = 0.99


class Agent:
    def __init__(self, environment):
        self.__environment = environment
        self.__qtable = {}
        self.__learning_rate = 0.5
        self.__discount_factor = 0.5
        self.__actions = 0
        self.__last_action = None
        self.__score = 0
        self.__temperature = 1
        self.__coins = 0
        self.__state = environment.player_start
        for s in environment.states:
            self.__qtable[(s[0], s[1], True)] = {}
            self.__qtable[(s[0], s[1], False)] = {}
            for a in ACTIONS:
                self.__qtable[(s[0], s[1], True)][a] = 0.5 
                self.__qtable[(s[0], s[1], False)][a] = 0.5

    @property
    def state(self):
        return self.__state

    @property
    def actions(self):
        return self.__actions

    @property
    def score(self):
        return self.__score

    @property
    def coins(self):
        return self.__coins

    @property
    def qtable(self):
        return self.__qtable

    @property
    def environment(self):
        return self.__environment

    @property
    def temperature(self):
        return self.__temperature

    def add_coin(self, coin):
        self.__coins += coin

    def update(self, action, state, reward):
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (reward + self.__discount_factor * maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__last_action = action
        self.__actions += 1
        self.__score += reward

    def best_action(self):
        has_gemes = []
        
        if self.__state[0] + 1 >= 0 and self.__state[0] + 1 <= self.environment.width and self.__state[1] >= 0 and self.__state[1] <= self.environment.height and self.environment.states[(self.__state[0] + 1, self.__state[1])] is 2:
            has_gemes.append(DOWN)
        if self.__state[0] - 1 >= 0 and self.__state[0] - 1 <= self.environment.width and self.__state[1] >= 0 and self.__state[1] <= self.environment.height and self.environment.states[(self.__state[0] - 1, self.__state[1])] is 2:
            has_gemes.append(UP)
        if self.__state[0] >= 0 and self.__state[0] <= self.environment.width and self.__state[1] + 1 >= 0 and self.__state[1] + 1 <= self.environment.height and self.environment.states[(self.__state[0], self.__state[1] + 1)] is 2:
            has_gemes.append(RIGHT)
        if self.__state[0] >= 0 and self.__state[0] <= self.environment.width and self.__state[1] - 1 >= 0 and self.__state[1] - 1 <= self.environment.height and self.environment.states[(self.__state[0], self.__state[1] - 1)] is 2:
            has_gemes.append(LEFT)

        if len(has_gemes) > 0:
            rewards = self.__qtable[(self.__state[0], self.__state[1], True)]
            best = None
            for adjacent in has_gemes:
                if best is None or rewards[adjacent] > rewards[best]:
                    best = adjacent
            return best
        else:
            rewards = self.__qtable[(self.__state[0], self.__state[1], False)]
            self.__temperature = self.__temperature * TEMPERATURE_DECAY_FACTOR
            if random() < self.__temperature:
                return choice(ACTIONS)
            rewards = self.__qtable[self.__state]
            best = None
            for a in rewards:
                if best is None or rewards[a] > rewards[best]:
                    best = a
            return best

    def do(self, action):
        if action is not None:
            self.__environment.apply(self, action)

    def reset(self):
        self.__state = self.__environment.player_start
        self.__actions = 0
        self.__last_action = None
        self.__score = 0
        self.__coins = 0
        self.save_table(FILE_TABLE)
        self.__temperature = 1
        self.environment.start()

    def save_table(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load_table(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)
