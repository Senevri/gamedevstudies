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
    worm = WormState(100, 100, 24, (255, 255, 255)).tuple()


class PyGame:
    _display_surf: Surface
    update_display = False

    def __init__(self, state: Optional[State]):
        logger.info(__name__)
        self.state = state if isinstance(state, State) else State()
        self._running = True
        self.old_state = self.state
        self.size = self.width, self.height = 480, 480
        self.worm_direction = (1, 0)
        self.direction_table = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        self.on_init()

    def on_init(self):
        pygame.init()
        pygame.key.set_repeat(0)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption(self.state.window_caption + str(self.state.times))
        self.curloop = 0
        self.input = InputManager()

    def on_event(self, event: Event):
        # logger.info(f"Event! {event}")
        input_manager = self.input
        input_manager.event = event
        if event.type == pygame.QUIT or input_manager.is_key_pressed("quit"):
            self._running = False

        if event.type == pygame.KEYUP:
            return
        if actions := input_manager.get_actions():
            logger.info(actions)
            self.handle_actions(actions)

    def handle_actions(self, actions):
        for action in actions:
            if direction_change := self.direction_table.get(action):
                self.worm_direction = direction_change

    def is_running(self):
        return self._running

    def on_loop(self):
        self.curloop += 1
        if self.curloop == 20:
            _worm = WormState(*self.state.worm)
            x, y = self.worm_direction
            _worm.x += x
            _worm.y += y
            self.curloop = 0
            self.state.worm = _worm.tuple()
            self.update_display = True
        # logger.info(f"Loop!")

    def draw_worm(self):
        worm_s = WormState(*self.state.worm)
        pygame.draw.rect(
            self._display_surf, worm_s.color, (worm_s.x, worm_s.y, worm_s.size, worm_s.size)
        )

    def on_render(self):
        if self.update_display:
            self._display_surf.fill((0, 0, 0))
            self.update_display = False
        self.draw_worm()
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

    def run(self, state):
        # Step function for external reloader.
        # This could all also be IN the reloader
        if state:
            self.state = state
            ws = WormState(*state.worm)
            ws.color = (200, 255, 0)
            self.state.worm = ws.tuple()
        if not self.update():
            self.state.quit_game = True
        return self.state
