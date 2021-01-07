import numpy as np

def getResult(dict_variaveis):
    x = list(dict_variaveis.values())
    return -sum(np.power(x,2))