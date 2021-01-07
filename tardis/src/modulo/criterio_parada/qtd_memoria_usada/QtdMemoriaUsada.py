"""
:author: Rafael
:data: 20/10/2020
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.LogarMemoria import LogarMemoria
from src.modulo.criterio_parada.CriterioParadaPadrao import CriterioParadaPadrao


class QtdMemoriaUsada(CriterioParadaPadrao):
    """
    Classe destinada para avaliar convergia segundo critério de FO máxima encontrada por iteracao
    """

    def __init__(self):
        super(QtdMemoriaUsada, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.CRITERIO_PARADA_QTD_MEMORIA_USADA_MB] + super(QtdMemoriaUsada, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._msg = "O Criterio de Parada Quantidade de memória usada foi atingido."

    def run(self, contexto: Contexto) -> bool:
        """
        Verificar se a quantidade de novas soluções é maior do que exigido.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o bool [TRUE = deve parar. FALSE = não deve parar]
        :rtype: Bool
        """
        super(QtdMemoriaUsada, self).run(contexto)

        qtd_memoria_usada_criterio = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_QTD_MEMORIA_USADA_MB)
        qtd_memoria_usada_real = LogarMemoria(self._contexto)

        if qtd_memoria_usada_criterio > qtd_memoria_usada_real:
            return False
        else:
            self.log(texto=f"O critério de parada quantidade de memória usada foi atendido.")
            self.log(texto=f"A quantidade de memória usada é [{qtd_memoria_usada_real}], o máximo permitido é [{qtd_memoria_usada_criterio}]")
            return True
