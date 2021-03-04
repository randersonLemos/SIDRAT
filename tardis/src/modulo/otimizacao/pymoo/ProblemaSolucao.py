"""
:author: rafael
:data: 14/02/2020
"""
# variaveis discreta https://pymoo.org/tutorial/discrete_problem.html
# my sampling        https://pymoo.org/tutorial/custom.html
# ler o resultado    https://pymoo.org/misc/results.html
# my callback        https://pymoo.org/misc/callback.html
# my repair          https://pymoo.org/misc/constraint_handling.html
# visualizacao       https://pymoo.org/visualization/pcp.html
# my problem         https://pymoo.org/problems/custom.html
# criterio de parada https://pymoo.org/misc/termination_criterion.html
import copy

import numpy as np
from pymoo.model.problem import Problem

from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.modulo.EnumModulo import EnumModulo
from src.problema.Solucao import Solucao


class ProblemaSolucao(Problem):

    def __init__(self, n_var, n_obj=1, xl=0, xu=1, contexto=None, otimizador=None, nome_of_mono=None):
        super().__init__(n_var=n_var, n_obj=n_obj, n_constr=1, xl=xl, xu=xu, type_var=np.int)
        self._n_var = n_var
        self._n_obj = n_obj
        self._contexto = contexto
        self._solucoes = contexto.get_atributo(EnumAtributo.SOLUCOES)
        self._otimizador = otimizador
        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)
        if nome_of_mono is not None:
            self._nomes_direcoes_of = {nome_of_mono: self._nomes_direcoes_of[nome_of_mono]}

    @property
    def contexto(self):
        return self._contexto

    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto
        self._solucoes = contexto.get_atributo(EnumAtributo.SOLUCOES)

    def _evaluate(self, x, out, *args, **kwargs):
        if len(kwargs) == 0:
            return

        iteracao_max = max(list(self._solucoes.solucoes))
        iteracao_atual = iteracao_max + 1
        id = max(list(self._solucoes.solucoes[iteracao_max])) + 1

        Loggin().log(arquivo=__name__, tipo=EnumLogStatus.INFO, texto=f"Inicializando o Calculo para geração [{iteracao_atual}]")

        solucao_base: Solucao = self._contexto.get_atributo(EnumAtributo.SOLUCAO_BASE)

        for ii in range(x.shape[0]):
            solucao_nova = Solucao(id, iteracao_atual, solucao_base)
            id += 1
            variavies = solucao_base.get_variavies_by_tipo()
            jj = 0
            for variavel in variavies:
                try:
                    solucao_nova.variaveis.get_variavel_by_nome(variavel).posicao = int(x[ii][jj])
                except ValueError as ex:
                    Loggin().log(arquivo=__name__, texto="Valor for do limite", info_ex=str(ex))

                jj += 1
            solucao_nova.geral = f'[{self._otimizador}]'
            self._solucoes.add_in_solucoes(solucao_nova)

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, self._solucoes, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [iteracao_atual], True)

        Loggin().log(arquivo=__name__, tipo=EnumLogStatus.INFO, texto=f"Iniciando avaliação.")
        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
        self._contexto = avaliacao.run(self._contexto)
        self._solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

        f1 = np.zeros((len(self._solucoes.solucoes[iteracao_atual]), self._n_obj))
        g1 = np.zeros((len(self._solucoes.solucoes[iteracao_atual]), self._n_obj))

        for ii in self._solucoes.solucoes[iteracao_atual]:
            try:
                posicao = ii - list(self._solucoes.solucoes[iteracao_atual])[0]
                n_of = 0
                for nome_of in sorted(self._nomes_direcoes_of):
                    # para minimizar precisa ser -1 o valor padrão.
                    direcao_of_valor = 1
                    if EnumValues.MIN.name in self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name]:
                        direcao_of_valor = -1
                    if self._solucoes.solucoes[iteracao_atual][ii].has_erro is None:
                        f1[posicao][n_of] = -1 * self._solucoes.solucoes[iteracao_atual][ii].of[nome_of].valor * direcao_of_valor
                        g1[posicao][n_of] = -1 * self._solucoes.solucoes[iteracao_atual][ii].of[nome_of].valor * direcao_of_valor
                    else:
                        f1[posicao][n_of] = -1 * Solucao.of_padrao(self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name])
                        g1[posicao][n_of] = -1 * Solucao.of_padrao(self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name])
                    n_of += 1
            except Exception as ex:
                Loggin().log(arquivo=__name__, tipo=EnumLogStatus.ERRO, texto=f"Não foi possivel ler of da solucao [{ii}] geracao [{iteracao_atual}].")

        out["F"] = f1
        out["G"] = g1
        self._salvar()

    def _salvar(self):
        exportacao = Exportacao()
        exportacao.csv(self._contexto)
        exportacao.obejto(self._contexto)
        LogarMemoria(self._contexto)
