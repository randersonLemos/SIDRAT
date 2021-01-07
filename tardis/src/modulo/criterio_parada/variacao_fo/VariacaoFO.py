import src.contexto.Contexto
from src.modulo.criterio_parada.CriterioParadaPadrao import CriterioParadaPadrao
from src.problema import Solucoes


class VariacaoFO(CriterioParadaPadrao):
    """
    Classe destinada para avaliar convergia segundo critério de FO máxima encontrada por iteracao
    """

    def __init__(self):
        super(VariacaoFO, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [src.contexto.Contexto.EnumAtributo.CRITERIO_PARADA_VARIACAO_FO] + super(VariacaoFO, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._msg = "O Criterio de Parada Variaçaão da Função Objetivo foi atingido."

    def run(self, contexto: src.contexto.Contexto.Contexto) -> bool:
        """
        Executa a o criterio de parada para verificar se foi atigindo o a variação mínima de FO.
        (FOmaxL[i-2]/FOmaxG + FOmaxL[i-1]/FOmaxG + FOmaxL[i]/FOmaxG) <= variacao
        onde:
            i é a ultima iteracao
            FOmaxL é o valor de maximo FO na iteração expecificada
            FOmaxG é o valor maximo da FO globalmente
            variacao é a variação estipulada pelo usuário

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o bool [TRUE = deve parar. FALSE = não deve parar]
        :rtype: Bool
        """
        super(VariacaoFO, self).run(contexto)

        solucoes: Solucoes = self._contexto.get_atributo(src.contexto.Contexto.EnumAtributo.SOLUCOES)
        delta_convergencia = self._contexto.get_atributo(src.contexto.Contexto.EnumAtributo.CRITERIO_PARADA_VARIACAO_FO)

        iteracao = max(solucoes.solucoes)

        if iteracao < 3:
            return False
        else:
            foMax = solucoes.melhor_solucao().of
            [foMax1, foMax2, foMax3] = [float("-inf")]*3

            for _, solucao in contexto.get_atributo(src.contexto.Contexto.EnumAtributo.SOLUCOES).solucoes[iteracao].items():
                foMax3 = foMax3 if solucao.of < foMax3 else solucao.of

            for _, solucao in contexto.get_atributo(src.contexto.Contexto.EnumAtributo.SOLUCOES).solucoes[iteracao].items():
                foMax2 = foMax2 if solucao.of < foMax3 else solucao.of

            for _, solucao in contexto.get_atributo(src.contexto.Contexto.EnumAtributo.SOLUCOES).solucoes[iteracao - 2].items():
                foMax1 = foMax1 if solucao.of < foMax3 else solucao.of

            variacao_FOmax = abs(1 - foMax/foMax3) + abs(1 - foMax/foMax2) + abs(1 - foMax/foMax1)

            condicao = delta_convergencia > variacao_FOmax

            self.log(texto=f'Valor da variação da of efetuadas [{variacao_FOmax}] valor máximo permitido [{delta_convergencia}]')
            if condicao:
                return False
            else:
                return True
