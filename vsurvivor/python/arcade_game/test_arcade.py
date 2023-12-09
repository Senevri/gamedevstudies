import sys
import os
import arcade
from pyglet.window import key as pyglet_key
from dataclasses import dataclass, asdict
from typing import Optional
from log import getLogger
from reloader import Reloader
import time

logger = getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

reload = Reloader()

resource_path = os.path.join(os.path.dirname(__file__))
sys.path.append(resource_path)


def log_key(key, modifiers=None):
    logger.warning(f"Key: {pyglet_key.symbol_string(key)}, modifiers: {modifiers})")


@dataclass
class PlayerData:
    center_x: int = 0
    center_y: int = 0
    change_x: int = 0
    change_y: int = 0


class Player(arcade.Sprite):
    def __init__(self, pd: PlayerData):
        self.data = pd
        super().__init__(os.path.join(resource_path, "player.png"))
        self.center_x = pd.center_x
        self.center_y = pd.center_y
        self.change_x = pd.change_x
        self.change_y = pd.change_y

    def __repr__(self):
        return str((self.center_x, self.center_y, self.change_x, self.change_y))

    def update(self, newdata: Optional[PlayerData] = None):
        if newdata:
            self.data = newdata
        attr_names = ["center_x", "center_y", "change_x", "change_y"]
        for key in attr_names:
            setattr(self, key, getattr(self.data, key))


@dataclass
class GameState:
    player: Optional[Player] = None
    player_list: list[PlayerData] = None


class MyGame(arcade.Window):
    keys_down = set()
    changed = False
    run = lambda self: arcade.run()

    def __init__(self, state=None):
        reload.reload(arcade)
        reload.update_filetimes()
        self.state = state or GameState()
        self.sprites: arcade.SpriteList = arcade.SpriteList()
        self.state.player_list = []
        self.set_location(50, 50)
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "My VS Clone")
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.lastupdate = 0
        self.terminated = False

    def setup(self, state=None):
        if not self.state.player:
            self.state.player = PlayerData(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if self.state.player not in self.state.player_list:
            self.state.player_list.append(self.state.player)
        self.sprites.append(Player(self.state.player))
        logger.warn(self.state.player_list)

    def on_key_release(self, key, modifiers):
        log_key(key, modifiers)

        key_lookup_x = [
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ]
        key_lookup_y = [arcade.key.UP, arcade.key.DOWN]

        if key in key_lookup_x:
            self.state.player.change_x = 0
        if key in key_lookup_y:
            self.state.player.change_y = 0

        if key in key_lookup_x or key in key_lookup_y:
            self.keys_down.remove(key)

    # def on_key_down(self, key, modifiers):

    def on_key_press(self, key, modifiers):
        log_key(key, modifiers)

        key_lookup = {
            arcade.key.LEFT: (-5, 0),
            arcade.key.RIGHT: (5, 0),
            arcade.key.UP: (0, 5),
            arcade.key.DOWN: (0, -5),
            arcade.key.ESCAPE: "close",
        }

        if key in key_lookup:
            action = key_lookup[key]
            if action == "close":
                self.terminated = True
                arcade.exit()
            elif isinstance(key_lookup[key], tuple):
                self.keys_down.add(key)
                self.state.player.change_x, self.state.player.change_y = action
        # self.state.player.center_x += self.state.player.change_x
        # self.state.player.center_y += self.state.player.change_y

    def on_draw(self):
        if self.terminated or self.changed:
            return
        arcade.start_render()
        try:
            for sprite in self.sprites:
                sprite.update()
            self.sprites.draw()
        except Exception as ex:
            logger.error(ex)
            logger.warn(self.state)
            arcade.close_window()

    def exit(self):
        arcade.exit()

    def on_update(self, delta_time):
        self.lastupdate += delta_time
        if self.lastupdate > 5:
            self.lastupdate = 0
            if updated := reload.list_updated_files():
                self.changed = True
                reload.update_filetimes()
                logger.info(f"Changed : {list(updated)}")
                arcade.close_window()
                arcade.exit()
                return
        # logger.warning(self.state.player)

        if self.keys_down:
            if arcade.key.LEFT in self.keys_down or arcade.key.RIGHT in self.keys_down:
                self.state.player.center_x += self.state.player.change_x
            if arcade.key.UP in self.keys_down or arcade.key.DOWN in self.keys_down:
                self.state.player.center_y += self.state.player.change_y
        self.sprites.update()


def main():
    game = MyGame()
    while not game.terminated:
        game.setup()
        arcade.run()
        state = game.state
        game = MyGame(state)


if __name__ == "__main__":
    main()
