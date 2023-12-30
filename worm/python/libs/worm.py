from dataclasses import dataclass
from typing import Optional
import pygame
from pygame import Surface
from pygame.event import Event
import os, sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from libs import log
    from libs.userinput import InputManager
except ImportError:
    from . import log

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


@dataclass
class State:
    window_caption: str = ""
    times: int = 0
    quit_game: bool = False
    worm_direction = (1, 0)
    worm = WormState(100, 100, 24, (255, 255, 255)).tuple()


class PyGame:
    _display_surf: Surface
    update_display = False

    def __init__(self, state: Optional[State], game_logic_callbacks={}):
        logger.info(__name__)
        self.state = state if isinstance(state, State) else State()
        self._running = True
        self.old_state = self.state
        self.size = self.width, self.height = 480, 480
        self.callbacks = game_logic_callbacks
        self.on_init()

    def on_init(self):
        pygame.init()
        pygame.key.set_repeat(0)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption(self.state.window_caption + str(self.state.times))
        self.curloop = 0
        self.input = InputManager()
        self.run_callback("initialize")

    def run_callback(self, callback_name):
        if callback_name in self.callbacks:
            self.callbacks[callback_name](self)

    def on_event(self, event: Event):
        # logger.info(f"Event! {event}")
        input_manager = self.input
        input_manager.event = event
        if event.type == pygame.QUIT or input_manager.is_key_pressed("quit"):
            self._running = False

        if event.type == pygame.KEYUP:
            return

        if event.type == pygame.JOYHATMOTION:
            pass

        if actions := input_manager.get_actions():
            logger.info(actions)
            self.handle_actions(actions)
        else:
            # unhandled event
            logger.debug(event)

    def handle_actions(self, actions):
        self.actions = actions
        self.run_callback("handle_actions")

    def is_running(self):
        return self._running

    def on_loop(self):
        self.curloop += 1
        self.run_callback("loop")
        self.update_display = True
        # logger.info(f"Loop!")

    def on_render(self):
        if self.update_display:
            self._display_surf.fill((0, 0, 0))
            self.update_display = False
        self.run_callback("render")
        # logger.info("render")
        pygame.display.update()

    def on_cleanup(self):
        self.state.times += 1
        pygame.quit()

    def on_execute(self):
        # logger.info("running")
        for event in pygame.event.get():
            self.on_event(event)
        self.on_loop()
        self.on_render()
        # Reload libs here

    def update(self):
        self.on_execute()
        # logger.info(f"Worm: {self.state.worm}")
        # logger.warn(self.curloop)
        return self.is_running()


class Worm:
    def __init__(self, state):
        callbacks = {
            "initialize": self.initialize_game,
            "terminate": self.terminate,
            "loop": self.update_worm,
            "handle_actions": self.handle_actions,
            "render": self.render,
        }
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
        pygame.draw.rect(
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
