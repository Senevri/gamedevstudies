# reloader.py
import importlib
import glob
import os

import time
import traceback
from types import ModuleType
from typing import Optional

import libs
from libs import log
from pprint import pprint, pformat
import inspect

logger = log.getLogger("Main")

dir_path = os.path.dirname(os.path.realpath(__file__))

file_modification_times = {}


def get_file_mtimes(module_name="libs"):
    files = glob.glob(os.path.join(dir_path, module_name, "*.py"))
    mtimes = {}
    for file in files:
        cur_mtime = os.stat(file).st_mtime
        mtimes[file] = cur_mtime
    return mtimes


def check_for_updates(item) -> list:
    reloaded_items = []
    if isinstance(item, str):
        if item.endswith(".py"):
            reloaded_items.append(reload_module_from_file(item))
        else:
            reloaded_items.extend(check_for_folder_updates(item))
    if isinstance(item, list):
        # check_for_folder_updates(os.path.join(dir_path, folder)) for folder in item

        for updated_item in (check_for_folder_updates(folder) for folder in item):
            reloaded_items.extend(updated_item)

    return reloaded_items


def update_modification_time(file):
    # Update the modification time
    realpath = os.path.realpath(file)
    file_modification_times[realpath] = os.path.getmtime(realpath)


def check_for_folder_updates(folder):
    # Get a list of all .py files in the specified folder
    files_path = os.path.join(folder, "*.py")
    files = glob.glob(files_path)
    reloaded_modules = []
    # Check if any of the files have been modified
    for file in files:
        module_name = os.path.basename(file)[:-3]
        if module_name == "__init__":
            continue
        module = reload_module_from_file(file, folder)
        update_modification_time(file)
        if not module:
            continue
        reloaded_modules.append(module)
        # Return the reloaded module
    return reloaded_modules


def reload_module_from_file(file, folder=None):
    global file_modification_times
    if not folder:
        folder = dir_path

    realpath = os.path.realpath(file)
    if file_modification_times.get(realpath) != os.path.getmtime(realpath):
        # Reload the module
        module_name = os.path.basename(file)[:-3]
        reload_module(f"{folder}.{module_name}")


def reload_changed_libs(module_str) -> Optional[object]:
    global file_modification_times

    reload = False
    # check if any files changed
    new_mtimes = get_file_mtimes(module_str)

    for file, new_mtime in new_mtimes.items():
        cur_mtime = file_modification_times.get(file, 0)
        if new_mtime != cur_mtime:
            logger.info(f"reload_changed_libs: {file}")
            # file_mtimes[file] = new_mtime
            reload = True

    if reload:
        file_modification_times = new_mtimes
        return reload_module(module_str)


def reload_module(module_str):
    main_module: ModuleType = importlib.import_module(module_str)
    importlib.reload(main_module)
    module_list = [m[1] for m in inspect.getmembers(main_module, inspect.ismodule) if m[1]]
    # logger.info(pformat(module_list))
    for submodule in module_list:
        importlib.reload(submodule)
    logger.info(f"Reloaded {main_module.__name__}")
    return main_module
    # threading.Timer(5.0, reload_changed_libs, ).start()


def example_main_loop():
    global file_modification_times
    file_modification_times = get_file_mtimes()
    # logger.info(pformat(file_modification_times))
    game_obj = libs.worm.PyGame(None)  # an object encapsulating the stateful system
    if not game_obj:
        return -1
    state: libs.worm.State = game_obj.run(None)

    while True:
        try:
            state = game_obj.run(state)
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            time.sleep(5)
        if new_lib := reload_changed_libs(libs.__name__):
            logger.warn("Mainloop: changed library")
            game_obj.on_cleanup()
            game_obj = new_lib.worm.PyGame(state)
        # logger.warn(game_obj.mystr)

        if state.quit_game:
            break
    pprint(state)
    # time.sleep(0.1)
    return 0


if __name__ == "__main__":
    print(__file__)
    example_main_loop()
