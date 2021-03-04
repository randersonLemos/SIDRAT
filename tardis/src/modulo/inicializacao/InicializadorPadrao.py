"""
:author: Rafael
:data: 07/09/2020
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.loggin.Loggin import Loggin


class InicializadorPadrao(Loggin):
    """
    Classe destinada para a ser o pai de todos os inicializadores
    """


    def __init__(self):
        super().__init__()
        self._name = __name__
        self._necessidade = []
        self._contexto = None
        self._nomes_direcoes_of = None


    def run(self, contexto):
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Executando {self._name}")
        self._contexto = contexto
        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)


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
