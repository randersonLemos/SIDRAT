import numpy as np
import os
import src.modulo.problemas_fechados.funcoes_teste.base.knapsack


def getResult(dict_variaveis):
    """
    Problema da mochila sem repeticao, em que deve-se maximizar o valor dos produtos dentro de uma mochila sem exceder
    uma restricao de peso. Cada produto tem um valor e peso especifico
    :param dict_variaveis:
    :return: valor da somatoria dos valores dos produtos na mochila ou menos infinito caso a restricao seja atingida
    """
    folder_data_base = os.path.dirname(src.modulo.problemas_fechados.funcoes_teste.base.knapsack.__file__)

    weight_value = np.load(os.path.join(folder_data_base, 'weight_value_knapsack.npy'))
    x = np.array(list(dict_variaveis.values())).reshape(1,-1)

    weight_constraint = weight_value[:x.shape[1], :].sum(axis=0)[0] / 1.5

    weight_value_solution = x.dot(weight_value[:x.shape[1], :])
    weigh, value = weight_value_solution[0][0], weight_value_solution[0][1]

    return value if weigh < weight_constraint else -float('inf')