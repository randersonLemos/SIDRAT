"""
:author: Rafael
:data: 17/08/2020
"""
import copy
import math
import random

from src.contexto.Contexto import Contexto, EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin import Loggin
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.problema.Solucao import Solucao


class FonteAlimento:
    def __init__(self, iteracao, id, direcao=EnumValues.MAX.name):
        self._id = id
        self._iteracao = iteracao
        self._direcao = direcao
        self._direcao_of = 1
        if self._direcao in EnumValues.MIN.name:
            self._direcao_of = -1

        self._of = self._direcao_of * float('inf')
        self._fitness = self._calcular_fitness(self._of)
        self._probabilidade = 0
        self._trial = 0
        self._nova_fonte_alimento = None

    @property
    def id(self):
        return self._id

    @property
    def iteracao(self):
        return self._iteracao

    @property
    def nova_fonte_alimento(self):
        return self._nova_fonte_alimento

    @nova_fonte_alimento.setter
    def nova_fonte_alimento(self, nova_fonte_alimento):
        self._nova_fonte_alimento = nova_fonte_alimento

    @property
    def trial(self):
        return self._trial

    @trial.setter
    def trial(self, trial):
        self._trial = trial

    def _calcular_fitness(self, of):
        fitness = 0

        try:
            if of >= 0:
                fitness = 1 / (1 + of)
            else:
                fitness = 1 + abs(of)
        except Exception as ex:
            Loggin.log(tipo=EnumLogStatus.WARN, texto=f'A função objetivo é não numérico [{of}]', info_ex=str(ex))
            of = self._direcao_of * float('-inf')
            if of >= 0:
                fitness = 1 / (1 + of)
            else:
                fitness = 1 + abs(of)

        return fitness

    @property
    def of(self):
        return self._of

    @of.setter
    def of(self, of):
        self._of = of
        self._fitness = self._calcular_fitness(of)

    @property
    def fitness(self):
        return self._fitness

    @property
    def probabilidade(self):
        return self._probabilidade

    def calcula_probabilidade(self, fits):
        self._probabilidade = 0.9 * (self._fitness / max(fits)) + 0.1


