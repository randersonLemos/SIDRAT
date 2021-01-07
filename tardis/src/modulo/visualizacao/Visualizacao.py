"""
:author: Rafael
:data: 01/10/2020
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.visualizacao.painel.PainelPadrao import PainelPadrao
from src.modulo.visualizacao.painel.comparacao.Comparacao import Comparacao
from src.modulo.visualizacao.painel.execucao.Execucao import Execucao


class Visualizacao(ModuloPadrao):
    """
    Classe destinada para carregar o modulo de Sorteio
    """

    def __init__(self):
        super(Visualizacao, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.VISUALIZACAO_TYPE] + super(Visualizacao, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._painel = PainelPadrao()

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Visualizacao, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.VISUALIZACAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.VISUALIZACAO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.COMPARACAO.name) or (tipo == EnumValues.COMPARACAO):
                self.log(texto=f'A visualizacao selecionada foi Comparacao.')
                self._painel = Comparacao()

            if (tipo == EnumValues.EXECUCAO.name) or (tipo == EnumValues.EXECUCAO):
                self.log(texto=f'A visualizacao selecionada foi Comparacao.')
                self._painel = Execucao()

            self._necessidade += self._painel.necessidade

    def run(self, contexto) -> Contexto:
        """
        Executa o sorteio desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._painel.name
        self._contexto = super(Visualizacao, self).run(contexto)

        self._painel.contexto = self._contexto
        self._painel.run()

        return self._painel.contexto
