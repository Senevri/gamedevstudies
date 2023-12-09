import importlib
import test_arcade
from log import getLogger

logger = getLogger(__name__)

persist_state = None


def run_game():
    global persist_state
    game = test_arcade.MyGame(persist_state)
    game.setup()
    game.run()
    persist_state = game.state
    return game


while True:
    importlib.reload(test_arcade)
    game = run_game()
    if game.terminated:
        logger.warning("Terminating game...")
        break
    del game
