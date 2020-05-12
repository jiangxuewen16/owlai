import importlib
import pkgutil


def auto_import_module(moduleName: str, maxLevel=2):
    """
    自动import指定模块的所有包
    """
    maxLevel -= 1
    if maxLevel <= 0:
        return
    module = importlib.import_module(moduleName)
    for filefiner, name, ispkg in pkgutil.walk_packages(module.__path__):
        if ispkg:
            auto_import_module(moduleName + '.' + name)
        importlib.import_module(moduleName + '.' + name)
