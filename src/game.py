import arcade

SPRITE_SIZE = 55
SCREEN_TITLE = "AI PAC-MAN"


class Game(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * SPRITE_SIZE, agent.environment.height * SPRITE_SIZE, SCREEN_TITLE)
        self.__agent = agent
        self.__environment = agent.environment
        self.__iteration = 1
        self.player = None
        self.score = 0
        self.boost_count_up = 0
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Boosts")
        self.collect_coin_sound = arcade.load_sound("./assets/sounds/coin-sound.wav")
        self.collect_boost_sound = arcade.load_sound("./assets/sounds/boost-sound.wav")

    def setup(self):
        coin_image_source = ":resources:images/items/gemYellow.png"
        boost_image_source = ":resources:images/items/gemBlue.png"
        wall_image_source = ":resources:images/tiles/grassCenter_round.png"
        player_image_source = ":resources:images/animated_characters/robot/robot_idle.png"

        for state in self.__environment.states:
            if self.__environment.get_content(state) == 2:
                coin = arcade.Sprite(coin_image_source, 0.5)
                coin.center_x = (state[1] + 0.5) * SPRITE_SIZE
                coin.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Coins", coin)
            elif self.__environment.get_content(state) == 4:
                boost = arcade.Sprite(boost_image_source, 0.5)
                boost.center_x = (state[1] + 0.5) * SPRITE_SIZE
                boost.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Boosts", boost)
            elif self.__environment.get_content(state) == 5:
                self.player = arcade.Sprite(player_image_source, 0.5)
                self.player.center_x = (state[1] + 0.5) * SPRITE_SIZE
                self.player.center_y = self.height - (state[0] + 0.5) * 64
                self.scene.add_sprite("Player", self.player)
            elif self.__environment.get_content(state) == 3:
                wall = arcade.Sprite(wall_image_source, 0.5)
                wall.center_x = (state[1] + 0.5) * SPRITE_SIZE
                wall.center_y = self.height - (state[0] + 0.5) * SPRITE_SIZE
                self.scene.add_sprite("Walls", wall)

        arcade.set_background_color(arcade.color.MIDNIGHT_GREEN)

    def update_agent(self):
        self.player.center_x = (self.__agent.state[1] + 0.5) * SPRITE_SIZE
        self.player.center_y = self.height - (self.__agent.state[0] + 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        score_text = f"Coins: {self.score}"
        # move_text = f"Movement:"
        # iteration_text = f"Iterations:"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):
        if self.score != self.__agent.environment.goal:
            coin_hit_list = arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list("Coins"))
            boost_hit_list = arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list("Boosts"))
            action = self.__agent.best_action()
            self.__agent.do(action)

            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                # arcade.play_sound(self.collect_coin_sound)
                self.score += 1

            for boost in boost_hit_list:
                boost.remove_from_sprite_lists()
                arcade.play_sound(self.collect_boost_sound)
                self.boost_count_up = 0
            self.update_agent()
