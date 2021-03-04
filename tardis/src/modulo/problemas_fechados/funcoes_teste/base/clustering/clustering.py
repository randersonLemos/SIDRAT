import numpy as np
import os
from scipy.spatial import distance_matrix
import src.modulo.problemas_fechados.funcoes_teste.base.clustering


def getResult(dict_variaveis):
    """
    Problema de clusterizacao. Variaveis de decisão são os centros dos clusters e a funcao objetivo é o somatorio
    de um conjunto de pontos (fixos) ate os centros dos clusters mais proximos.
    :param dict_variaveis:
    :return: quadrado da somatoria das distancias
    """

    folder_data_base = os.path.dirname(src.modulo.problemas_fechados.funcoes_teste.base.clustering.__file__)

    coord_elements = np.load(os.path.join(folder_data_base, 'coor_pontos_clustering.npy'))

    coord_cent = [[dict_variaveis[f'x{a}'], dict_variaveis[f'y{a}']] for a in
                  range(1, int(len(dict_variaveis) / 2 + 1))]

    matrix_dist = distance_matrix(coord_elements, coord_cent)
    cluster_associados = matrix_dist.argmin(axis=1)
    cluster_label, count = np.unique(cluster_associados, return_counts=True)
    print('cluster quantity')
    cont = ''
    for label, qtt in zip(cluster_label, count):
        cont += f'label={label}, qtt={qtt};\t'
    print(cont)

    return -(-matrix_dist.min(axis=1).sum()) ** 2
