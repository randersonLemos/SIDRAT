import os
import sys
import importlib


def load_method(path_python: str) -> "getResult":
    """

    Método responsável pelo carregamento de um arquivo python externo ao tardis que contem o metodo getResult
    :param path_python:
    :return:
    """

    file = os.path.basename(path_python)
    dir = os.path.dirname(path_python)

    module_name = file.split('.')[0]

    sys.path.append(dir)

    return importlib.import_module(module_name).getResult
