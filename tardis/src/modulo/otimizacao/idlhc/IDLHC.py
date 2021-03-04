"""
:author: Luis
:data: 21/01/2020
"""

import copy
import traceback

import numpy as np

from src.contexto.Contexto import Contexto, EnumAtributo
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.modulo.EnumModulo import EnumModulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.modulo.sorteio.Sorteio import Sorteio
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes
from src.problema.Variavel import Variavel


class IDLHC(OtimizadorPadrao):
    """
    Algoritmo de otimização IDLHC - Hiper Cubo Latino Discretizado Iterativo.
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        EA = EnumAtributo

        if EA.INICIALIZACAO_DOMINIO not in self._necessidade:
            self._necessidade.append(EA.INICIALIZACAO_DOMINIO)

        if EA.OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO not in self._necessidade:
            self._necessidade.append(EA.OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO)

        if EA.OTIMIZACAO_IDLHC_AMOSTRAS_PDF not in self._necessidade:
            self._necessidade.append(EA.OTIMIZACAO_IDLHC_AMOSTRAS_PDF)

        if EA.PATH_RESULTADO not in self._necessidade:
            self._necessidade.append(EA.PATH_RESULTADO)

        self._variaveis_nome_niveis = {}

        self._tamanho_populacao = None

        self._melhores_solucoes = None

        self._solucao_referencia = None

        self._solucoes_historico = None


    def inicializacao(self):
        super().inicializacao()

        EA = EnumAtributo

        self._solucao_referencia = copy.deepcopy(
            self._contexto.get_atributo(EA.SOLUCAO_BASE)
        )

        self._tamanho_populacao = self._contexto.get_atributo(
            EA.OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO
        )

        self._solucoes_historico = self._solucoes.conjunto_melhores_solucoes(
              quantidade=self._tamanho_populacao
            , nome_of_mono=self._nome_of_mono
        )

        if self._contexto.tem_atributo(EA.OTIMIZACAO_IDLHC_SOLUCAO_HISTORICO):
            solucoes_historico = self._contexto.get_atributo(
                EA.OTIMIZACAO_IDLHC_SOLUCAO_HISTORICO
            )
            if solucoes_historico:
                if self._iteracao == max(solucoes_historico):
                    self._solucoes_historico = solucoes_historico

        self._nome_variaveis = self._solucao_base.variaveis.get_variaveis_by_tipo(
            EnumTipoVariaveis.VARIAVEL
        )

        for nome_variavel in self._nome_variaveis:
            variavel = self._nome_variaveis[nome_variavel]
            niveis = variavel.dominio.niveis
            self._variaveis_nome_niveis[nome_variavel] = niveis


    def run(self):
        """
        Executa otimização usando método IDLHC.
        """
        self.log(texto=f"Executando {self._name}.")

        EM = EnumModulo
        EA = EnumAtributo

        sorteio = self._contexto.get_modulo(EM.SORTEIO)

        criterio = self._contexto.get_modulo(EM.CRITERIOPARADA)

        avaliacao = self._contexto.get_modulo(EM.AVALIACAO)

        primeira_iteracao = True

        while not criterio.run(self._contexto):
            self.log(texto="Iteração {}.".format(self._iteracao + 1))

            if not primeira_iteracao:
                self._atualiza_probabilidades()

            self._iteracao += 1

            sorteio.sorteio.tamanho_populacao = self._tamanho_populacao
            sorteio.sorteio.iteracao = self._iteracao
            sorteio.sorteio.ultimo_id = self._id
            sorteio.sorteio.solucao_referencia = self._solucao_referencia
            sorteio.sorteio.contexto = self._contexto

            try:
                sorteio.sorteio.run()

            except Exception:
                traceback.print_exc()

            self._id = sorteio.sorteio.ultimo_id

            solucoes = sorteio.sorteio.solucoes  # novas soluções

            qtd_solucoes = 0
           
            for iteracao in solucoes.solucoes:
                for index in solucoes.solucoes[iteracao]:
                    qtd_solucoes += 1
                    solucoes.solucoes[iteracao][index].geral += "[IDHLC] "
                    self._solucoes.add_in_solucoes(solucoes.solucoes[iteracao][index])

            # Avaliamos se pelo menos uma das soluções sorteadas se trata
            # de solução nova e se a quantidade de amostras geradas no sorteio
            # é maior que o numero de amostras utilizadas para atualização da PDF
            if qtd_solucoes < self._contexto.get_atributo(
                EA.OTIMIZACAO_IDLHC_AMOSTRAS_PDF
            ):
                self.log(texto='Convergencia foi atingida por perda de variabilidade ' +
                               'das amostras.')
                break

            self._contexto.set_atributo(EA.SORTEIO_SOLUCOES_NOVAS, self._solucoes, True)
            self._contexto.set_atributo(EA.AVALIACAO_ITERACAO_AVALIAR, [self._iteracao], True)
            self._contexto = avaliacao.run(self._contexto)

            for id in self._solucoes.solucoes[self._iteracao]:
                self._solucoes_historico.add_in_solucoes(self._solucoes.solucoes[self._iteracao][id])

            self._para_resume()
            Exportacao().csv(self._contexto)
            Exportacao().objeto(self._contexto)
            LogarMemoria(self._contexto)

            primeira_iteracao = False


        self.log(texto=f'Fim da execução do {self._name}.')


    def _atualiza_probabilidades(self):
        self.log(texto="Atualiza probabilidades.")

        qtd_solucoes_atualizar = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_IDLHC_AMOSTRAS_PDF)

        id_melhores_solucoes = []

        #if primeira_iteracao_idlhc:
        #    dict_solucoes_melhores = self._solucoes_historico.conjunto_melhores_solucoes(
        #        quantidade=qtd_solucoes_atualizar,
        #        nome_of_mono=self._nome_of_mono
        #    )._solucoes

        #else:
        #    dict_solucoes_melhores = self._solucoes_historico.conjunto_melhores_solucoes(
        #        quantidade=qtd_solucoes_atualizar
        #        , nome_of_mono=self._nome_of_mono
        #        , iteracao=self._iteracao
        #    )._solucoes

        dict_solucoes_melhores = self._solucoes_historico.conjunto_melhores_solucoes(
            quantidade=qtd_solucoes_atualizar
            , nome_of_mono=self._nome_of_mono
            , iteracao=self._iteracao
        ).solucoes

        for iteracao in dict_solucoes_melhores:
            for id in dict_solucoes_melhores[iteracao]:
                id_melhores_solucoes.append(id)

        contador_valores = {}
        for nome_variavel in self._nome_variaveis:
            contador_valores[nome_variavel] = []
            for iteracao in self._solucoes_historico.solucoes:
                for _id in id_melhores_solucoes:
                    if _id in self._solucoes_historico.solucoes[iteracao]:
                        contador_valores[nome_variavel].append(
                            self._solucoes_historico.solucoes[iteracao][_id].variaveis.get_variavel_by_nome(
                                nome_variavel).valor)

        novas_probabilidades = {}
        for nome_variavel in self._variaveis_nome_niveis:
            novas_probabilidades[nome_variavel] = []
            for candidato in self._variaveis_nome_niveis[nome_variavel]:
                frequencia_valor_normalizada = round(
                    contador_valores[nome_variavel].count(candidato) / qtd_solucoes_atualizar, 2)
                novas_probabilidades[nome_variavel].append(frequencia_valor_normalizada)

            if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_IDLHC_CORTE_PDF):
                novas_probabilidades[nome_variavel] = self._ajusta_corte_pdf(novas_probabilidades[nome_variavel])

        for variavel in novas_probabilidades:
            restante = round(1 - sum(novas_probabilidades[variavel]), 2)
            for i in range(len((novas_probabilidades)[variavel])):
                if novas_probabilidades[variavel][i] + restante >= 0:
                    novas_probabilidades[variavel][i] = round(restante + novas_probabilidades[variavel][i], 2)
                    break

        for variavel in self._nome_variaveis:
            self._solucao_referencia.variaveis.get_variavel_by_nome(variavel).dominio.probabilidade = \
                    novas_probabilidades[variavel]


    def _ajusta_corte_pdf(self, lista_probabilidades):
        """
        Ajusta a probabilidade. Caso algum nivel tenha probabilidade abaixo do valor de corte definido pelo usuário, ela
        recebe o valor zero, e a probabilidade é redistribuida para os outros niveis. Caso todos os níveis tenham probabilidade
        abaixo do valor de corte, não há alteraçao das probabilidades
        :param lista_probabilidades:
        :return: lista_probabilidades_atualizada
        """

        lista_probabilidades_atualizada = copy.deepcopy(lista_probabilidades)
        np_probabilidades = np.array(lista_probabilidades)
        # Máscara que identifica as probabilidades que estejam abaixo de um valor de corte
        mask_corte_inferior = np_probabilidades <= self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_IDLHC_CORTE_PDF)

        if not all(mask_corte_inferior):
            if any(mask_corte_inferior):
                np_probabilidades[~mask_corte_inferior] = np_probabilidades[
                                                              ~mask_corte_inferior] + \
                                                          sum(np_probabilidades[mask_corte_inferior]) / \
                                                          len(np_probabilidades[~mask_corte_inferior])
                np_probabilidades[mask_corte_inferior] = 0
                lista_probabilidades_atualizada = [float(prob) for prob in list(np_probabilidades)]

        return lista_probabilidades_atualizada


    def _para_resume(self):
        self.log(texto="Salvando atributos para resume.")
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_IDLHC_SOLUCAO_HISTORICO, self._solucoes_historico, True)
        self._contexto.set_atributo(EnumAtributo.SOLUCOES, self._solucoes, True)
