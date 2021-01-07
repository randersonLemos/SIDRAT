"""
:author: Rafael
:data: 15/09/2019
"""
from abc import ABCMeta

from src.modulo.visualizacao.painel.PainelPadrao import PainelPadrao


class Execucao(PainelPadrao):
    """
    Classe destinada para a ser o pai de todos os sorteios
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Execucao, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [] + super(Execucao, self).necessidade

    def run(self):
        """
        Executa o inicializador desejado.
        """
        super(Execucao, self).run()

        #TODO colocar o codigo