class ABC(OtimizadorPadrao):
    """
    Implementação do algoritmo de otimização ABC - Artificial Bee Colony Algorithm
    segue referencias usadas:
        https://abc.erciyes.edu.tr/publ.htm [ref:1]
        http://www.scholarpedia.org/article/Artificial_bee_colony_algorithm [ref:2]
        https://www.youtube.com/watch?v=U9ah51wjvgo [ref:3]
        https://www.youtube.com/watch?v=MAhlPwK4_fI [ref:4]
        https://www.youtube.com/watch?v=2Huy72h7Y20&t=1996s [ref:5]
    """

    def __init__(self):
        super(ABC, self).__init__()

        self._fontes_alimento = []
        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_ABC_FONTE_ALIMENTO] + super(ABC, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._qtd_fonte_alimento = 0
        self._lista_variaveis = []
        self._melhor_fitness = float('-inf')
        self._avaliacao = None
        self._criterio = None
        self._trial_limit = 0
        self._existe_solucao_avaliar = False
        self._ultima_iteracao = -1
        self._direcao = EnumValues.MAX.name

    def inicializacao(self):
        super(ABC, self).inicializacao()

        random.seed(self._contexto.get_atributo(EnumAtributo.RANDOM_SEED))

        self._avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
        self._criterio = self._contexto.get_modulo(EnumModulo.CRITERIOPARADA)

        self._qtd_fonte_alimento = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_ABC_FONTE_ALIMENTO)

        variaveis = copy.deepcopy(self._solucao_base.get_variavies_by_tipo())
        for nome_var in variaveis:
            self._lista_variaveis.append(nome_var)

        self._trial_limit = int((int(self._qtd_fonte_alimento/2) + len(self._lista_variaveis))/1.5)

        if self._contexto.tem_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_FONTE_ALIMENTO):
            self._fontes_alimento = self._contexto.get_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_FONTE_ALIMENTO)

        if self._contexto.tem_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_ULTIMA_ITERACAO):
            self._ultima_iteracao = self._contexto.get_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_ULTIMA_ITERACAO)

        self._direcao = self._nomes_direcoes_of[self._nome_of_mono][EnumValues.DIRECAO.name]
        if self._direcao in EnumValues.MIN.name:
            self._melhor_fitness = -1 * self._melhor_fitness

    def run(self):
        """
        Executa a otimizacao usando o método MCC.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o contexto atualizado
        :rtype: Contexto
        """
        super(ABC, self).run()

        self._iniciar_fonte_alimento()
        self._tratar_fonte_alimento()
        self._salvar()

        while not self._criterio.run(self._contexto):
            self._employ_bees()
            self._avaliar()
            self._tratar_nova_fonte_alimento()
            self._salvar()

            if not self._exite_probabilidade_diferente_1():
                self.log(texto=f'Fim da execução do {self._name}')
                return
            self._onlooker_bees()
            self._avaliar()
            self._tratar_nova_fonte_alimento()
            self._salvar()

            self._scout_bees()
            if self._existe_solucao_avaliar:
                self._avaliar()
                self._tratar_fonte_alimento()
                self._salvar()

        self.log(texto=f'Fim da execução do {self._name}')

    def _iniciar_fonte_alimento(self):
        self.log(tipo=EnumLogStatus.INFO, texto='Iniciando as fonte de alimento.')
        self._existe_solucao_avaliar = False

        # resume de um otimizador diferente
        if self._iteracao > 1 and self._iteracao != self._ultima_iteracao:
            self._fontes_alimento = []
            solucoes_melhores = self._solucoes.conjunto_melhores_solucoes(quantidade=self._qtd_fonte_alimento, nome_of_mono=self._nome_of_mono).solucoes
            for iteracao in solucoes_melhores:
                for id in solucoes_melhores[iteracao]:
                    fonte_alimento = FonteAlimento(iteracao, id, solucoes_melhores[iteracao][id].of[self._nome_of_mono].direcao)
                    fonte_alimento.of = solucoes_melhores[iteracao][id].of[self._nome_of_mono].valor
                    self._fontes_alimento.append(fonte_alimento)

        # resume do ABC
        if self._iteracao > 1 and self._iteracao == self._ultima_iteracao:
            qtd_solucoes_melhores = self._qtd_fonte_alimento - len(self._fontes_alimento)
            solucoes_melhores = self._solucoes.conjunto_melhores_solucoes(quantidade=qtd_solucoes_melhores, nome_of_mono=self._nome_of_mono).solucoes
            for iteracao in solucoes_melhores:
                for id in solucoes_melhores[iteracao]:
                    fonte_alimento = FonteAlimento(iteracao, id, solucoes_melhores[iteracao][id].of[self._nome_of_mono].direcao)
                    fonte_alimento.of = solucoes_melhores[iteracao][id].of[self._nome_of_mono].valor
                    self._fontes_alimento.append(fonte_alimento)

        # default
        if self._qtd_fonte_alimento != len(self._fontes_alimento):
            self._iteracao += 1
            while self._qtd_fonte_alimento > len(self._fontes_alimento):
                self._id += 1
                solucao = Solucao(iteracao=self._iteracao, id=self._id, solucao=self._solucao_base)
                solucao.geral = '[ABC][Aleatorio][Inicio]'

                variaveis = copy.deepcopy(solucao.get_variavies_by_tipo())
                for nome_var in variaveis:
                    lim_inferior = 0
                    lim_superior = len(variaveis[nome_var].dominio.niveis) - 1
                    posicao = random.randint(lim_inferior, lim_superior)  # ajuste para inteiro, equação [ref:2].5
                    variaveis[nome_var].posicao = posicao
                    solucao.variaveis.set_variavel_posicao_by_nome(variaveis[nome_var].nome, variaveis[nome_var].posicao)

                if self._solucoes.existe_solucao(solucao):
                    self._id -= 1
                else:
                    self._solucoes.add_in_solucoes(solucao)
                    self._fontes_alimento.append(FonteAlimento(solucao.iteracao, solucao.id, solucao.of[self._nome_of_mono].direcao))
                    self._existe_solucao_avaliar = True
                    # self.log(tipo=EnumLogStatus.INFO, texto=solucao.to_string())
            self._avaliar()

    def _employ_bees(self):
        self.log(tipo=EnumLogStatus.INFO, texto=f'Iniciando fase Employ, para iteracao [{self._iteracao + 1}].')
        self._existe_solucao_avaliar = False
        self._iteracao += 1
        index_fc = 0
        while index_fc < self._qtd_fonte_alimento:
            self._id += 1
            solucao_nova = self._nova_solucao(index_fc, self._iteracao, self._id, 'Employ')
            # self.log(texto=f'{solucao_nova.to_string()}')
            self._solucoes.add_in_solucoes(solucao_nova)
            self._existe_solucao_avaliar = True
            self._fontes_alimento[index_fc].nova_fonte_alimento = FonteAlimento(solucao_nova.iteracao, solucao_nova.id, solucao_nova.of[self._nome_of_mono].direcao)
            index_fc += 1

    def _onlooker_bees(self):
        self.log(tipo=EnumLogStatus.INFO, texto=f'Iniciando fase OnLooker, para iteracao [{self._iteracao + 1}].')
        self._existe_solucao_avaliar = False
        self._iteracao += 1
        fontes_alimento = copy.deepcopy(self._fontes_alimento)

        index_fc_selecionada = 0
        index_fc_posicao = 0  # para saber se percorreu todas as fontes
        while index_fc_posicao < self._qtd_fonte_alimento:
            r = random.random()
            fonte_alimento = fontes_alimento[index_fc_selecionada]
            if (r < fonte_alimento.probabilidade and self._direcao in EnumValues.MIN.name) or \
                    (r > fonte_alimento.probabilidade and self._direcao in EnumValues.MAX.name):
                self._id += 1
                self._fontes_alimento[index_fc_posicao] = copy.deepcopy(fonte_alimento)
                self._fontes_alimento[index_fc_posicao].nova_fonte_alimento = None

                solucao_nova = self._nova_solucao(index_fc_selecionada, self._iteracao, self._id, 'OnLooker')
                self._solucoes.add_in_solucoes(solucao_nova)
                self._existe_solucao_avaliar = True
                self._fontes_alimento[index_fc_posicao].nova_fonte_alimento = FonteAlimento(solucao_nova.iteracao, solucao_nova.id, solucao_nova.of[self._nome_of_mono].direcao)
                index_fc_posicao += 1

            index_fc_selecionada += 1
            index_fc_selecionada = index_fc_selecionada % self._qtd_fonte_alimento

    def _scout_bees(self):
        self.log(tipo=EnumLogStatus.INFO, texto=f'Iniciando fase Scout, para iteracao [{self._iteracao + 1}].')
        self._existe_solucao_avaliar = False
        for index_fc in range(len(self._fontes_alimento)):
            if self._fontes_alimento[index_fc].trial > self._trial_limit:
                self.log(texto="Gerando solucao aleatoria...")
                self._id += 1
                self._iteracao += 1
                solucao_nova = self._nova_solucao_aleatoria(index_fc, self._iteracao, self._id, "Scout")
                solucao_nova.geral = "[ABC][SCOUT][Aleatoria]"
                self._solucoes.add_in_solucoes(solucao_nova)
                self._existe_solucao_avaliar = True
                self._fontes_alimento[index_fc] = FonteAlimento(solucao_nova.iteracao, solucao_nova.id, solucao_nova.of[self._nome_of_mono].direcao)

    def _avaliar(self):
        if self._existe_solucao_avaliar:
            self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, self._iteracao, True)
            self._contexto = self._avaliacao.run(self._contexto)

    def _tratar_fonte_alimento(self):
        fitness = []
        for fonte_alimento in self._fontes_alimento:
            if fonte_alimento.iteracao == self._iteracao:
                solucao = self._solucoes.get_solucao_by_iteracao_id(fonte_alimento.iteracao, fonte_alimento.id)
                fonte_alimento.of = solucao.of[self._nome_of_mono].valor
                fitness.append(fonte_alimento.fitness)

        for ii in range(len(self._fontes_alimento)):
            fonte_alimento = self._fontes_alimento[ii]
            if fonte_alimento.iteracao == self._iteracao:
                fonte_alimento.calcula_probabilidade(fitness)

    def _tratar_nova_fonte_alimento(self):
        nova_fonte_alimento = None

        fitness = []
        for fonte_alimento in self._fontes_alimento:
            nova_fonte_alimento = fonte_alimento.nova_fonte_alimento
            if nova_fonte_alimento is not None:
                solucao = self._solucoes.get_solucao_by_iteracao_id(nova_fonte_alimento.iteracao, nova_fonte_alimento.id)
                nova_fonte_alimento.of = solucao.of[self._nome_of_mono].valor
                fitness.append(fonte_alimento.fitness)
            else:
                fonte_alimento.trial += 1

        if len(fitness) > 0:
            for ii in range(len(self._fontes_alimento)):
                fonte_alimento = self._fontes_alimento[ii]
                if nova_fonte_alimento is not None:
                    nova_fonte_alimento = fonte_alimento.nova_fonte_alimento
                    nova_fonte_alimento.calcula_probabilidade(fitness)

                    if (nova_fonte_alimento.fitness > fonte_alimento.fitness and self._direcao in EnumValues.MIN.name) or \
                            (nova_fonte_alimento.fitness <= fonte_alimento.fitness and self._direcao in EnumValues.MAX.name):
                        self._fontes_alimento[ii] = nova_fonte_alimento
                    else:
                        self._fontes_alimento[ii].trial += 1
                        self._fontes_alimento[ii].nova_fonte_alimento = None
                else:
                    self._fontes_alimento[ii].trial += 1

    def _exite_probabilidade_diferente_1(self):
        for ii in range(len(self._fontes_alimento)):
            if self._fontes_alimento[ii].probabilidade < 1:
                return True
        return False

    def _nova_solucao(self, index_fc_selecionada, iteracao, id, prefixo) -> Solucao:
        solucao_fonte = copy.deepcopy(self._solucoes.get_solucao_by_iteracao_id(self._fontes_alimento[index_fc_selecionada].iteracao, self._fontes_alimento[index_fc_selecionada].id))
        solucao_nova = Solucao(iteracao=iteracao, id=id, solucao=solucao_fonte)
        solucao_nova.geral = f'[ABC][Vizinhanca][{prefixo}]'
        try:
            from random import sample
            index_variaveis_sorteio = sample(range(0, len(self._lista_variaveis)), len(self._lista_variaveis))
            index_fonte_alimento_sorteio = sample(range(0, len(self._fontes_alimento)), len(self._fontes_alimento))

            fonte_vizinha_index = index_fonte_alimento_sorteio.pop(0)
            while fonte_vizinha_index == index_fc_selecionada:
                fonte_vizinha_index = index_fonte_alimento_sorteio.pop(0)
            fonte_vizinha = self._fontes_alimento[fonte_vizinha_index]

            contador_existem = 0
            limites_random = 1
            while self._solucoes.existe_solucao(solucao_nova):
                contador_existem += 1
                variavel_modificar = self._lista_variaveis[index_variaveis_sorteio.pop(0)]
                dominio_niveis = len(solucao_nova.get_variavies_by_tipo()[variavel_modificar].dominio.niveis)

                posicao_fonte = solucao_nova.get_variavies_by_tipo()[variavel_modificar].posicao
                posicao_vizinha = self._solucoes.get_solucao_by_iteracao_id(fonte_vizinha.iteracao, fonte_vizinha.id).get_variavies_by_tipo()[variavel_modificar].posicao

                r = random.uniform(-1 * limites_random, limites_random)
                # gera valores entre -1 e 1, equacao [ref:2].6 | estamos gerando entre -2 e 2 para aumentar variabilidade visto que são inteiros
                posicao_nova = max(min(dominio_niveis - 1, math.ceil(posicao_fonte + (posicao_fonte - posicao_vizinha) * r)), 0)
                posicao_antiga = solucao_nova.get_variavies_by_tipo()[variavel_modificar].posicao
                if posicao_antiga == posicao_nova:
                    if posicao_nova == dominio_niveis - 1:
                        posicao_nova += -1
                    elif posicao_nova == 0:
                        posicao_nova += 1
                    else:
                        posicao_nova += random.sample([-1, 1], 1)[0]
                self.log(texto=f'[{variavel_modificar} | {posicao_antiga} > {posicao_nova}]')
                solucao_nova.get_variavies_by_tipo()[variavel_modificar].posicao = posicao_nova
                if limites_random >= 10:
                    break

                if len(index_variaveis_sorteio) <= 0:
                    limites_random += 0.1
                    index_variaveis_sorteio = sample(range(0, len(self._lista_variaveis)), len(self._lista_variaveis))

                    if len(index_fonte_alimento_sorteio) <= 0:
                        index_fonte_alimento_sorteio = sample(range(0, len(self._fontes_alimento)), len(self._fontes_alimento))

                    fonte_vizinha_index = index_fonte_alimento_sorteio.pop(0)
                    while fonte_vizinha_index == index_fc_selecionada:
                        if len(index_fonte_alimento_sorteio) <= 0:
                            index_fonte_alimento_sorteio = sample(range(0, len(self._fontes_alimento)), len(self._fontes_alimento))
                        fonte_vizinha_index = index_fonte_alimento_sorteio.pop(0)

                    fonte_vizinha = self._fontes_alimento[fonte_vizinha_index]

            self.log(texto=f'Tentativas para nova solucao [{contador_existem}] e Limite em [{limites_random:.2f}].')
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto="Erro para obter nova solucao.", info_ex=str(ex))

        return solucao_nova

    def _nova_solucao_aleatoria(self, index_fc, iteracao, id, prefixo):
        solucao = copy.deepcopy(self._solucoes.get_solucao_by_iteracao_id(self._fontes_alimento[index_fc].iteracao,
                                                                          self._fontes_alimento[index_fc].id))
        variaveis = copy.deepcopy(solucao.get_variavies_by_tipo())
        for nome_var in variaveis:
            lim_inferior = 0
            lim_superior = len(variaveis[nome_var].dominio.niveis) - 1
            posicao = random.randint(lim_inferior, lim_superior)  # ajuste para inteiro, equação [ref:2].5
            variaveis[nome_var].posicao = posicao
            solucao.variaveis.set_variavel_posicao_by_nome(variaveis[nome_var].nome, variaveis[nome_var].posicao)

        solucao_nova = Solucao(iteracao=iteracao, id=id, solucao=solucao)
        solucao_nova.geral = f'[ABC][Aleatoria][{prefixo}]'
        return solucao_nova

    def _salvar(self):
        if self._existe_solucao_avaliar:
            self._para_resume()
            Exportacao().csv(self._contexto)
            Exportacao().obejto(self._contexto)
            LogarMemoria(self._contexto)

    def _para_resume(self):
        self.log(texto="Salvando atributos para resume.")
        self._contexto.set_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_FONTE_ALIMENTO, self._fontes_alimento, True)
        self._contexto.set_atributo(EnumAtributo.INTERNO_OTIMIZACAO_ABC_ULTIMA_ITERACAO, self._iteracao, True)
