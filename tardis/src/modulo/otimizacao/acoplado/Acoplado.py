"""
:author: Rafael
:data: 15/09/2020
"""
import copy

from src.contexto.Contexto import Contexto, EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.modulo.EnumModulo import EnumModulo
from src.modulo.Modulo import Modulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao


class Acoplado(OtimizadorPadrao):
    """
    Implementação do algoritmo de otimização MCC - metodo das coordenadas ciclicas
    """

    def __init__(self):
        super(Acoplado, self).__init__()
        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_ACOPLADO_OTIMIZACAO_TYPE,
                             EnumAtributo.OTIMIZACAO_ACOPLADO_SIMULACOES_MAX] + super(Acoplado, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """
        self._lista_otimizadores = None
        self._acoplado_simulacao_max_informado = None
        self._acoplado_simulacao_max = 0
        self._criterio_parada_simulacoes_max = None
        self._criterio_parada = None
        self._index_otimizador = 0

    def inicializacao(self):
        super(Acoplado, self).inicializacao()
        self._lista_otimizadores = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_ACOPLADO_OTIMIZACAO_TYPE)
        self._acoplado_simulacao_max_informado = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_ACOPLADO_SIMULACOES_MAX)
        self._criterio_parada_simulacoes_max = self._acoplado_simulacao_max * len(self._lista_otimizadores)
        if self._contexto.tem_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX):
            self._criterio_parada_simulacoes_max = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX)
        self._criterio_parada = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA)
        self._index_otimizador = 0

    def run(self):
        """
        Executa a otimizacao usando o método MCC.
        """
        super(Acoplado, self).run()
        criterio = self._contexto.get_modulo(EnumModulo.CRITERIOPARADA)

        while not criterio.run(self._contexto):
            self._ajusta_criterio_parada()

            otimizador = self._seleciona_otimizador()
            self._contexto = otimizador.run(self._contexto)

            self._iteracao = max(self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes) + 1

            self._para_resume()
            Exportacao().csv(self._contexto)
            Exportacao().obejto(self._contexto)
            LogarMemoria(self._contexto)

            self._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA, self._criterio_parada, True)
            self._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX, self._criterio_parada_simulacoes_max, True)

        self.log(texto=f'Fim da execução do {__name__}')

    def _seleciona_otimizador(self):
        if self._index_otimizador >= len(self._lista_otimizadores):
            self._index_otimizador -= len(self._lista_otimizadores)

        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TYPE, self._lista_otimizadores[self._index_otimizador], True)
        self._index_otimizador += 1

        from src.modulo.otimizacao.Otimizador import Otimizador
        otimizador: Otimizador = Modulo(Otimizador()).run(self._contexto)

        return otimizador

    def _ajusta_criterio_parada(self):
        if EnumValues.SIMULACOES_MAX.name not in self._criterio_parada:
            aux = copy.deepcopy(self._criterio_parada)
            aux.app(EnumValues.SIMULACOES_MAX)
            self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TYPE, aux, True)
        else:
            self._acoplado_simulacao_max += self._acoplado_simulacao_max_informado
            if self._acoplado_simulacao_max > self._criterio_parada_simulacoes_max:
                self._acoplado_simulacao_max = self._criterio_parada_simulacoes_max

        self._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX, self._acoplado_simulacao_max, True)

    def _para_resume(self):
        self.log(texto="Salvando atributos para resume.")

