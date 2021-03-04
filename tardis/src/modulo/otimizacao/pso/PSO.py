"""
:author: Nome_do_autor
:data: 06/08/2020
"""
from copy import deepcopy

import numpy as np

from src.contexto.Contexto import Contexto, EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.problema.Solucao import Solucao, Of


class PSO(OtimizadorPadrao):
    """
    Isto é um comentário da classe MyClass
    """

    def __init__(self):
        """
        Construtor da classe do PSO
        """
        super(PSO, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_PSO_QTD_POPULACAO] + super(PSO, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._variaveis = None
        self._solucao_referencia: Solucao = None
        self._tamanho_populacao = None
        self._solucoes_historico = {}
        self._populacao = []
        self._gbest = None
        self._w = 0.72
        self._cp = 1.496
        self._cg = 1.496
        self._wdamp = 1
        self._direcao_of = EnumValues.MAX.name

    def inicializacao(self):
        super(PSO, self).inicializacao()
        self._variaveis = self._solucao_base.get_variavies_by_tipo()
        self._tamanho_populacao = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_PSO_QTD_POPULACAO)
        self._direcao_of = self._nomes_direcoes_of[self._nome_of_mono][EnumValues.DIRECAO.name]
        if self._direcao_of in EnumValues.MIN.name:
            self._gbest = {'posicao': None, 'of': float('inf'), 'variavel_nome': None}
        else:
            self._gbest = {'posicao': None, 'of': float('-inf'), 'variavel_nome': None}

        np.random.seed(self._contexto.get_atributo(EnumAtributo.RANDOM_SEED))

        ultima_iteracao_pso = None
        if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_PSO_ULTIMA_ITERACAO):
            ultima_iteracao_pso = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_PSO_ULTIMA_ITERACAO)
        if self._iteracao == 0 or self._iteracao == ultima_iteracao_pso:
            if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_PSO_POPULACAO):
                populacao = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_PSO_POPULACAO)
                if populacao is not None:
                    self._populacao = populacao
            if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_PSO_W):
                self._w = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_PSO_W)
        else:
            self._solucoes_historico = self._solucoes.conjunto_melhores_solucoes(quantidade=self._tamanho_populacao, nome_of_mono=self._nome_of_mono).solucoes

    def run(self):
        """
        Executa o PSO

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o contexto atualizado
        :rtype: Contexto
        """
        super(PSO, self).run()

        exportacao = Exportacao()
        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
        criterio = self._contexto.get_modulo(EnumModulo.CRITERIOPARADA)

        self._iteracao_um(avaliacao, exportacao)

        while not criterio.run(self._contexto):
            self.log(texto=f"Nova iteracao do método")

            for ii in range(self._tamanho_populacao):
                rp = np.random.rand(1)
                rg = np.random.rand(1)
                ld = np.zeros(len(self._variaveis))
                lu = np.zeros(len(self._variaveis))
                for jj in range(len(self._variaveis)):
                    ld[jj] = 0
                    lu[jj] = self._populacao[ii]['variavel'][jj]['lu']-1

                termo_inercia = self._w * self._populacao[ii]['velocidade']
                termo_cognitivo = self._cp * rp * (self._populacao[ii]['best_posicao'] - self._populacao[ii]['posicao'])
                termo_social = self._cg * rg * (self._gbest['posicao'] - self._populacao[ii]['posicao'])

                self._populacao[ii]['velocidade'] = termo_inercia + termo_cognitivo + termo_social

                posicao_atualizada = self._populacao[ii]['posicao'] + self._populacao[ii]['velocidade']
                posicao_atualizada = np.round(posicao_atualizada, 0).astype(int)
                posicao_atualizada = np.maximum(posicao_atualizada, ld)
                posicao_atualizada = np.minimum(posicao_atualizada, lu)
                self._populacao[ii]['posicao'] = np.round(posicao_atualizada, 0).astype(int)

                for vv in range(len(self._populacao[ii]['variavel'])):
                    self._populacao[ii]['variavel'][vv]['posicao'] = self._populacao[ii]['posicao'][vv]

                self._populacao[ii]['of'] = Solucao.of_padrao(direcao=self._direcao_of)
                self._populacao[ii]['id'] = None

            self._w *= self._wdamp

            self._gerar_solucoes_avalia()
            self._avaliar_solucoes(avaliacao)
            self._set_melhores()

            self._para_resume()
            exportacao.csv(self._contexto)
            exportacao.obejto(self._contexto)
            LogarMemoria(self._contexto)

        self.log(texto=f'Fim da execução do {self._name}')

    def _iteracao_um(self, avaliacao, exportacao):
        empty_particle = {
            'posicao': None,
            'velocidade': None,
            'of': None,
            'best_posicao': None,
            'best_of': -1*float('inf'),
            'variavel': None,
            'id': None,
        }

        if len(self._populacao) == 0:
            self._populacao = []
            for ii in range(self._tamanho_populacao):
                self._populacao.append(empty_particle.copy())
                self._populacao[ii]['of'] = Solucao.of_padrao(direcao=self._direcao_of)  # ofFunction(self._populacao[ii]['posicao'])
                self._populacao[ii]['velocidade'] = np.full(len(self._variaveis), self._w)
                self._populacao[ii]['posicao'] = np.zeros(len(self._variaveis))
                self._populacao[ii]['variavel'] = [None] * (len(self._variaveis))
                self._populacao[ii]['best_posicao'] = deepcopy(self._populacao[ii]['posicao'])
                self._populacao[ii]['best_of'] = deepcopy(self._populacao[ii]['of'])

            if len(self._solucoes_historico) > 0:
                self._obtem_variaveis_solucao_historico()
            else:
                self._obtem_variavies_aleatoriamente()

            self._gerar_solucoes_avalia()
            self._avaliar_solucoes(avaliacao)
            self._set_melhores()

            self._para_resume()
            exportacao.csv(self._contexto)
            exportacao.obejto(self._contexto)
            LogarMemoria(self._contexto)
        else:
            self._gbest['posicao'] = deepcopy(self._populacao[0]['posicao'])
            self._gbest['variavel'] = deepcopy(self._populacao[0]['variavel'])
            self._gbest['of'] = deepcopy(self._populacao[0]['of'])
            for ii in range(1, len(self._populacao)):
                if self._populacao[ii]['of'] > self._gbest['of']:
                    self._gbest['posicao'] = deepcopy(self._populacao[ii]['posicao'])
                    self._gbest['variavel'] = deepcopy(self._populacao[ii]['variavel'])
                    self._gbest['of'] = deepcopy(self._populacao[ii]['of'])
            self._set_melhores()

    def _gerar_solucoes_avalia(self):
        self._iteracao += 1
        self.log(texto="Calculando nova populacao.")
        for ii in range(self._tamanho_populacao):
            self._id += 1
            solucao = Solucao(id=self._id, iteracao=self._iteracao, solucao=self._solucao_base)

            for jj in range(len(self._populacao[ii]['posicao'])):
                nome = self._populacao[ii]['variavel'][jj]['nome']
                posicao = self._populacao[ii]['variavel'][jj]['posicao']

                try:
                    solucao.variaveis.set_variavel_posicao_by_nome(nome, posicao)
                except Exception as ex:
                    self.log(tipo=EnumLogStatus.ERRO, texto="Erro ao setar variavel", info_ex=str(ex))
                    solucao.variaveis.set_variavel_posicao_by_nome(nome, 0)

            solucao.geral = "[PSO] "
            self._solucoes.add_in_solucoes(solucao)

            self._populacao[ii]['id'] = solucao.id
            self._populacao[ii]['of'] = Solucao.of_padrao(direcao=self._direcao_of)

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, self._solucoes, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [self._iteracao], True)

    def _avaliar_solucoes(self, avaliacao):
        self._contexto = avaliacao.run(self._contexto)
        self._solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

    def _set_melhores(self):
        direcao_of_valor = 1
        if self._direcao_of in EnumValues.MIN.name:
            direcao_of_valor = -1
        for ii in range(self._tamanho_populacao):
            id = self._populacao[ii]['id']
            solucao: Solucao = self._solucoes.get_solucao_by_iteracao_id(self._iteracao, id)
            self._populacao[ii]['of'] = solucao.of[self._nome_of_mono].valor

            if not solucao.of_valida():
                for of_nome in solucao.of:
                    self._populacao[ii]['of'] = Solucao.of_padrao(direcao=self._direcao_of)
                    self.log(tipo=EnumLogStatus.WARN, texto=f'Solucao com itercao [{solucao.iteracao}] e id [{solucao.id}], esta com of {of_nome} nula. Será atribuido {Solucao.of_padrao(direcao=self._direcao_of)} para of')

            if solucao.has_erro is not None:
                self._populacao[ii]['of'] = Solucao.of_padrao(direcao=self._direcao_of)
                self.log(tipo=EnumLogStatus.WARN, texto=f'Solucao com itercao [{solucao.iteracao}] e id [{solucao.id}], esta com erro [{solucao.has_erro}]. Será atribuido -inf para of')

            if (direcao_of_valor * self._populacao[ii]['of']) > (direcao_of_valor * self._populacao[ii]['best_of']):
                self.log(texto=f"[Melhor LOCAL] [pop:{ii}][it:{self._iteracao}][id:{id}]: of -> [{self._populacao[ii]['best_of']}]>[{self._populacao[ii]['of']}]")
                self._populacao[ii]['best_posicao'] = deepcopy(self._populacao[ii]['posicao'])
                self._populacao[ii]['best_of'] = deepcopy(self._populacao[ii]['of'])

                if (direcao_of_valor * self._populacao[ii]['of']) > (direcao_of_valor * self._gbest['of']):
                    self.log(texto=f"[Melhor GLOBAL] [it:{self._iteracao}][id:{id}]: of -> [{self._gbest['of']}]>[{self._populacao[ii]['of']}]")
                    self._gbest['posicao'] = deepcopy(self._populacao[ii]['posicao'])
                    self._gbest['variavel'] = deepcopy(self._populacao[ii]['variavel'])
                    self._gbest['of'] = deepcopy(self._populacao[ii]['of'])

    def _obtem_variaveis_solucao_historico(self):
        ii = 0
        for iteracao in self._solucoes_historico:
            for id in self._solucoes_historico[iteracao]:
                variaveis = self._solucoes_historico[iteracao][id].variaveis
                vv = 0
                for nome in self._variaveis:
                    variavel = variaveis.get_variavel_by_nome(nome)
                    lu = len(variavel.dominio.niveis)
                    self._populacao[ii]['posicao'][vv] = variavel.posicao
                    self._populacao[ii]['variavel'][vv] = {'nome': nome, 'lu': lu, 'posicao': variavel.posicao}
                    vv += 1
                self._populacao[ii]['best_posicao'] = deepcopy(self._populacao[ii]['posicao'])
                self._populacao[ii]['best_of'] = deepcopy(self._populacao[ii]['of'])
                ii += 1

    def _obtem_variavies_aleatoriamente(self):
        for ii in range(self._tamanho_populacao):
            vv = 0
            for nome in self._variaveis:
                lu = len(self._variaveis[nome].dominio.niveis)
                rand_posicao = np.random.randint(0, high=lu, size=1)

                self._populacao[ii]['posicao'][vv] = int(rand_posicao[0])
                self._populacao[ii]['variavel'][vv] = {'nome': nome, 'lu': lu, 'posicao': int(rand_posicao[0])}

                vv += 1
            self._populacao[ii]['best_posicao'] = deepcopy(self._populacao[ii]['posicao'])
            self._populacao[ii]['best_of'] = deepcopy(self._populacao[ii]['of'])

    def _para_resume(self):
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_PSO_POPULACAO, self._populacao, True)
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_PSO_W, self._w, True)
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_PSO_ULTIMA_ITERACAO, self._iteracao, True)
