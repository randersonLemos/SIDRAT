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
    Classe destinada para a ser o pai de todos os sorteios
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(SorteioPadrao, self).__init__()

        self._necessidade = []
        self._contexto = None
        self._name = __name__

        self._tamanho_populacao = None
        """
        Qual o tamanho da população que o sorteio vai retornar
        """

        self._iteracao = None
        """
        Qual a iteração responsavel por esse sorteio
        """

        self._ultimo_id = None
        """
        Qual é o proximo id
        """

        self._solucao_referencia = None
        """
        Solução de referencia para o sorteio
        """

        self._solucoes = Solucoes()
        """
        Conjunto que contem as solucoes sorteadas
        """

        self._solucoes_historico = None

    def before(self):
        self.log(texto=f"Before {self._name}")
        self._solucoes_historico = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

    def run(self):
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Executando {self._name}")

    @property
    def tamanho_populacao(self):
        return self._tamanho_populacao

    @property
    def iteracao(self):
        return self._iteracao

    @property
    def ultimo_id(self):
        return self._ultimo_id

    @property
    def solucao_referencia(self):
        return self._solucao_referencia

    @property
    def solucoes(self):
        return self._solucoes

    @tamanho_populacao.setter
    def tamanho_populacao(self, tamanho_populacao):
        self._tamanho_populacao = tamanho_populacao

    @iteracao.setter
    def iteracao(self, iteracao):
        self._iteracao = iteracao

    @ultimo_id.setter
    def ultimo_id(self, ultimo_id):
        self._ultimo_id = ultimo_id

    @solucao_referencia.setter
    def solucao_referencia(self, solucao_referencia):
        self._solucao_referencia = solucao_referencia

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
