from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.modulo.criterio_parada.CriterioParadaPadrao import CriterioParadaPadrao


class SimulacoesMaximas(CriterioParadaPadrao):
    """
    Classe destinada para avaliar criterio de parada de simulacoes maximas
    """

    def __init__(self):
        super(SimulacoesMaximas, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX] + super(SimulacoesMaximas, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._msg = "O Criterio de Parada Simulação Máxima foi atingido."

    def run(self, contexto: Contexto) -> bool:
        """
        Executa a o criterio de parada para verificar se foi atigindo o número maximo de simulacoes

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o bool [TRUE = excedeu o número máximo de simulações. FALSE = não excedeu o número máximo de simulações]
        :rtype: Bool
        """
        super(SimulacoesMaximas, self).run(contexto)

        if self._contexto.tem_atributo(EnumAtributo.QTD_SOLUCES_AVALIADAS):
            qtd_avaliacao = self._contexto.get_atributo(EnumAtributo.QTD_SOLUCES_AVALIADAS)
        else:
            qtd_avaliacao = 0
        max_avaliacoes = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX)

        self.log(texto=f'Quantidade de avaliações efetuadas [{qtd_avaliacao}] quantidade máxima permitida [{max_avaliacoes}]')
        return qtd_avaliacao >= max_avaliacoes


