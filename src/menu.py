import arcade
from src.agent import Agent
from src.environment import Environment

from src.game import Game

class Menu(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        background_img_path = "assets/images/menu_wallpaper.jpg"
        self.background = arcade.load_texture(background_img_path)

        arcade.set_background_color(arcade.color.MIDNIGHT_GREEN)
    
    def on_draw(self) -> None:
        arcade.start_render()

        # arcade.draw_lrwh_rectangle_textured(
        #     0,0,
        #     self.window.width, self.window.height,
        #     self.background,
        # )

        arcade.draw_text(
            "Main menu",
            start_x=self.window.width // 2 - 350,
            start_y=self.window.height // 2 + self.window.height // 4,
            color=arcade.color.DARK_CYAN,
            font_size=80,
            bold=True
        )

        arcade.draw_rectangle_filled(
            center_x=self.window.width // 2,
            center_y=self.window.height // 3 + 20,
            width=self.window.width // 1.4,
            height=self.window.height // 3,
            color=(200,200,200,20),
        )
    
        arcade.draw_text(
            "Esc to quit app",
            start_x=self.window.width - 250,
            start_y=30,
            color=arcade.color.LIGHT_GRAY,
            font_size=20,
            bold=True
        )

        arcade.draw_text(
            "Press M for manual mode",
            start_x=self.window.width // 2 - 375,
            start_y=self.window.height // 3 + 50,
            color=arcade.color.DARK_CYAN,
            font_size=40,
            bold=True
        )
        arcade.draw_text(
            "Press A for IA mode",
            start_x=self.window.width // 2 - 300,
            start_y=self.window.height // 4,
            color=arcade.color.DARK_CYAN,
            font_size=40,
            bold=True
        )
            
        
    
    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.A:
            environment = Environment()
            agent = Agent(environment)
            game_view = Game(agent, manual=False)
            self.window.show_view(game_view)
            game_view.setup()
        elif key == arcade.key.M:
            environment = Environment()
            agent = Agent(environment)
            game_view = Game(agent, manual=True)
            self.window.show_view(game_view)
            game_view.setup() 
        elif key == arcade.key.ESCAPE:
            self.window.close()