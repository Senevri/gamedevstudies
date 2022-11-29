import importlib
import glob
import os
import logging
import time
import traceback
from typing import Optional

import libs
from libs import game

logging.basicConfig()
logger = logging.getLogger("Main")
logging.getLogger("Main").setLevel(logging.DEBUG)
logger.warn = logger.warning

dir_path = os.path.dirname(os.path.realpath(__file__))

file_mtimes = {}

def mainloop():
    file_mtimes =get_file_mtimes()
    game_obj = game.Game()
    state = None
    while True:
        try:
            state = game_obj.run(state)
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            time.sleep(5)
        print ("loop")
        if new_obj := reload_changed_libs():
            logger.warn("Mainloop: changed library")
            game_obj = new_obj
        # logger.warn(game_obj.mystr)

        if state.quit_game:
            break
        #time.sleep(0.1)

def get_file_mtimes():
    files = glob.glob(f"{dir_path}./libs/*.py")
    mtimes = {}
    for file in files:
        cur_mtime = os.stat(file).st_mtime
        mtimes[file] = cur_mtime
    return mtimes

def reload_changed_libs() -> Optional[game.Game]:
    # check if any files changed
    files = glob.glob(f"{dir_path}./libs/*.py")
    #files.append(__file__)
    reload = False
    new_mtimes = get_file_mtimes()

    for file, new_mtime in new_mtimes.items():
        cur_mtime = file_mtimes.get(file, 0)
        if new_mtime != cur_mtime:
            logger.info(f"reload_changed_libs: {file}")
            file_mtimes[file] = new_mtime
            reload = True

    if reload:
        importlib.reload(libs)
        for module in libs.modules:
            importlib.reload(module)
        logger.info("Reloaded")
        return game.Game()
    # threading.Timer(5.0, reload_changed_libs, ).start()

if __name__ == "__main__":
    mainloop()
