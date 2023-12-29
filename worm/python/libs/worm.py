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
        self.size = self.weight, self.height = 480, 480
        self.on_init()

    def on_init(self):
        pygame.init()
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

        if event.type == pygame.KEYDOWN:
            pass
        # Example of using the input manager
        if input_manager.is_key_pressed("up"):
            print("Up key pressed")

        if input_manager.is_mouse_button_pressed("left_click"):
            print("Left mouse button clicked")

        if input_manager.is_gamepad_button_pressed("button_a"):
            print("Gamepad button A pressed")

        if input_manager.is_mouse_wheel_up():
            print("Mousewheel up")

        if input_manager.is_mouse_wheel_down():
            print("Mousewheel down")

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
