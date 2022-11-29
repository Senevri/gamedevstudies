import logging

import time
from datetime import datetime

from .worm import PyGame, State

logging.basicConfig()
logger = logging.getLogger("Game")
logging.getLogger("Game").setLevel(logging.DEBUG)
logger.warn = logger.warning


class Game:
    mystr = ""
    times = 0

    def __init__(self, state = None):
        # this state is only initial, not used on reload
        self.state = State(
            window_caption="Pygame Window "
        )
        self.mystr = "Hello world"

    def try_pygame(self, state: State):
        self.pygame = PyGame(state)
        #self.pygame.set_state(state)
        self.pygame.on_execute()

    def run(self, state):
        logger.info(datetime.now())
        self.test()
        state = state or self.state
        self.try_pygame(state)
        time.sleep(1)
        self.pygame.state.times += 1

        return self.pygame.state


    def test(self):
        #logger.info(self)
        #print(self.mystr + str(self.times))
        self.times += 1

