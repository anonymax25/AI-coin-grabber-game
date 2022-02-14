import arcade
import arcade.gui
import os

from src.agent import Agent
from src.environment import Environment
from src.game import Game
from src.graph import Graph

FILE_TABLE = 'agent.dat'
FILE_INFORMATION = 'game.dat'
FILE_STATS = 'stats.dat'


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.MIDNIGHT_GREEN)

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="coin grabber", font_size=32, font_name="Kenney Future",
                                              text_color=arcade.color.AMBER)
        self.v_box.add(ui_text_label.with_space_around(bottom=50))

        start_button = arcade.gui.UIFlatButton(text="Play", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        start_ia_button = arcade.gui.UIFlatButton(text="IA Mode", width=200)
        self.v_box.add(start_ia_button.with_space_around(bottom=20))

        reset_button = arcade.gui.UIFlatButton(text="Reset IA Data", width=200)
        self.v_box.add(reset_button.with_space_around(bottom=20))

        stats_button = arcade.gui.UIFlatButton(text="Stats", width=200)
        self.v_box.add(stats_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start
        start_ia_button.on_click = self.on_click_start_ia
        reset_button.on_click = self.on_click_reset_data
        stats_button.on_click = self.on_click_plot_stats
        quit_button.on_click = self.on_click_quit

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_click_start(self, event):
        environment = Environment()
        agent = Agent(environment)
        game_view = Game(agent, manual=True)
        self.window.show_view(game_view)
        game_view.setup()

    def on_click_start_ia(self, event):
        environment = Environment()
        agent = Agent(environment)
        if os.path.exists(FILE_TABLE):
            agent.load_table(FILE_TABLE)
        game_view = Game(agent, manual=False)
        if os.path.exists(FILE_INFORMATION):
            game_view.load_information(FILE_INFORMATION)
        self.window.show_view(game_view)
        game_view.setup()

    def on_click_reset_data(self, event):
        if os.path.exists(FILE_TABLE):
            os.remove(FILE_TABLE)
        if os.path.exists(FILE_INFORMATION):
            os.remove(FILE_INFORMATION)
        if os.path.exists(FILE_STATS):
            os.remove(FILE_STATS)

    def on_click_quit(self, event):
        arcade.exit()

    def on_click_plot_stats(self, event):
        environment = Environment()
        agent = Agent(environment)
        game_view = Game(agent, manual=False)
        if os.path.exists(FILE_STATS):
            game_view.load_stats(FILE_STATS)
        graph_view = Graph([*range(0, len(game_view.stats), 1)], game_view.stats)
        self.window.show_view(graph_view)

    def on_draw(self) -> None:
        arcade.start_render()
        self.manager.draw()
