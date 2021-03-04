"""
:author: Rafael
:data: 15/10/2020
"""
from copy import deepcopy

import h5py
import numpy as np

from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.InOut import InOut
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.problema.Solucao import Of, Solucao


class CalculaOfProducao(Loggin):
    """
    Classe destinada a ler os resultados
    """

    def __init__(self, contexto):
        """
        Comentário do construtor
        """
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._contexto = contexto
        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)
        self._solucoes = None

    def run(self, buffer, solucoes):
        """

        :param buffer:
        :type buffer:
        :param solucoes:
        :type solucoes:
        :return:
        :rtype:
        """
        self._solucoes = solucoes
        if EnumValues.WP.name in self._nomes_direcoes_of or\
                EnumValues.NP.name in self._nomes_direcoes_of or\
                EnumValues.WI.name in self._nomes_direcoes_of or\
                EnumValues.GI.name in self._nomes_direcoes_of:
            self._ler_dados_producao(buffer)

        return self._solucoes

    def _ler_dados_producao(self, buffer):
        unipro = buffer['unipro']
        if len(unipro) == 0:
            return

        keys = deepcopy(list(unipro.keys()))

        self.log(texto=f'Ler dados producao')
        try:
            keys = deepcopy(list(unipro.keys()))
            for ii in range(len(keys)):
                prefixo = keys[ii]
                iteracao = unipro[prefixo]['iteracao']
                id = unipro[prefixo]['id']
                path = unipro[prefixo]['path']
                path_file = InOut.ajuste_path(f'{path}.unipro')
                file_unipro = h5py.File(path_file)

                if EnumValues.WP.name in self._nomes_direcoes_of:
                    self._set_of(iteracao=iteracao, id=id, file_unipro=file_unipro, nome_of=EnumValues.WP.name)
                if EnumValues.NP.name in self._nomes_direcoes_of:
                    self._set_of(iteracao=iteracao, id=id, file_unipro=file_unipro, nome_of=EnumValues.NP.name)
                if EnumValues.WI.name in self._nomes_direcoes_of:
                    self._set_of(iteracao=iteracao, id=id, file_unipro=file_unipro, nome_of=EnumValues.WI.name)
                if EnumValues.GI.name in self._nomes_direcoes_of:
                    self._set_of(iteracao=iteracao, id=id, file_unipro=file_unipro, nome_of=EnumValues.GI.name)

        except Exception as ex:
            for ii in range(len(keys)):
                prefixo = keys[ii]
                iteracao = unipro[prefixo]['iteracao']
                id = unipro[prefixo]['id']
                self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao obter dados de produção da solucao iteracao [{iteracao}], e id [{id}]', info_ex=str(ex))
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'OBTER_OF_PROD'
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[EnumValues.NP.name].valor = Solucao.of_padrao(self._nomes_direcoes_of[EnumValues.NP.name][EnumValues.DIRECAO.name])
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[EnumValues.WP.name].valor = Solucao.of_padrao(self._nomes_direcoes_of[EnumValues.WP.name][EnumValues.DIRECAO.name])
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[EnumValues.WP.name].valor = Solucao.of_padrao(self._nomes_direcoes_of[EnumValues.WI.name][EnumValues.DIRECAO.name])
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[EnumValues.WP.name].valor = Solucao.of_padrao(self._nomes_direcoes_of[EnumValues.GI.name][EnumValues.DIRECAO.name])

    def _set_of(self, iteracao, id, file_unipro, nome_of):
        try:
            tempo, valor_of = self._ler_serie_field_unipro(file_unipro, nome_of)
            self.log(texto=f'Solucao iteracao [{iteracao}], e id [{id}] tem OF [{nome_of}] no valor de [{valor_of}] e tempo [{tempo}]')
            self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = valor_of
            self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).set_avaliada()
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao obter dados de {nome_of} da solucao iteracao [{iteracao}], e id [{id}]', info_ex=str(ex))
            self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'OBTER_{nome_of}'
            self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = Solucao.of_padrao(self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name])

    def _ler_serie_field_unipro(self, unipro, serie):
        valor_of = 0
        tempo = 0
        for timevalue in np.array(unipro['Field'][serie])[:, :]:
            if tempo < int(timevalue[0][0]):
                tempo = int(timevalue[0][0])
                valor_of = timevalue[1][0]
        return tempo, valor_of
