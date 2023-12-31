# worm.py
from dataclasses import dataclass
import os, sys


from libs import log
from libs.userinput import InputManager
from libs.basegame import PyGame, BaseState

logger = log.getLogger(__name__)


@dataclass
class WormState:
    x: int
    y: int
    size: int
    color: tuple

    def tuple(self):
        return (self.x, self.y, self.size, self.color)

    def __eq__(self, cmp):
        logger.warn("cmp")
        # return any(
        #     self.x != cmp.x
        # )
        return self.tuple() != cmp.tuple()


class State(BaseState):
    window_caption: str = ""
    times: int = 0
    quit_game: bool = False
    worm_direction = (1, 0)
    worm = WormState(100, 100, 24, (255, 255, 255)).tuple()


class Worm:
    def __init__(self, state):
        callbacks = {
            "initialize": self.initialize_game,
            "terminate": self.terminate,
            "loop": self.update_worm,
            "handle_actions": self.handle_actions,
            "render": self.render,
        }
        state = state or State()
        self.direction_table = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        self.game = PyGame(state, callbacks)

    def initialize_game(self, game: PyGame):
        pass

    def terminate(self):
        return self.game.on_cleanup()

    def handle_actions(self, game):
        for action in game.actions:
            if direction_change := self.direction_table.get(action):
                game.state.worm_direction = direction_change

    def update_worm(self, game):
        if game.curloop == 20:
            _worm = WormState(*game.state.worm)
            x, y = game.state.worm_direction
            _worm.x += x
            _worm.y += y
            game.curloop = 0
            game.state.worm = _worm.tuple()

    def render(self, game):
        worm_s = WormState(*game.state.worm)
        game.pygame.draw.rect(
            game._display_surf, worm_s.color, (worm_s.x, worm_s.y, worm_s.size, worm_s.size)
        )

    def run(self, state):
        # Step function for external reloader.
        # This could all also be IN the reloader
        if state:
            self.game.state = state
            ws = WormState(*state.worm)
            ws.color = (200, 255, 100)
            self.game.state.worm = ws.tuple()
        if not self.game.update():
            self.game.state.quit_game = True
        return self.game.state
