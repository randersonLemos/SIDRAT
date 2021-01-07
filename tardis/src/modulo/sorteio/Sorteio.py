"""
:author: Rafael
:data: 06/12/2019
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.sorteio.HLDG.HLDG import HLDG
from src.modulo.sorteio.SorteioPadrao import SorteioPadrao


class Sorteio(ModuloPadrao):
    """
    Classe destinada para carregar o modulo de Sorteio
    """

    def __init__(self):
        super(Sorteio, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [] + super(Sorteio, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._sorteio = SorteioPadrao()

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Sorteio, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.SORTEIO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.SORTEIO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.HLDG.name) or (tipo == EnumValues.HLDG):
                self.log(texto=f'O modulo de sorteio [{EnumValues.HLDG.name}] foi definido.')
                self._sorteio = HLDG()

            self._necessidade += self._sorteio.necessidade

    def run(self, contexto) -> Contexto:
        """
        Executa o sorteio desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._sorteio.name
        self._contexto = super(Sorteio, self).run(contexto)

        self._sorteio.contexto = self._contexto
        self._sorteio.before()
        self._sorteio.run()

        return self._sorteio.contexto

    @property
    def sorteio(self):
        return self._sorteio
