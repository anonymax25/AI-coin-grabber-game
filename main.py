"""
AI COIN GRABBER GAME

Authors: DA CORTE Julien, D'HARBOULLE Maxime, GOMARI Abdelillah
"""
import arcade
import arcade.utils
import time

#Ticks per second of the game mouvement 
TPS = 2
BOOST_TPS_SCALE = 2
BOOST_TIME = 4
ANIMATION_DETAIL_LEVEL = 10

# Set how many rows and columns we will have
ROW_COUNT = 13
COLUMN_COUNT = 22

SCALE = 1
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 35 * SCALE
HEIGHT = 35 * SCALE

COIN_SCALING = 0.5 * SCALE
WALL_SCALING = 1 * SCALE
BOOST_SCALING = 0.7 * SCALE
PLAYER_SCALING = 0.9 * SCALE

CHARACTER_SCALING = 1 * SCALE
TILE_SCALING = 0.5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = HEIGHT * ROW_COUNT
SCREEN_TITLE = "AI PAC-MAN"

# 22 Column - 13 rows - [0] space - [2] Coins - [3] Wall - [4] Ghost safe-space - [5] Boost
SIMPLE_MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
    [0, 3, 5, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 5, 3, 0],
    [0, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 0],
    [0, 3, 6, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 3, 2, 2, 2, 2, 2, 2, 3, 0],
    [0, 3, 2, 3, 2, 3, 3, 2, 3, 3, 4, 4, 3, 3, 2, 3, 3, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 0],
    [0, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 0],
    [0, 3, 5, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 5, 3, 0],
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 28 Column - 31 rows - [1] Empty Space - [2] Coins - [3] Wall - [4] Ghost safe-space - [5] Boost
MAZE = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 5, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 5, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
    [3, 5, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 5, 3],
    [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
    [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
    [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = SIMPLE_MAZE
        self.scene = None
        self.player_sprite = None
        self.boost_count_up = 0
        self.activate_boost = False
        self.player_list = None
        self.gui_camera = None
        self.score = 0

        self.collect_coin_sound = arcade.load_sound("./resources/sounds/coin-sound.wav")
        self.collect_boost_sound = arcade.load_sound("./resources/sounds/boost-sound.wav")

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.score = 0

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Ghosts")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("Boosts", use_spatial_hash=True)

        coin_image_source = "./resources/images/coin.png"
        wall_image_source = "./resources/images/wall.png"
        player_image_source = "./resources/images/player.png"
        boost_image_source = "./resources/images/boost.png"

        

        self.mouvement_queue = []

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = WIDTH * column + WIDTH // 2
                y = HEIGHT * row + HEIGHT // 2

                if self.grid[row][column] == 2:
                    coin = arcade.Sprite(coin_image_source, COIN_SCALING)
                    coin.center_x = x
                    coin.center_y = y
                    self.scene.add_sprite("Coins", coin)
                elif self.grid[row][column] == 5:
                    boost = arcade.Sprite(boost_image_source, BOOST_SCALING)
                    boost.center_x = x
                    boost.center_y = y
                    self.scene.add_sprite("Boosts", boost)
                elif self.grid[row][column] == 6:
                    if(self.player_sprite):
                        continue
                    self.player_sprite = arcade.Sprite(player_image_source, PLAYER_SCALING)
                    self.player_sprite.center_x = x #5* WIDTH + WIDTH/2 - 2
                    self.player_sprite.center_y = y #6* HEIGHT + HEIGHT/2
                    self.scene.add_sprite("Player", self.player_sprite)
                elif self.grid[row][column] == 3:
                    wall = arcade.Sprite(wall_image_source, WALL_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.scene.add_sprite("Walls", wall)
                else:
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, arcade.color.BLACK)

        self.start_time = time.time()
        self.ellapsed_time = 0
        self.last_action = 0
        self.requested_action = "none"
        self.player_sprite.is_moving= False
        self.player_sprite.moving_to_x = 0
        self.player_sprite.moving_to_y = 0


    def on_draw(self):
        arcade.start_render()

        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Coins: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            20,
        )
        
        arcade.draw_text(
            str(int(self.ellapsed_time)) + "s",
            SCREEN_WIDTH-100,
            10,
            arcade.csscolor.WHITE,
            20,
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.mouvement_queue.insert(0, "up")
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.mouvement_queue.insert(0, "down")
        if key == arcade.key.LEFT or key == arcade.key.Q:
            self.mouvement_queue.insert(0, "left")
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.mouvement_queue.insert(0, "right")
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.mouvement_queue = [a for a in self.mouvement_queue if a != "up"]
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.mouvement_queue = [a for a in self.mouvement_queue if a != "down"]
        if key == arcade.key.LEFT or key == arcade.key.Q:
            self.mouvement_queue = [a for a in self.mouvement_queue if a != "left"]
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.mouvement_queue = [a for a in self.mouvement_queue if a != "right"]

    def move(self, x, y):
        for wall in self.scene.get_sprite_list("Walls"):
            if(wall.collides_with_point((x,y))):
                return
        self.player_sprite.moving_to_x = x
        self.player_sprite.moving_to_y = y
        
        # ease in mouvement
        self.player_sprite.center_x = self.player_sprite.center_x - ((self.player_sprite.center_x - x) / ANIMATION_DETAIL_LEVEL * TPS * (BOOST_TPS_SCALE if self.activate_boost else 1))
        self.player_sprite.center_y = self.player_sprite.center_y - ((self.player_sprite.center_y - y) / ANIMATION_DETAIL_LEVEL * TPS * (BOOST_TPS_SCALE if self.activate_boost else 1)) 
        
        if abs(self.player_sprite.center_y - y) < 1 and abs(self.player_sprite.center_x - x) < 1:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y
            self.player_sprite.is_moving= False        

    def apply_action(self):
        if self.action != "none":
            print(self.action)
        if self.action == "up":
            self.player_sprite.is_moving= True
            self.move(self.player_sprite.center_x, self.player_sprite.center_y + HEIGHT)
        elif self.action == "down":
            self.player_sprite.is_moving= True
            self.move(self.player_sprite.center_x, self.player_sprite.center_y - HEIGHT)
        elif self.action == "left":
            self.player_sprite.is_moving= True
            self.move(self.player_sprite.center_x - WIDTH, self.player_sprite.center_y)
        elif self.action == "right":
            self.player_sprite.is_moving= True
            self.move(self.player_sprite.center_x + WIDTH, self.player_sprite.center_y)

    def on_update(self, delta_time):
        self.ellapsed_time = time.time() - self.start_time
        self.action = self.mouvement_queue[0] if len(self.mouvement_queue) > 0 else "none"
        if self.player_sprite.is_moving:
            self.move(self.player_sprite.moving_to_x, self.player_sprite.moving_to_y)
        elif(self.ellapsed_time > self.last_action + 1 / (TPS * (BOOST_TPS_SCALE if self.activate_boost else 1))):
            self.last_action = self.ellapsed_time
            self.apply_action()
            self.action = "none"

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Coins")
        )

        boost_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Boosts")
        )

        if self.boost_count_up > BOOST_TIME:
            self.activate_boost = False
            

        if self.activate_boost:
            self.boost_count_up += delta_time

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        for boost in boost_hit_list:
            boost.remove_from_sprite_lists()
            arcade.play_sound(self.collect_boost_sound)
            self.activate_boost = True
            self.boost_count_up = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
