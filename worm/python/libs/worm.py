from dataclasses import dataclass
from typing import Optional
import pygame
from pygame import Surface
from time import sleep

# from pygame.locals import (

# )

try:
    from libs import log
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
        self.size = self.weight, self.height = 800, 800
        self.on_init()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption(self.state.window_caption + str(self.state.times))
        self.curloop = 0

    def on_event(self, event):
        # logger.info(f"Event! {event}")
        if event.type == pygame.QUIT:
            self._running = False

    def is_running(self):
        return self._running

    def on_loop(self):
        self.curloop += 1
        if self.curloop == 20:
            _worm = WormState(*self.state.worm)
            _worm.x += 1
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
        logger.warn(self.state.worm)
        # logger.warn(self.curloop)
        return self.is_running()
