# userinput.py
from typing import Optional
import pygame
from pygame.locals import *


class InputManager:
    def __init__(self):
        self.actions = "up,down,left,right,fire,quit".split(",")

        self.key_mappings = {
            "up": K_UP,
            "down": K_DOWN,
            "left": K_LEFT,
            "right": K_RIGHT,
            "fire": K_SPACE,
            "quit": K_ESCAPE,
        }

        self.mouse_mappings = {"left_click": 0, "right_click": 2, "middle_click": 1}

        self.gamepad_mappings = {
            "button_a": 0,
            "button_b": 1,
            "button_x": 2,
            "button_y": 3,
            "start": 9,
            "select": 8,
        }
        self.event: Optional[pygame.event.Event] = None

        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def is_key_pressed(self, key):
        return pygame.key.get_pressed()[self.key_mappings[key]] == 1

    def is_mouse_button_pressed(self, button):
        return pygame.mouse.get_pressed()[self.mouse_mappings[button]] == 1

    def is_gamepad_button_pressed(self, button):
        if self.joystick:
            return self.joystick.get_button(self.gamepad_mappings[button]) == 1
        return False

    def get_gamepad_direction(self):
        if self.joystick:
            return [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]

    def is_mouse_wheel_up(self):
        if event := self.event:
            return (
                event.type == MOUSEBUTTONDOWN
                and event.button == 4
                or (event.type == MOUSEWHEEL and event.y > 0)
            )
        return False

    def is_mouse_wheel_down(self):
        if event := self.event:
            return (
                event.type == MOUSEBUTTONDOWN
                and event.button == 5
                or (event.type == MOUSEWHEEL and event.y < 0)
            )
        return False

    def get_actions(self):
        # sourcery skip: for-append-to-extend, inline-immediately-returned-variable, list-comprehension
        current_actions = []
        for action in self.actions:
            if (
                (action in self.key_mappings and self.is_key_pressed(action))
                or (action in self.gamepad_mappings and self.is_gamepad_button_pressed(action))
                or (action in self.mouse_mappings and self.is_mouse_button_pressed(action))
            ):
                current_actions.append(action)
        return current_actions


def main():
    input_manager = InputManager()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Example of using the input manager
        if input_manager.is_key_pressed("up"):
            print("Up key pressed")

        if input_manager.is_mouse_button_pressed("left_click"):
            print("Left mouse button clicked")

        if input_manager.is_gamepad_button_pressed("button_a"):
            print("Gamepad button A pressed")

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
