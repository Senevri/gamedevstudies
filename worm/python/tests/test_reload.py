# test_reload.py
from dataclasses import dataclass
from typing import Optional
import traceback
from pprint import pformat
import time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import libs
import reloader

check_for_updates = reloader.check_for_updates

logger = libs.log.getLogger(__name__)

modification_times = {}


@dataclass
class MockState:
    window_caption = "hello world"
    counter = 0


class MockGame:
    def __init__(self, state: Optional[MockState]):
        if state:
            self.state = state
            self.window_caption = state.window_caption
            self.counter = state.counter
            return
        self.state = MockState()
        self.running = True
        self.counter = 0

    def spinny_animation(self):  # sourcery skip: use-itertools-product
        spinny_chars = ["-", "\\", "|", "/"]
        char = spinny_chars[self.counter % len(spinny_chars)]
        print(f"\b{char}", end="", flush=True)
        time.sleep(0.1)  # Adjust the sleep duration if needed

    def update(self):
        self.counter += 1
        self.state.counter = self.counter
        self.spinny_animation()
        return self.counter < 1000

    def on_cleanup(self):
        print(self.state)


def touch_file(name):
    with open(name, "a") as file:
        st_info = os.stat(name)  # Storing file status
        # setting access time with file's access time (no change)
        # setting modified time with current time of the system)
        os.utime(name, (st_info.st_atime, time.time()))
    # logger.info(f"touched {name}, {st_info}")


if __name__ == "__main__":
    running = True
    module_names = ["tests"]
    state = MockState()
    my_object = MockGame(None)

    while running:
        try:
            for module in check_for_updates(module_names):
                if module:  # shouldn't be needed
                    state = my_object.state  # capture state from object to be reloaded
                    if module.__name__ == "test_reload":
                        my_object = module.MockGame(state)
                    logger.info(f"Reloaded! {my_object.window_caption}")
                else:
                    pass
                    # logger.info(f"shouldn't go here: {module_names}, {module}")
            # Use the updated my_object object
            running = my_object.update()

            state = my_object.state
            if 0 == my_object.counter % 20:
                touch_file(__file__)
        except Exception as ex:
            logger.error(f"{ex}\n{traceback.format_exc()}")
    my_object.on_cleanup()
