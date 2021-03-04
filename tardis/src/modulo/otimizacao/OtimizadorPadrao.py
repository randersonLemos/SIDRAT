"""
:author: Rafael
:data: 06/12/2019
"""

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumValues, EnumAtributo
from src.contexto.EnumAtributo import EnumValues, EnumAtributo
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin.Loggin import Loggin
from src.problema.Solucao import Solucao, Of
from src.problema.Solucoes import Solucoes


class OtimizadorPadrao(Loggin):
    """
    Classe destinada para a ser o pai de todos os modulos
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._contexto = None

        self._necessidade = [EnumAtributo.OTIMIZACAO_TYPE]

        self._conjunto_solucoes_inicial = None  # Conjunto com as melhores soluções até agora

        self._solucao_base = None  # Armeza solução com os valores defaults presente no domínio

        self._solucoes = None   # Conjunto com todas as soluções presentes e avaliadas

        self._id = None  # Identificador correte

        self._iteracao = None  # Iteração corrente

        self._nomes_direcoes_of = None  # Dicionário com as direções das ofs

        self._nome_of_mono = None  # Nome da of


    def inicializacao(self):
        self.log(texto=f"Inicialização de {self._name}")

        EA = EnumAtributo
        EV = EnumValues

        self._solucao_base = self._contexto.get_atributo(EA.SOLUCAO_BASE)

        self._nomes_direcoes_of = self._contexto.get_atributo(EA.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)

        if self._contexto.tem_atributo(EA.AVALIACAO_OF_NOME_MONO):
            self._nome_of_mono = self._contexto.get_atributo(EA.AVALIACAO_OF_NOME_MONO, valor_unico_list=True)[0]

        for nome_of in self._nomes_direcoes_of:
            direcao = self._nomes_direcoes_of[nome_of][EV.DIRECAO.name]

            if (self._solucao_base.of is None) or (nome_of not in self._solucao_base.of):
                self._solucao_base.of = Of(nome_of, direcao=direcao)

        self._solucoes = self._contexto.get_atributo(EA.SOLUCOES)

        self._iteracao = max(list(self._solucoes.solucoes))

        self._id = max(list(self._solucoes.solucoes[self._iteracao]))


    def before(self):
        self.log(texto=f"Before {self._name}")


    def run(self):
        """
        Executa o inicializador desejado.
        """
        self.log(texto=f"Executando {self._name}")


    def after(self):
        self.log(texto=f"After {self._name}")

        Exportacao().csv(self._contexto, nome='ultima')

        Exportacao().objeto(self._contexto, nome='ultima')

        LogarMemoria(self._contexto)


    @property
    def necessidade(self):
        return self._necessidade


    @property
    def contexto(self):
        return self._contexto


    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto


    def atualiza_contexto(self, contexto):
        self._contexto = contexto
