import numpy as np

def getResult(dict_variaveis):
    x = list(dict_variaveis.values())
    xi = np.array(x[:-1])
    xi_mais_1 = np.array(x[1:])
    return -(sum(100 * (np.power(xi_mais_1 - np.power(xi, 2), 2) + np.power((1 - xi), 2))))