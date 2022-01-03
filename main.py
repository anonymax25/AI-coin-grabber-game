"""
AI COIN GRABBER GAME

Authors: DA CORTE Julien, D'HARBOULLE Maxime, GOMARI Abdelillah
"""
import arcade

from src.environment import Environment
from src.agent import Agent
from src.game import Game
from src.menu import Menu


def main():
    window = arcade.Window(1100, 700, "Game")
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
