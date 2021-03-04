"""
:author: Rafael
:data: 15/09/2019
"""
from abc import ABCMeta

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.loggin.Loggin import Loggin
from src.problema.Solucoes import Solucoes


class SorteioPadrao(Loggin):
    """
    Class pai dos sorteios
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._necessidade = []

        self._contexto = None

        self._tamanho_populacao = None  # Tamanho população

        self._iteracao = None  # Iteração responsável pelo sorteio

        self._ultimo_id = None  # Qual é o próximo id

        self._solucao_referencia = None  # Solução de referência para o sorteio

        self._solucoes = None  # Conjunto que contem as soluções

        self._solucoes_historico = None  # Histórico de soluções


    def before(self):
        self.log(texto=f"Before {self._name}")

        self._solucoes_historico = self._contexto.get_atributo(EnumAtributo.SOLUCOES)


    def run(self):
        """
        Executa o inicializador desejado.
        """
        self.log(texto=f"Executando {self._name}")


    @property
    def solucoes(self):
        return self._solucoes


    @property
    def necessidade(self):
        return self._necessidade


    @property
    def iteracao(self):
        return self._iteracao


    @iteracao.setter
    def iteracao(self, iteracao):
        self._iteracao = iteracao


    @property
    def contexto(self):
        return self._contexto


    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto


    @property
    def ultimo_id(self):
        return self._ultimo_id


    @ultimo_id.setter
    def ultimo_id(self, ultimo_id):
        self._ultimo_id = ultimo_id


    @property
    def solucao_referencia(self):
        return self._solucao_referencia


    @solucao_referencia.setter
    def solucao_referencia(self, solucao_referencia):
        self._solucao_referencia = solucao_referencia


    @property
    def tamanho_populacao(self):
        return self._tamanho_populacao


    @tamanho_populacao.setter
    def tamanho_populacao(self, tamanho_populacao):
        self._tamanho_populacao = tamanho_populacao
