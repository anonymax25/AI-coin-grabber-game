from cmath import log
from random import *
import pickle

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]

FILE_TABLE = 'agent.dat'
FILE_INFORMATION = 'game.dat'

TEMPERATURE_DECAY_FACTOR = 0.99


class Agent:
    def __init__(self, environment):
        self.__environment = environment
        self.__qtable = {}
        self.__learning_rate = 1
        self.__discount_factor = 1
        self.__actions = 0
        self.__last_action = None
        self.__score = 0
        self.__temperature = 1
        self.__coins = 0
        self.__state = environment.player_start
        for s in environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = random() * 10.0

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
        # update q-table
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (reward + self.__discount_factor *
                                                                       maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__last_action = action
        self.__actions += 1
        self.__score += reward

    def best_action(self):
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
        if action != None:
            self.__environment.apply(self, action)

    def reset(self):
        self.__state = self.__environment.player_start
        self.__actions = 0
        self.__last_action = None
        self.__score = 0
        self.__coins = 0
        self.save_table(FILE_TABLE)
        self.__temperature = 1
#         self.save("agent.dat")
        self.environment.start()

    def save_table(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load_table(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)
