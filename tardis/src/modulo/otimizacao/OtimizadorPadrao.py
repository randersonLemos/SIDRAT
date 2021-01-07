"""
:author: Rafael
:data: 06/12/2019
"""
from abc import ABCMeta

from src.contexto.Contexto import Contexto
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
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._contexto = None
        """
        Todas as informações necessárias
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_TYPE]
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._conjunto_solucoes_inicial = None
        """
        Conjunto com as melhores soluções até agora
        """

        self._solucao_base = None
        """
        Armazena a solução base, solução com os valores defaults presente no dominio
        """

        self._solucoes = None
        """
        Conjunto com todas as soluções presentes e avaliadas.
        """

        self._id = None
        """
        Id (ou identificador) corrente
        """

        self._iteracao = None
        """
        Iteracao corrente
        """

        self._nomes_direcoes_of = None
        """
        Dicionario de nome direcao of
        """

        self._nome_of_mono = None

    def run(self):
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Executando {self._name}")

    def inicializacao(self):
        self.log(texto=f"Inicialização {self._name}")

        self._solucao_base: Solucao = self._contexto.get_atributo(EnumAtributo.SOLUCAO_BASE)
        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)
        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO):
            self._nome_of_mono = self._contexto.get_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, valor_unico_list=True)[0]
        for nome_of in self._nomes_direcoes_of:
            direcao = self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name]
            if self._solucao_base.of is None or nome_of not in self._solucao_base.of:
                self._solucao_base.of = Of(nome_of, direcao=direcao)

        self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        self._iteracao = max(list(self._solucoes.solucoes))
        self._id = max(list(self._solucoes.solucoes[self._iteracao]))

    def before(self):
        self.log(texto=f"Before {self._name}")

    def after(self):
        self.log(texto=f"After {self._name}")

        Exportacao().csv(self._contexto, nome='ultima')
        Exportacao().obejto(self._contexto, nome='ultima')
        LogarMemoria(self._contexto)

    @property
    def contexto(self):
        """
        contexto com todas as informações necessárias
        :return:
        """
        return self._contexto

    @property
    def necessidade(self):
        """
        Defini quais os atributos necessarios para executar o modulo desejado
        """
        return self._necessidade

    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto

