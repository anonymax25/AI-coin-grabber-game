import os

import arcade
import pickle

from src.agent import DOWN, LEFT, RIGHT, UP

SPRITE_SIZE = 55

coin_image_source = ":resources:images/items/gemYellow.png"
wall_image_source = ":resources:images/tiles/grassCenter_round.png"
player_image_source = ":resources:images/animated_characters/robot/robot_idle.png"

FILE_INFORMATION = 'game.dat'
FILE_STATS = 'stats.dat'


class Game(arcade.View):
    def __init__(self, agent, manual=False):
        super().__init__()
        self.__manual = manual
        self.__manualAction = None
        self.__agent = agent
        self.__environment = agent.environment
        self.__iteration = 1
        self.player = None
        self.__lastScore = None
        self.__averageScore = None
        self.__highScore = None
        self.__stats = []
        self.window.scene = arcade.Scene()
        self.window.scene.add_sprite_list("Player")
        self.window.scene.add_sprite_list("Walls")
        self.window.scene.add_sprite_list("Coins")
        self.collect_coin_sound = arcade.load_sound("./assets/sounds/coin-sound.wav")

    def setup(self):
        for state in self.__environment.states:
            if self.__environment.get_content(state) == 2:
                coin = arcade.Sprite(coin_image_source, 0.5)
                coin.center_x = (state[1] + 0.5) * SPRITE_SIZE
                coin.center_y = self.window.height - (state[0] + 0.5) * SPRITE_SIZE
                self.window.scene.add_sprite("Coins", coin)
            elif self.__environment.get_content(state) == 5:
                self.player = arcade.Sprite(player_image_source, 0.5)
                self.player.center_x = (state[1] + 0.5) * SPRITE_SIZE
                self.player.center_y = self.window.height - (state[0] + 0.5) * 64
                self.window.scene.add_sprite("Player", self.player)
            elif self.__environment.get_content(state) == 3:
                wall = arcade.Sprite(wall_image_source, 0.5)
                wall.center_x = (state[1] + 0.5) * SPRITE_SIZE
                wall.center_y = self.window.height - (state[0] + 0.5) * SPRITE_SIZE
                self.window.scene.add_sprite("Walls", wall)

        arcade.set_background_color(arcade.color.MIDNIGHT_GREEN)

    def update_agent(self):
        self.player.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
        self.player.center_y = self.window.height - (self.__agent.state[0] + 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        score_text = f"Score: {self.__agent.score}"
        coins_text = f"Nombres de gèmes: {self.__agent.coins}"
        move_text = f"Movements: {self.__agent.actions}"
        iteration_text = f"Nombres d'iterations: {self.__iteration}"

        self.window.scene.draw()
        arcade.draw_text(coins_text, 10, 10, arcade.csscolor.WHITE, 15)
        arcade.draw_text(iteration_text, 10, 30, arcade.csscolor.WHITE, 15)
        arcade.draw_text(move_text, 10, 50, arcade.csscolor.WHITE, 15)
        arcade.draw_text(score_text, 10, 70, arcade.csscolor.WHITE, 15)

        last_score_text = f"Last Score: {'None' if self.__lastScore is None else self.__lastScore}"
        high_score_text = f"High Score: {'None' if self.__highScore is None else self.__highScore}"
        avg_score_text = f"Avg Score: {'None' if self.__averageScore is None else format(self.__averageScore, '.2f')}"
        temperature_score_text = f"Temperature: {'None' if self.__agent is None else format(self.__agent.temperature, '.2f')}"

        arcade.draw_text(last_score_text, 300, 10, arcade.csscolor.WHITE, 15)
        arcade.draw_text(high_score_text, 300, 30, arcade.csscolor.WHITE, 15)
        arcade.draw_text(avg_score_text, 300, 50, arcade.csscolor.WHITE, 15)
        arcade.draw_text(temperature_score_text, 300, 70, arcade.csscolor.WHITE, 15)

        arcade.draw_text(
            "Mode: manual" if self.__manual else "Mode: AI",
            start_x=self.window.width - 300,
            start_y=50,
            color=arcade.color.LIGHT_GRAY,
            font_size=20,
            bold=True
        )

        arcade.draw_text(
            "Esc to go to menu",
            start_x=self.window.width - 300,
            start_y=20,
            color=arcade.color.LIGHT_GRAY,
            font_size=20,
            bold=True
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from src.menu import Menu
            menu_view = Menu()
            self.window.show_view(menu_view)
        if key == arcade.key.R:
            self.reset()
            self.__iteration += 1
        if self.__manual is True:
            if key == arcade.key.UP:
                self.__manualAction = UP
            elif key == arcade.key.DOWN:
                self.__manualAction = DOWN
            elif key == arcade.key.LEFT:
                self.__manualAction = LEFT
            elif key == arcade.key.RIGHT:
                self.__manualAction = RIGHT

    def on_update(self, delta_time):
        if self.__agent.coins < self.__agent.environment.goal:
            coin_hit_list = arcade.check_for_collision_with_list(self.player,
                                                                 self.window.scene.get_sprite_list("Coins"))
            if self.__manual:
                action = self.__manualAction
            else:
                action = self.__agent.best_action()

            self.__agent.do(action)
            self.__manualAction = None

            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.__agent.add_coin(1)

            self.update_agent()
        else:
            self.__lastScore = self.__agent.score

            if self.__highScore is None or self.__highScore < self.__agent.score:
                self.__highScore = self.__agent.score

            if self.__averageScore is None:
                self.__averageScore = self.__agent.score
            else:
                self.__averageScore += (self.__agent.score - self.__averageScore) / self.__iteration

            self.reset()
            self.__iteration += 1
            for state in self.__environment.states:
                if self.__environment.get_content(state) == 2:
                    coin = arcade.Sprite(coin_image_source, 0.5)
                    coin.center_x = (state[1] + 0.5) * SPRITE_SIZE
                    coin.center_y = self.window.height - (state[0] + 0.5) * SPRITE_SIZE
                    self.window.scene.add_sprite("Coins", coin)

    def save_information(self, filename):
        information = (self.__iteration, self.__averageScore, self.__lastScore, self.__highScore)
        with open(filename, 'wb') as file:
            pickle.dump(information, file)

    def load_information(self, filename):
        with open(filename, 'rb') as file:
            self.__iteration, self.__averageScore, self.__lastScore, self.__highScore = pickle.load(file)

    @property
    def stats(self):
        return self.__stats

    def save_stats(self, filename):
        if os.path.exists(FILE_STATS):
            self.load_stats(filename)
        self.__stats.append(self.__lastScore)
        with open(filename, 'wb') as file:
            pickle.dump(self.__stats, file)

    def load_stats(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.__stats = pickle.load(file)
        except EOFError:
            self.__stats = []

    def reset(self):
        self.__agent.reset()
        self.save_information(FILE_INFORMATION)
        self.save_stats(FILE_STATS)
