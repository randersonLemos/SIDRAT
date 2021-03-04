"""
:author: Luis Otavio
:data: 14/07/2020
"""

import copy
import random

import numpy as np

from src.contexto.Contexto import Contexto, EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.problema.Solucao import Solucao


class Tabuseach(OtimizadorPadrao):
    """

    Implementação do algoritmo de otimização MCC - metodo das coordenadas ciclicas
    """

    def __init__(self):

        super(Tabuseach, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_TABUSEARCH_TAMANHO_TABU_LIST,
                             EnumAtributo.OTIMIZACAO_TABUSEARCH_NUMERO_AMOSTRAS] + super(Tabuseach, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._beststrategy = None
        self._tabulist = []
        self._tamanho_populacao = None
        self._tamanho_tabu_list = None
        self._n_variaveis = None
        self._direcao_of = 1

    def inicializacao(self):
        super(Tabuseach, self).inicializacao()

        if self._nomes_direcoes_of[self._nome_of_mono][EnumValues.DIRECAO.name] in EnumValues.MIN.name:
            self._direcao_of = -1
        if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_VARIAVEIS_ITERACAO):
            self._n_variaveis = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_VARIAVEIS_ITERACAO)
        else:
            self._n_variaveis = 1

        if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_BESTSTRATEGY) and \
           self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_TABU_LIST):

            #caso melhor estrategia tabusearch e tabu list ja estejam carregadas, fazemos uma avaliacao se a iteração da melhor estrategia carregada pelo tabu search
            # se trata da ultima iteracao. Caso negativo, se trata de otimizacao com acoplamento
            self._tabulist = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_TABU_LIST)
            ultima_iteracao = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
            if ultima_iteracao == self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_BESTSTRATEGY).iteracao:
                self._beststrategy = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_BESTSTRATEGY)
            else:
                self._beststrategy = self._contexto.get_atributo(EnumAtributo.SOLUCOES).melhor_solucao(nome_of_mono=self._nome_of_mono)
                self._tabulist.append(self._beststrategy.serializacao())

        else:
            #Atribuindo melhor solucao disponivel a beststrategy e a adicionando a lista de tabu que pode estar vazia ou nao, caso venha de solucao de outros otimizadores
            self._beststrategy = self._contexto.get_atributo(EnumAtributo.SOLUCOES).melhor_solucao(nome_of_mono=self._nome_of_mono)
            self._tabulist.append(self._beststrategy.serializacao())

        self._tamanho_populacao = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_NUMERO_AMOSTRAS)
        self._tamanho_tabu_list = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_TAMANHO_TABU_LIST)

    def run(self):
        """
        Executa a otimizacao usando o método Tabu Search.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Tabuseach, self).run()

        criterio = self._contexto.get_modulo(EnumModulo.CRITERIOPARADA)

        while not criterio.run(self._contexto):
            self._iteracao += 1

            neighbors = self._get_neighbors()
            self._run_neighbors(neighbors)

            solucoes_ultima_iteracao = self._contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao([self._iteracao])

            beststrategy_of = self._direcao_of * float('-inf')
            for id_solucao in solucoes_ultima_iteracao[self._iteracao]:
                candidatestrategy = solucoes_ultima_iteracao[self._iteracao][id_solucao]
                if candidatestrategy.has_erro == "" or candidatestrategy.has_erro is None:
                    if candidatestrategy.of_valida():
                        if (self._direcao_of * candidatestrategy.of[self._nome_of_mono].valor) > (self._direcao_of * beststrategy_of):
                            beststrategy = candidatestrategy
                            beststrategy_of = beststrategy.of[self._nome_of_mono].valor

            beststrategy.geral = ''.join([beststrategy.geral] + ['[Melhor]'])

            self._tabulist.append(beststrategy.serializacao())
            if self._tamanho_tabu_list <= len(self._tabulist):
                self._tabulist = self._tabulist[1:]

            self._beststrategy = beststrategy

            self._para_resume()
            Exportacao().csv(self._contexto)
            Exportacao().obejto(self._contexto)
            LogarMemoria(self._contexto)

        self.log(texto=f'Fim da execução do {self._name}')

    def _para_resume(self):
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_TABU_LIST, self._tabulist, sobrescreve=True)
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TABUSEARCH_BESTSTRATEGY, self._beststrategy, sobrescreve=True)

    def _get_neighbors(self) -> list:
        """

        Metodo responsavel por selecionar solucoes vizinhas em relacao a melhor solucao
        :return neighbors:  lista de solucoes vizinhas
        """

        neighbors = []
        for i in range(self._tamanho_populacao):
            candidatestrategy = copy.deepcopy(self._beststrategy)
            variaveis = candidatestrategy.variaveis

            in_tabu_list = True
            # checa se candidado esta em tabulist. caso true repete.
            while in_tabu_list:
                # Ecolhe aleatoriamente uma das variaveis que sera alterada. Esta solucao e uma solucao vizinha a
                # melhor solucao
                nome_variaveis = random.sample(list(variaveis.get_variaveis_by_tipo()), self._n_variaveis)
                for nome_variavel in nome_variaveis:
                    variavel = variaveis.get_variavel_by_nome(nome_variavel)
                    numero_posicoes = len(variavel.dominio.niveis)

                    # checa se posição é invalida, fora dos limites do problema. caso true repete
                    posicao_invalida = True
                    while posicao_invalida:
                        nova_posicao = np.random.choice([-1, 0, 1], p=[0.33, 0.34, 0.33]) + variavel.posicao
                        if (nova_posicao >= 0) and (nova_posicao < numero_posicoes):
                            posicao_invalida = False

                    variavel.posicao = nova_posicao

                if candidatestrategy.serializacao() not in self._tabulist:
                    in_tabu_list = False
                else:
                    self.log(tipo=EnumLogStatus.INFO, texto='Tabu List Utilizado')

            neighbors.append(candidatestrategy)

        return neighbors

    def _run_neighbors(self, neighbors: list):
        """
        Metodo responsavel por simular  as estratégias vizinhas
        :param neighbors:
        """

        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)

        for candidatestrategy in neighbors:
            self._id += 1
            solucao = Solucao(id=int(self._id), iteracao=int(self._iteracao), solucao=candidatestrategy)
            solucao.geral += "[TS]"
            self._solucoes.add_in_solucoes(solucao)

        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [self._iteracao], sobrescreve=True)
        self._contexto = avaliacao.run(self._contexto)

