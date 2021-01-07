"""
:author: Luis
:data: 21/01/2020
"""
import random

import numpy as np
import pandas as pd

from src.contexto.Contexto import EnumLogStatus
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.modulo.sorteio.SorteioPadrao import SorteioPadrao
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes


class HLDG(SorteioPadrao):
    """
    Classe para construção sorteio de amostras com hiper cubo latino
    """

    def __init__(self):

        super(HLDG, self).__init__()

        self._name = __name__

    def run(self):
        """
        Executa a amostragem com o HLDG
        """
        super(HLDG, self).run()

        self._gera_solucoes()

    def _gera_solucoes(self):
        """
        Gera as solucoes e salva na variavel de classe
        """
        self.log(texto="Gerando Soluções")
        self._solucoes = Solucoes()
        nome_variaveis = self._solucao_referencia.variaveis.get_variaveis_by_tipo(EnumTipoVariaveis.VARIAVEL)
        amostras = []
        for nome_variavel in nome_variaveis:
            probabilidade = self._solucao_referencia.variaveis.get_variavel_by_nome(nome_variavel).dominio.probabilidade
            niveis = self._solucao_referencia.variaveis.get_variavel_by_nome(nome_variavel).dominio.niveis

            if round(sum(probabilidade), 3) != round(1, 3):
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Somatorio das probabilidades diferente de 1')
            amostra = self._gera_amostragem_variaveis(probabilidade, niveis, self._tamanho_populacao)
            amostras.append(amostra)

        amostras = np.array(amostras).T
        amostras = self._checa_duplicidade(amostras)
        solucoes_df = pd.DataFrame(amostras, columns=nome_variaveis.keys())

        for i in range(solucoes_df.shape[0]):

            self._ultimo_id += 1
            solucao = Solucao(id=int(self._ultimo_id), iteracao=int(self._iteracao), solucao=self._solucao_referencia)

            for variavel, valor in zip(solucoes_df.columns, solucoes_df.iloc[i, :]):
                solucao.variaveis.get_variavel_by_nome(variavel).valor = InOut.ajusta_entrada(str(valor))

            #Caso a simulacao ja tenha sido simulada, o avaliador sera responsavel por reutilizar o valor ja simulado
            #Caso nao queira solucoes repetidas, deve ser tratado fora da classe de sorteio
            self._solucoes.add_in_solucoes(solucao)

    def _checa_duplicidade(self, sampled: np.array) -> np.array:
        """
        Chega duplicidade nos sorteios e retona solucoes sem repeticao
        :param sampled: vetor com as variaveis amostradas para cada amostra
        :return sampled_clean: amostragem sem repeticao
        """
        sampled_clean, c = np.unique(sampled, return_counts=True, axis=0)
        return sampled_clean

    def _gera_amostragem_variaveis(self, probs: list, values: list, samples: int) -> list:
        """
        gera amostragem para uma variavel
        :param probs: probabilidade dos niveis das variaveis
        :param values: valor de cada nivel das variaveis
        :param samples: numero de amostras esperado
        :return sampled values: vetor com a amostragem das variaveis
        """
        sampled_values = []
        for prob, value in zip(probs, values):
            sampled_values += round(samples * prob) * [value]

        if len(sampled_values) > 0:
            while len(sampled_values) != samples:
                unicos, n_repeticoes = np.unique(sampled_values, return_counts=True, axis=0)
                c = list(zip(unicos, n_repeticoes))
                random.shuffle(c)
                unicos, n_repeticoes = zip(*c)
                if len(sampled_values) > samples:
                    sampled_values.remove(unicos[np.argmax(n_repeticoes)])
                elif len(sampled_values) < samples:
                    sampled_values += [unicos[np.argmin(n_repeticoes)]]
            random.shuffle(sampled_values)
        return sampled_values
