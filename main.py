"""
AI COIN GRABBER GAME

Authors: DA CORTE Julien, D'HARBOULLE Maxime, GOMARI Abdelillah
"""
import arcade

from src.environment import Environment
from src.agent import Agent
from src.game import Game


def main():
    environment = Environment()
    agent = Agent(environment)
    window = Game(agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
