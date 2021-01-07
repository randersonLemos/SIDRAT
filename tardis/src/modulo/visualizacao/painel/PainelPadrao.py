"""
:author: Rafael
:data: 15/09/2019
"""
from abc import ABCMeta

from src.contexto.Contexto import Contexto
from src.loggin.Loggin import Loggin


class PainelPadrao(Loggin):
    """
    Classe destinada para a ser o pai de todos os sorteios
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(PainelPadrao, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._contexto = None
        """
        Todas as informações necessárias
        """

        self._necessidade = []
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

    def run(self):
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Executando {self._name}")

    @property
    def contexto(self):
        """
        contexto com todas as informações necessárias
        :return:
        """
        return self._contexto

    @property
    def necessidade(self):
        """
        Defini quais os atributos necessarios para executar o modulo desejado
        """
        return self._necessidade

    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto
