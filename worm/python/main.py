import importlib
import libs
import os
import time
import pygame
import glob
import inspect
import traceback
from pprint import pformat

logger = libs.log.getLogger(__name__)

modification_times = {}


def check_for_updates(folder):
    # Get a list of all .py files in the specified folder
    files = glob.glob(f"{folder}/*.py")

    # Check if any of the files have been modified
    for file in files:
        if modification_times.get(file) != os.path.getmtime(file):
            # Reload the module
            module_name = file.split("/")[-1][:-3]
            full_module_name = folder.replace("/", ".") + "." + module_name
            logger.info((file, module_name, full_module_name))
            imported_module = importlib.import_module("libs")
            libs = importlib.reload(imported_module)

            # Get a list of all the modules in the libs package
            module_list = [m[1] for m in inspect.getmembers(libs, inspect.ismodule)]
            logger.info(pformat(module_list))
            for module in module_list:
                importlib.reload(module)

            # Update the modification time
            modification_times[file] = os.path.getmtime(file)

            # Return the reloaded module
            return imported_module


if __name__ == "__main__":
    # Run the game loop
    running = True
    libs = check_for_updates("libs")

    if inspect.ismodule(libs):
        my_object = libs.worm.PyGame(None)
        state = my_object.state
    else:
        exit(-1)

    while running:
        try:
            if libs := check_for_updates("libs"):
                # Edit this line to reflect your dynamic stateful object
                my_object = libs.worm.PyGame(state)
                logger.info("Reloaded!")
            # Use the updated my_object object
            running = my_object.update()
            my_object.state.window_caption = "asdf"
            state = my_object.state

        except Exception as ex:
            logger.error(f"{ex}\n{traceback.format_exc()}")
    my_object.on_cleanup()
