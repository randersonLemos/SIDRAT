from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.modulo.criterio_parada.CriterioParadaPadrao import CriterioParadaPadrao
from src.problema.Solucoes import Solucoes


class IteracoesMaximas(CriterioParadaPadrao):
    """
    Classe destinada para avaliar criterio de parada de simulacoes maximas
    """

    def __init__(self):
        super(IteracoesMaximas, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.CRITERIO_PARADA_ITERACOES] + super(IteracoesMaximas, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._msg = "O Criterio de Parada Máxima Iteracao foi atingido."

        self._solucoes = Solucoes()

    def run(self, contexto: Contexto) -> bool:
        """
        Executa a o criterio de parada para verificar se foi atigindo o número maximo de simulacoes

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o bool [TRUE = excedeu o número máximo de simulações. FALSE = não excedeu o número máximo de simulações]
        :rtype: Bool
        """
        super(IteracoesMaximas, self).run(contexto)

        self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        ultima_iteracao = max(map(int, self._solucoes.solucoes))

        iteracao_convergengia = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_ITERACOES)

        condicao = ultima_iteracao >= iteracao_convergengia

        self.log(texto=f'Quantidade de iterações efetuadas [{ultima_iteracao}] quantidade máxima permitida [{iteracao_convergengia}]')

        if condicao:
            return True
        else:
            return False
