import importlib
import os


def import_modules_from_directory(directory):
    modules = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".py") and not file_name.startswith("__"):
            module_name = file_name[:-3]
            full_module_name = f"{directory}.{module_name}"
            print(full_module_name)
            module = importlib.import_module(full_module_name)
            modules.append(module)
    return modules


# Example usage:
directory_path = "."
modules = import_modules_from_directory(directory_path)
