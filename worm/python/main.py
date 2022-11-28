import importlib
import glob
import os
import logging
import threading
import time
import libs
from libs import game

logging.getLogger().setLevel(logging.DEBUG)

dir_path = os.path.dirname(os.path.realpath(__file__))

file_mtimes = {}

def mainloop(game_obj: game.Game):
    while(True):
        game_obj.test()
        new_obj = reload_changed_libs()
        logging.warn(game_obj)
        game_obj = new_obj or game_obj
        time.sleep(1)


def reload_changed_libs():
    # check if any files changed
    files = glob.glob(f"{dir_path}./libs/*.py")
    for file in files:
        cur_mtime = file_mtimes.get(file, 0)
        new_mtime = os.stat(file).st_mtime
        if new_mtime != cur_mtime:
            logging.info(f"reload_changed_libs: {file}")
            file_mtimes[file] = new_mtime
            importlib.reload(libs)
            from libs import game
            logging.info(f"Reloaded {file}")
            return game.Game()

    #threading.Timer(5.0, reload_changed_libs, [game]).start()

if __name__ == "__main__":
    #reload_changed_libs(game)
    _game = game.Game()
    mainloop(_game)
