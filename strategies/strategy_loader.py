import importlib.util
import os
import inspect
from strategies.base import Strategy


def load_strategies_from_folder(folder_path: str):
    strategies = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, folder_path))[0].replace(os.sep, ".")
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Strategy) and obj is not Strategy:
                        strategies.append(obj())
    return strategies
