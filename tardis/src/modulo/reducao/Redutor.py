from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.reducao.RedutorPadrao import RedutorPadrao
from src.modulo.reducao.SimulacaoParcial import SimulacaoParcial


class Redutor(ModuloPadrao):
    """
    Classe destinada para carregar o modulo de redução setado na configuração
    """

    def __init__(self):
        super(Redutor, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_TYPE] + super(Redutor, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._redutor = RedutorPadrao()

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Redutor, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.REDUCAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.REDUCAO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.SIMULACAO_PARCIAL.name) or (tipo == EnumValues.SIMULACAO_PARCIAL):
                self.log(texto=f'O redutor [{EnumValues.SIMULACAO_PARCIAL.name}] foi definido.')
                self._redutor = SimulacaoParcial()

            self._necessidade += self._redutor.necessidade

    def run(self, contexto) -> Contexto:
        """
        Executa o Redutor desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._redutor.name
        self._contexto = super(Redutor, self).run(contexto)

        self._redutor.run(self._contexto)
        return self._redutor.contexto

    def after(self, contexto: Contexto) -> Contexto:
        """
        Executa o after do Redutor desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._redutor.name
        self._contexto = super(Redutor, self).after(contexto)

        self._redutor.after(self._contexto)
        return self._redutor.contexto
