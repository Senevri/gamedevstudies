import importlib
import glob
import os
import logging
import threading
import time
import libs
import pkgutil
from libs import game

logging.getLogger().setLevel(logging.DEBUG)

logging.warn = logging.warning

dir_path = os.path.dirname(os.path.realpath(__file__))

file_mtimes = {}

def mainloop():
    game_obj = None
    while True:
        if new_obj := reload_changed_libs():
            logging.warn("Mainloop: changed library")
            game_obj = new_obj
        # logging.warn(game_obj.mystr)
        game_obj.run()

        time.sleep(1)


def reload_changed_libs():
    # check if any files changed
    files = glob.glob(f"{dir_path}./libs/*.py")
    files.append(__file__)
    reload = False
    for file in files:
        cur_mtime = file_mtimes.get(file, 0)
        new_mtime = os.stat(file).st_mtime
        if new_mtime != cur_mtime:
            logging.info(f"reload_changed_libs: {file}")
            file_mtimes[file] = new_mtime
            reload = True
    if reload:
        importlib.reload(libs)
        for module in libs.modules:
            importlib.reload(module)
        logging.info(f"Reloaded {file}")
        return game.Game()
    # threading.Timer(5.0, reload_changed_libs, ).start()

if __name__ == "__main__":
    mainloop()
