"""
:author: Rafael/Luis
:data: 20/02/2020
"""
from src.modulo.ModuloPadrao import ModuloPadrao
from src.contexto.Contexto import Contexto, EnumAtributo
from src.modulo.criterio_parada.qtd_memoria_usada.QtdMemoriaUsada import QtdMemoriaUsada
from src.modulo.criterio_parada.qtd_solucoes_novas.QtdSolucoesNovas import QtdSolucoesNovas
from src.modulo.criterio_parada.simulacoes_maximas.SimulacoesMaximas import SimulacoesMaximas
from src.contexto.EnumAtributo import EnumValues
from src.modulo.criterio_parada.variacao_fo.VariacaoFO import VariacaoFO
from src.modulo.criterio_parada.iteracoes_maximas.IteracoesMaximas import IteracoesMaximas


class CriterioParada(ModuloPadrao):
    """
    Classe destinada para executar os criterios de parada
    """

    def __init__(self):
        super(CriterioParada, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [] + super(CriterioParada, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._criterios_parada = []

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(CriterioParada, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.CRITERIO_PARADA):
            for criterio in self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA, True):
                if criterio == EnumValues.SIMULACOES_MAX.name:
                    simulacao_max = SimulacoesMaximas()
                    self._necessidade += simulacao_max.necessidade
                    self._criterios_parada.append(simulacao_max)
                if criterio == EnumValues.VARIACAO_OF.name:
                    variacaofo = VariacaoFO()
                    self._necessidade += variacaofo.necessidade
                    self._criterios_parada.append(variacaofo)
                if criterio == EnumValues.ITERACOES_MAX.name:
                    iteracoes_max = IteracoesMaximas()
                    self._necessidade += iteracoes_max.necessidade
                    self._criterios_parada.append(iteracoes_max)
                if criterio == EnumValues.QTD_SOLUCAO_NOVA.name:
                    qtd_solucoes_novas = QtdSolucoesNovas()
                    self._necessidade += qtd_solucoes_novas.necessidade
                    self._criterios_parada.append(qtd_solucoes_novas)
                if criterio == EnumValues.QTD_MEMORIA_USADA_MB.name:
                    qtd_memoria_usada = QtdMemoriaUsada()
                    self._necessidade += qtd_memoria_usada.necessidade
                    self._criterios_parada.append(qtd_memoria_usada)

    def run(self, contexto) -> bool:
        """
        Executa os criterios de paradas desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._contexto = super(CriterioParada, self).run(contexto)

        for criterio_parada in self._criterios_parada:
            if criterio_parada.run(self._contexto):
                self.log(texto=criterio_parada.msg)
                return True

        return False
