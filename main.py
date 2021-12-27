"""
AI COIN GRABBER GAME

Authors: DA CORTE Julien, D'HARBOULLE Maxime, GOMARI Abdelillah
"""

import arcade
import arcade.utils

from src.environment import Environment
from src.agent import Agent

# from src.game import Game

# Show some more logs
IS_DEBUG = False
SPRITE_SIZE = 64
SCALE = 2

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 35 * SCALE
HEIGHT = 35 * SCALE

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = WIDTH * 22
SCREEN_HEIGHT = HEIGHT * 13
SCREEN_TITLE = "AI PAC-MAN"


COIN_SCALING = 0.5 * SCALE
WALL_SCALING = 1 * SCALE
BOOST_SCALING = 0.6 * SCALE
PLAYER_SCALING = 0.9 * SCALE


# 22 Column - 13 rows - [0] space - [2] Coins - [3] Wall - [4] Boost - [5] Bot one - [6] Bot two
SIMPLE_MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
    [0, 3, 4, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 4, 3, 0],
    [0, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 0],
    [0, 3, 2, 2, 2, 2, 2, 2, 3, 5, 0, 0, 6, 3, 2, 2, 2, 2, 2, 2, 3, 0],
    [0, 3, 2, 3, 2, 3, 3, 2, 3, 3, 0, 0, 3, 3, 2, 3, 3, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 0],
    [0, 3, 4, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 4, 3, 0],
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class Game(arcade.Window):
    def __init__(self, width, height, title, agent):
        super().__init__(width, height, title)
        self.height = height
        # self.start_time = time.time()
        self.__environment = agent.environment
        self.__iteration = 1
        self.scene = arcade.Scene()
        self.__agent = agent
        self.boost_count_up = 0
        self.activate_boost = False
        self.player = None
        self.score = 0
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("Boosts", use_spatial_hash=True)

        self.collect_coin_sound = arcade.load_sound("./resources/sounds/coin-sound.wav")
        self.collect_boost_sound = arcade.load_sound("./resources/sounds/boost-sound.wav")

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        coin_image_source = "./resources/images/coin.png"
        wall_image_source = "./resources/images/wall.png"
        player_image_source = "./resources/images/player.png"
        boost_image_source = "./resources/images/boost.png"
        self.score = 0

        for state in self.__environment.states:
            if self.__environment.get_content(state) == 2:
                coin = arcade.Sprite(coin_image_source, 0.5)
                coin.center_x = (state[1] + 0.5) * SPRITE_SIZE
                coin.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Coins", coin)
            elif self.__environment.get_content(state) == 4:
                boost = arcade.Sprite(boost_image_source, BOOST_SCALING)
                boost.center_x = (state[1] + 0.5) * SPRITE_SIZE
                boost.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Boosts", boost)
            elif self.__environment.get_content(state) == 5:
                self.player = arcade.Sprite(player_image_source, PLAYER_SCALING)
                self.player.center_x = (state[1] + 0.5) * SPRITE_SIZE
                self.player.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Player", self.player)
            elif self.__environment.get_content(state) == 3:
                wall = arcade.Sprite(wall_image_source, WALL_SCALING)
                wall.center_x = (state[1] + 0.5) * SPRITE_SIZE
                wall.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Walls", wall)

    def update_agent(self):
        self.player.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
        self.player.center_y = self.height - (self.__agent.state[0] + 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        score_text = f"Coins: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):
        # boucle d'apprentissage et d'action
        # Mettre une fin

        if self.__agent.state:
            action = self.__agent.best_action()
            reward = self.__agent.do(action)

            coin_hit_list = arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list("Coins"))

            boost_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene.get_sprite_list("Boosts")
            )
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)
                self.score += 1

            for boost in boost_hit_list:
                boost.remove_from_sprite_lists()
                arcade.play_sound(self.collect_boost_sound)
                self.activate_boost = True
                self.boost_count_up = 0

            self.update_agent()


def main():
    environment = Environment(SIMPLE_MAZE)
    agent = Agent(environment)
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
