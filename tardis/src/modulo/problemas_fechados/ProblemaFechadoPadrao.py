"""
:author: Rafael
:data: 17/09/2020
"""
from abc import ABCMeta

from src.contexto.Contexto import Contexto
from src.loggin.Loggin import Loggin


class ProblemaFechadoPadrao(Loggin):
    """
    Classe destinada para a ser o pai de todos os inicializadores
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()
        self._necessidade = []
        self._contexto = None
        self._name = __name__

    def run(self, contexto):
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Executando {self._name}")
        self._contexto = contexto

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
