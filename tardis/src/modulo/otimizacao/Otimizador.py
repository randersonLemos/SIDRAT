"""
:author: Rafael
:data: 06/12/2019
"""
from src.contexto.EnumAtributo import EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.contexto.Contexto import EnumAtributo, Contexto
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.modulo.otimizacao.abc.ABC import ABC
from src.modulo.otimizacao.idlhc.IDLHC import IDLHC
from src.modulo.otimizacao.mcc.MCC import MCC
from src.modulo.otimizacao.pso.PSO import PSO
from src.modulo.otimizacao.pymoo.Pymoo import Pymoo
from src.modulo.otimizacao.tabusearch.Tabuseach import Tabuseach
from src.modulo.otimizacao.acoplado.Acoplado import Acoplado


class Otimizador(ModuloPadrao):
    """
    Classe destinada para a efetuar a otimizacao
    """

    def __init__(self):
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_TYPE,
                            EnumAtributo.PATH_RESULTADO,
                            EnumAtributo.AVALIACAO_TYPE,
                            EnumAtributo.INICIALIZACAO_DOMINIO] + super(Otimizador, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._modulo = OtimizadorPadrao()

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Otimizador, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.MCC.name) or (tipo == EnumValues.MCC):
                self.log(texto=f"O modulo de inicialização [{EnumValues.MCC.name}] foi definido.")
                self._modulo = MCC()
            elif (tipo == EnumValues.IDLHC.name) or (tipo == EnumValues.IDLHC):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.IDLHC.name}] foi definido.")
                self._modulo = IDLHC()
            elif (tipo == EnumValues.PYMOO_DE.name) or (tipo == EnumValues.PYMOO_DE):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.PYMOO_DE.name}] foi definido.")
                self._modulo = Pymoo()
                self._modulo.otimizador = EnumValues.PYMOO_DE
            elif (tipo == EnumValues.PYMOO_GA.name) or (tipo == EnumValues.PYMOO_GA):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.PYMOO_GA.name}] foi definido.")
                self._modulo = Pymoo()
                self._modulo.otimizador = EnumValues.PYMOO_GA
            elif (tipo == EnumValues.PYMOO_NSGA3.name) or (tipo == EnumValues.PYMOO_NSGA3):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.PYMOO_NSGA3.name}] foi definido.")
                self._modulo = Pymoo()
                self._modulo.otimizador = EnumValues.PYMOO_NSGA3
            elif (tipo == EnumValues.PSO.name) or (tipo == EnumValues.PSO):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.PSO.name}] foi definido.")
                self._modulo = PSO()
            elif (tipo == EnumValues.TABUSEARCH.name) or (tipo == EnumValues.TABUSEARCH):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.TABUSEARCH.name}] foi definido.")
                self._modulo = Tabuseach()
            elif (tipo == EnumValues.ABC.name) or (tipo == EnumValues.ABC):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.ABC.name}] foi definido.")
                self._modulo = ABC()
            elif (tipo == EnumValues.ACOPLADO.name) or (tipo == EnumValues.ACOPLADO):
                self.log(texto=f"O modulo de otimizacao [{EnumValues.ACOPLADO.name}] foi definido.")
                self._modulo = Acoplado()

            self._necessidade += self._modulo.necessidade

    def run(self, contexto) -> Contexto:
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._modulo.name
        self._contexto = super(Otimizador, self).run(contexto)

        self._modulo.contexto = contexto
        self._modulo.inicializacao()
        self._modulo.before()
        self._modulo.run()
        self._modulo.after()

        return self._modulo.contexto
