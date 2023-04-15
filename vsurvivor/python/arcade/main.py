import importlib
import test_arcade
from logging import getLogger

logger = getLogger(__file__)

persist_state = None

def run_game():
    global persist_state
    game = test_arcade.MyGame(persist_state)
    game.setup()
    test_arcade.arcade.run()
    persist_state = game.state
    return game.terminated

while True:
    importlib.reload(test_arcade)
    terminate = run_game()
    if terminate:
        logger.warning("Terminating game...")
        break
