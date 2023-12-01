import sys
import os
import arcade
from pyglet.window import key as pyglet_key
from dataclasses import dataclass, asdict
from typing import Optional
from logging import getLogger
from reloader import Reloader
logger = getLogger(__package__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

reload = Reloader()

resource_path = os.path.join(os.path.dirname(__file__))
sys.path.append(resource_path)

def log_key(key, modifiers = None):
    logger.warning(f"Key: {pyglet_key.symbol_string(key)}, modifiers: {modifiers})")


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(os.path.join(resource_path, "player.png"))
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

    def __repr__(self):
        return (str((self.center_x, self.center_y, self.change_x, self.change_y)))

@dataclass
class GameState:
    player: Optional[Player] = None
    player_list: arcade.SpriteList = arcade.SpriteList()

class MyGame(arcade.Window):
    keys_down = set()

    def __init__(self, state = None):
        self.state = state or GameState()
        self.set_location(50,50)
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "My VS Clone")
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.lastupdate = 0
        self.terminated = False


    def setup(self, state=None):
        self.state.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if not self.state.player_list:
            self.state.player_list = arcade.SpriteList()
        if self.state.player not in self.state.player_list:
            self.state.player_list.append(self.state.player)

    def on_key_release(self, key, modifiers):
        log_key(key, modifiers)

        key_lookup_x = [
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ]
        key_lookup_y = [
            arcade.key.UP,
            arcade.key.DOWN
        ]

        if key in key_lookup_x:
            self.state.player.change_x = 0
        if key in key_lookup_y:
            self.state.player.change_y = 0

        if key in key_lookup_x or key in key_lookup_y:
            self.keys_down.remove(key)

    #def on_key_down(self, key, modifiers):

    def on_key_press(self, key, modifiers):
        log_key(key, modifiers)

        key_lookup = {
            arcade.key.LEFT: (-5, 0),
            arcade.key.RIGHT: (5, 0),
            arcade.key.UP: (0, 5),
            arcade.key.DOWN: (0, -5),
            arcade.key.ESCAPE: "close"
        }

        if key in key_lookup:
            action = key_lookup[key]
            if action == "close":
                self.terminated = True
                arcade.close_window()
            elif isinstance(key_lookup[key], tuple):
                self.keys_down.add(key)
                self.state.player.change_x, self.state.player.change_y = action
        #self.state.player.center_x += self.state.player.change_x
        #self.state.player.center_y += self.state.player.change_y

    def on_draw(self):
        arcade.start_render()
        try:
            self.state.player_list.draw()
        except Exception as ex:
            logger.error(ex)
            logger.warn(self.state)
            arcade.close_window()


    def on_update(self, delta_time):
        self.lastupdate += delta_time
        if self.lastupdate > 5:
            self.lastupdate = 0
            if reload.list_updated_files():
                arcade.close_window()
        #logger.warning(self.state.player)

        if self.keys_down:
            if arcade.key.LEFT in self.keys_down or  arcade.key.RIGHT in self.keys_down:
                self.state.player.center_x += self.state.player.change_x
            if arcade.key.UP in self.keys_down or  arcade.key.DOWN in self.keys_down:
                self.state.player.center_y += self.state.player.change_y

        self.state.player_list.update()

def main():
    game = MyGame()
    while not game.terminated:
        game.setup()
        arcade.run()
        state = game.state
        game = MyGame(state)



if __name__ == "__main__":
    main()
