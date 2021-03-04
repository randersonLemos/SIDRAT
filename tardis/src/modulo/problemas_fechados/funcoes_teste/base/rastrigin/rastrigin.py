import numpy as np


def getResult(dict_variaveis):
    x = list(dict_variaveis.values())
    n = len(x)
    x = np.array(x)/15
    A = 10
    return -(A * n + sum(np.power(x, 2) - A * np.cos(2 * np.pi * x)))
