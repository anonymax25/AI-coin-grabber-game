"""
AI COIN GRABBER GAME

Authors: DA CORTE Julien, D'HARBOULLE Maxime, GOMARI Abdelillah
"""
import arcade
from arcade.sound import play_sound
import arcade.utils
import time
import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return not self.elements
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()


# show some more logs
IS_DEBUG = False

#Ticks per second of the game mouvement 
TPS = 3
BOOST_TPS_SCALE = 2
BOOST_TIME = 4
ANIMATION_DETAIL_LEVEL = 10

# Set how many rows and columns we will have
ROW_COUNT = 13
COLUMN_COUNT = 22

SCALE = 2
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
    [0, 3, 2, 3, 2, 3, 3, 2, 3, 3, 7, 4, 3, 3, 2, 3, 3, 2, 3, 2, 3, 0],
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
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_sprite.is_moving = False
                    self.player_sprite.moving_to_x = 0
                    self.player_sprite.moving_to_y = 0
                    self.player_sprite.action = "none"
                    self.player_sprite.mouvement_queue = []
                    self.scene.add_sprite("Player", self.player_sprite)
                elif self.grid[row][column] == 7:
                    self.ghost_sprite = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", PLAYER_SCALING/3)
                    self.ghost_sprite.center_x = x
                    self.ghost_sprite.center_y = y
                    self.ghost_sprite.grid = [ [0] * (COLUMN_COUNT-2) for _ in range((ROW_COUNT-2))]
                    self.ghost_sprite.known_cells = [ [False] * (COLUMN_COUNT-2) for _ in range((ROW_COUNT-2))]
                    self.ghost_sprite.x = column
                    self.ghost_sprite.y = row
                    self.ghost_sprite.known_cells[row][column] = True
                    self.ghost_sprite.is_moving = False
                    self.ghost_sprite.moving_to_x = 0
                    self.ghost_sprite.moving_to_y = 0
                    self.scene.add_sprite("Ghost", self.ghost_sprite)
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
        

        print(self.ghost_sprite.grid)
        print(self.ghost_sprite.known_cells)
        print(self.ghost_sprite.x)
        print(self.ghost_sprite.y)



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

        # arcade.draw_circle_outline(self.ghost_sprite.center_x, self.ghost_sprite.center_y, 20, arcade.color.GREEN)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.player_sprite.mouvement_queue.insert(0, "up")
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.mouvement_queue.insert(0, "down")
        if key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.mouvement_queue.insert(0, "left")
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.mouvement_queue.insert(0, "right")
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.player_sprite.mouvement_queue = [a for a in self.player_sprite.mouvement_queue if a != "up"]
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.mouvement_queue = [a for a in self.player_sprite.mouvement_queue if a != "down"]
        if key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.mouvement_queue = [a for a in self.player_sprite.mouvement_queue if a != "left"]
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.mouvement_queue = [a for a in self.player_sprite.mouvement_queue if a != "right"]

    def move(self, x, y, sprite):
        for wall in self.scene.get_sprite_list("Walls"):
            if(wall.collides_with_point((x,y))):
                return
        sprite.moving_to_x = x
        sprite.moving_to_y = y
        
        # ease in mouvement
        sprite.center_x = sprite.center_x - ((sprite.center_x - x) / ANIMATION_DETAIL_LEVEL * TPS * (BOOST_TPS_SCALE if self.activate_boost else 1))
        sprite.center_y = sprite.center_y - ((sprite.center_y - y) / ANIMATION_DETAIL_LEVEL * TPS * (BOOST_TPS_SCALE if self.activate_boost else 1)) 
        
        if abs(sprite.center_y - y) < 1 and abs(sprite.center_x - x) < 1:
            sprite.center_x = x
            sprite.center_y = y
            sprite.is_moving = False        

    def apply_action(self, sprite, action):
        if action != "none" and IS_DEBUG:
            print(action)
        if action == "up":
            sprite.is_moving = True
            self.move(sprite.center_x, sprite.center_y + HEIGHT, sprite)
        elif action == "down":
            sprite.is_moving = True
            self.move(sprite.center_x, sprite.center_y - HEIGHT, sprite)
        elif action == "left":
            sprite.is_moving = True
            self.move(sprite.center_x - WIDTH, sprite.center_y, sprite)
        elif action == "right":
            sprite.is_moving = True
            self.move(sprite.center_x + WIDTH, sprite.center_y, sprite)
    
    def play_ghost_turn(self, sprite):
        action = self.ghost_best_action(sprite)
        if action == "up":
            sprite.x = sprite.y + 1 
        elif action == "down":
            sprite.x = sprite.y - 1 
        elif action == "left":
            sprite.x = sprite.x - 1 
        elif action == "right":
            sprite.x = sprite.x + 1 
        self.apply_action(sprite, action)
        sprite.known_cells[sprite.y][sprite.x] = True

    def ghost_best_action(self, sprite):
        return "up"

    def on_update(self, delta_time):
        self.ellapsed_time = time.time() - self.start_time
        self.player_sprite.action = self.player_sprite.mouvement_queue[0] if len(self.player_sprite.mouvement_queue) > 0 else "none"
        
        if self.player_sprite.is_moving:
            self.move(self.player_sprite.moving_to_x, self.player_sprite.moving_to_y, self.player_sprite)
        if self.ghost_sprite.is_moving:
                    self.move(self.ghost_sprite.moving_to_x, self.ghost_sprite.moving_to_y, self.ghost_sprite)

        if(self.ellapsed_time > self.last_action + 1 / (TPS * (BOOST_TPS_SCALE if self.activate_boost else 1))):
            self.last_action = self.ellapsed_time
           
            if not self.player_sprite.is_moving:
                self.apply_action(self.player_sprite, self.player_sprite.action)
                self.player_sprite.action = "none"
            self.play_ghost_turn(self.ghost_sprite)
            


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


