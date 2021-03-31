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
    Classe destinada para efetuar a otimizacao
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        EA = EnumAtributo

        if EnumAtributo.OTIMIZACAO_TYPE not in self._necessidade:
            self._necessidade.append(EA.OTIMIZACAO_TYPE)

        if EnumAtributo.PATH_RESULTADO not in self._necessidade:
            self._necessidade.append(EA.PATH_RESULTADO)
        
        if EnumAtributo.AVALIACAO_TYPE not in self._necessidade:
            self._necessidade.append(EA.AVALIACAO_TYPE)
        
        if EnumAtributo.INICIALIZACAO_DOMINIO not in self._necessidade:
            self._necessidade.append(EA.INICIALIZACAO_DOMINIO)

        self._otimizador = OtimizadorPadrao()


    def carrega(self, contexto):
        """
        Método para obter o otimizador selecionado.

        :param  Contexto contexto: objeto que carrega todas as informações
        """
        self.log(texto=f"Carregando o {self._name}")

        self._contexto = contexto

        EA = EnumAtributo
        EV = EnumValues

        if self._contexto.tem_atributo(EA.OTIMIZACAO_TYPE):
            tipo = self._contexto.get_atributo(EA.OTIMIZACAO_TYPE)

            if isinstance(tipo, str):
                tipo = tipo.upper()

            if (tipo == EV.MCC.name) or (tipo == EV.MCC):
                self.log(texto=f"O modulo de inicialização [{EV.MCC.name}] foi definido.")
                self._otimizador = MCC()

            elif (tipo == EV.IDLHC.name) or (tipo == EV.IDLHC):
                self.log(texto=f"O modulo de otimizacao [{EV.IDLHC.name}] foi definido.")
                self._otimizador = IDLHC()

            elif (tipo == EV.PYMOO_DE.name) or (tipo == EV.PYMOO_DE):
                self.log(texto=f"O modulo de otimizacao [{EV.PYMOO_DE.name}] foi definido.")
                self._otimizador = Pymoo()
                self._otimizador.otimizador = EV.PYMOO_DE

            elif (tipo == EV.PYMOO_GA.name) or (tipo == EV.PYMOO_GA):
                self.log(texto=f"O modulo de otimizacao [{EV.PYMOO_GA.name}] foi definido.")
                self._otimizador = Pymoo()
                self._otimizador.otimizador = EV.PYMOO_GA

            elif (tipo == EV.PYMOO_NSGA3.name) or (tipo == EV.PYMOO_NSGA3):
                self.log(texto=f"O modulo de otimizacao [{EV.PYMOO_NSGA3.name}] foi definido.")
                self._otimizador = Pymoo()
                self._otimizador.otimizador = EV.PYMOO_NSGA3

            elif (tipo == EV.PSO.name) or (tipo == EV.PSO):
                self.log(texto=f"O modulo de otimizacao [{EV.PSO.name}] foi definido.")
                self._otimizador = PSO()

            elif (tipo == EV.TABUSEARCH.name) or (tipo == EV.TABUSEARCH):
                self.log(texto=f"O modulo de otimizacao [{EV.TABUSEARCH.name}] foi definido.")
                self._otimizador = Tabuseach()

            elif (tipo == EV.ABC.name) or (tipo == EV.ABC):
                self.log(texto=f"O modulo de otimizacao [{EV.ABC.name}] foi definido.")
                self._otimizador = ABC()

            elif (tipo == EV.ACOPLADO.name) or (tipo == EV.ACOPLADO):
                self.log(texto=f"O modulo de otimizacao [{EV.ACOPLADO.name}] foi definido.")
                self._otimizador = Acoplado()

            for necessidade in self._otimizador._necessidade:
                if necessidade not in self._necessidade:
                    self._necessidade.append(necessidade)


    def run(self, contexto) -> Contexto:
        """
        Executa o inicializador desejado.

        :param  Contexto contexto: objeto que carrega todas as informações
        :return Contexto contexto: objeto que carrega todas as informações
        """
        self.log(texto=f'Executando o {self._name}')

        self._contexto = contexto

        self._otimizador._contexto = contexto

        self._otimizador.inicializacao()

        self._otimizador.before()

        self._otimizador.run()

        self._otimizador.after()

        return self._otimizador.contexto
