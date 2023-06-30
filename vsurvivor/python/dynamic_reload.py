import importlib
import my_module
import os
import time
import pygame
import glob
import inspect
from logging import getLogger

logger = getLogger(__name__)

modification_times = {}

def check_for_updates(folder):
    # Get a list of all .py files in the specified folder
    files = glob.glob(f'{folder}/*.py')

    # Check if any of the files have been modified
    for file in files:
        if modification_times.get(file) != os.path.getmtime(file):
            # Reload the module
            module_name = file.split('/')[-1][:-3]
            full_module_name = folder.replace('/', '.') + '.' + module_name
            logger.warn((file, module_name, full_module_name))
            imported_module = importlib.import_module('my_module')
            my_module = importlib.reload(imported_module)

            # Get a list of all the modules in the my_module package
            module_list = [m[1] for m in inspect.getmembers(my_module, inspect.ismodule)]
            for module in module_list:
                logger.warn(module)
                importlib.reload(module)

            # Update the modification time
            modification_times[file] = os.path.getmtime(file)

            # Return the reloaded module
            return imported_module

# Run the game loop
running = True
my_module = check_for_updates("my_module")
my_object = my_module.my_class.MyClass()
state = my_object.state

while running:
    try:
        # Handle events
        for event in my_object.get_events():
            if event.type == pygame.QUIT:
                running = False

        if my_module := check_for_updates("my_module"):
            my_object = my_module.my_class.MyClass(state)

        my_object.update()

        # Use the updated my_object object
    except Exception as ex:
        logger.error(ex)
