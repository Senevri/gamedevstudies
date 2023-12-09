import importlib
import glob
import os

import time
import traceback
from typing import Optional

import libs

from pprint import pprint, pformat
import logging


logger = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))


class Reloader:
    file_mtimes = {}

    constructor = None

    def mainloop(self, constructor):
        self.file_mtimes = self.get_file_mtimes()
        logger.warn(pformat(file_mtimes))
        reload_obj = constructor()
        state = reload_obj.run(None)
        while True:
            try:
                state = reload_obj.run(state)
            except Exception as ex:
                print(ex)
                print(traceback.format_exc())
                time.sleep(5)
            print("loop")
            if new_obj := self.reload_changed_libs():
                logger.warn("Mainloop: changed library")
                reload_obj = new_obj
            # logger.warn(game_obj.mystr)

            if state.quit:
                break
            # time.sleep(0.1)

    def get_file_mtimes(self):
        # check if any files changed

        files = glob.glob(f"{dir_path}./libs/*.py")
        mtimes = {}
        for file in files:
            cur_mtime = os.stat(file).st_mtime
            mtimes[file] = cur_mtime
        return mtimes

    def reload_changed_libs(self):
        # check if any files changed
        reload = False
        new_mtimes = self.get_file_mtimes()

        for file, new_mtime in new_mtimes.items():
            cur_mtime = self.file_mtimes.get(file, 0)
            if new_mtime != cur_mtime:
                logger.info(f"reload_changed_libs: {file}")
                # file_mtimes[file] = new_mtime
                reload = True

        if reload:
            file_mtimes = new_mtimes
            importlib.reload(libs)
            for module in libs.modules:
                importlib.reload(module)
            logger.info("Reloaded")

        # threading.Timer(5.0, reload_changed_libs, ).start()


if __name__ == "__main__":
    from libs import game, log

    print(__file__)
    reload = Reloader(game.Game)
    reload.mainloop()
