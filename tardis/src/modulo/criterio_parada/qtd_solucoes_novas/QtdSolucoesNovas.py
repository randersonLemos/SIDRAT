"""
:author: Rafael
:data: 20/02/2020
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.modulo.criterio_parada.CriterioParadaPadrao import CriterioParadaPadrao


class QtdSolucoesNovas(CriterioParadaPadrao):
    """
    Classe destinada para avaliar convergia segundo critério de FO máxima encontrada por iteracao
    """

    def __init__(self):
        super(QtdSolucoesNovas, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.CRITERIO_PARADA_QTD_SOLUCAO_NOVA] + super(QtdSolucoesNovas, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._msg = "O Criterio de Parada Variaçaão da Função Objetivo foi atingido."

    def run(self, contexto: Contexto) -> bool:
        """
        Verificar se a quantidade de novas soluções é maior do que exigido.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o bool [TRUE = deve parar. FALSE = não deve parar]
        :rtype: Bool
        """
        super(QtdSolucoesNovas, self).run(contexto)

        interno_qtd_solucoes_novas = self._contexto.get_atributo(EnumAtributo.INTERNO_CRITERIO_PARADA_QTD_SOLUCAO_NOVA)
        qtd_solucoes_novas = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_QTD_SOLUCAO_NOVA)

        if max(self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes) == 0:
            return False

        if interno_qtd_solucoes_novas > qtd_solucoes_novas:
            return False
        else:
            self.log(texto=f"O critério de parada quantidade de soluções novas para avaliar foi atendido.")
            self.log(texto=f"A quantidade de novas soluções [{interno_qtd_solucoes_novas}], o mínimo permitido é [{qtd_solucoes_novas}]")
            return True
