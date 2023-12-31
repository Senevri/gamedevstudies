# basegame.py
import os, sys

from dataclasses import dataclass
from typing import Optional
import pygame
from pygame import Surface
from pygame.event import Event

from libs import log
from libs.userinput import InputManager

logger = log.getLogger(__name__)


@dataclass
class BaseState:
    window_caption: str = ""
    times: int = 0
    quit_game: bool = False


class PyGame:
    _display_surf: Surface
    update_display = False

    def __init__(self, state: Optional[BaseState], game_logic_callbacks={}):
        self.pygame = pygame
        logger.info(__name__)
        self.state = state if isinstance(state, BaseState) else BaseState()
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
