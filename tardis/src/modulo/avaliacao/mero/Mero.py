"""
:author: Rafael
:data: 16/12/2019
"""
import os
import re

import numpy as np

import src.modulo.problemas_fechados.campo_namorado_numero_pocos.base
import src.modulo.problemas_fechados.campo_namorado_posicionamento.base
import src.modulo.problemas_fechados.funcoes_teste.base
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.CSV import CSV
from src.inout.Copy import Copy
from src.inout.InOut import InOut
from src.inout.Remocao import Remocao
from src.inout.TXT import TXT
from src.loggin.Enum import EnumLogStatus
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.modulo.avaliacao.Resgate import Resgate
from src.modulo.avaliacao.mero.DSGU import DSGU
from src.modulo.avaliacao.mero.GEP import GEP
from src.modulo.avaliacao.mero.GEVT import GEVT
from src.modulo.avaliacao.mero.Processamento import Processamento
from src.modulo.avaliacao.multi_objetivo.MultiObjetivo import MultiObjetivo
from src.problema.Solucoes import Solucoes


class Mero(AvaliadorPadrao):
    """
        Classe destinada a organizar efetua a execução do MERO, e todas suas ferramentas.
    """

    def __init__(self):
        super(Mero, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_MERO_EXECUTAVEL,
                             EnumAtributo.SIMULADOR_NOME,
                             EnumAtributo.SIMULADOR_VERSAO,
                             EnumAtributo.PATH_SIMULACAO,
                             EnumAtributo.PATH_RESULTADO,
                             EnumAtributo.AVALIACAO_TYPE,
                             EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE,
                             EnumAtributo.AVALIACAO_MERO_UNIMAP_PATH,
                             EnumAtributo.AVALIACAO_MERO_UNIECO_PATH,
                             EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE] + super(Mero, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._dsgu = None

    def run(self):
        super(Mero, self).run()

        self._preparar_arquivos()

        # self._fake_of()
        # return

        gevt = GEVT()
        self._contexto = gevt.run(self._contexto)

        gep = GEP()
        self._contexto = gep.run(self._contexto)

        self._dsgu = DSGU()
        self._contexto = self._dsgu.run(self._contexto)

        processamento = Processamento()
        self._contexto = processamento.run(self._contexto)

    def _fake_of(self):
        try:
            iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
            solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao_para_avaliar(iteracoes)

            for iteracao in iteracoes:
                if iteracao in solucoes:
                    for k_id in solucoes[iteracao]:
                        from random import random
                        for nome_of in self._nomes_direcoes_of:
                            if EnumValues.MULTIOBJETIVO.name not in nome_of:
                                valor = random() * 1000000000
                                solucoes[iteracao][k_id].of[nome_of].valor = valor

        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, info_ex=str(ex))

    def before(self):
        super(Mero, self).before()

        self._setar_variavel_ambiente()
        self._obter_solucoes_existentes()

    def after(self):
        super(Mero, self).after()

        self._contexto = Resgate().melhores(self._contexto)
        if self._dsgu is not None:
            self._dsgu.finalizar_thread()
        self._avaliar_funcao_multi_objetivo()

        self._salvar_solucoes_avaliadas()

        remocao = Remocao()
        remocao.run(self._contexto)

    def _avaliar_funcao_multi_objetivo(self):
        if self._nome_of_mono is not None:
            multi_objetivo = MultiObjetivo()
            multi_objetivo.contexto = self._contexto
            multi_objetivo.before()
            multi_objetivo.run()
            multi_objetivo.after()
            self._contexto = multi_objetivo.contexto

    def _preparar_arquivos(self):
        path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        path_simulacao = self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)
        gevts_template_executar = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)

        for prefixo in gevts_template_executar.keys():
            path_completo_origem = InOut.ajuste_path(f'{path_projeto}/{gevts_template_executar[prefixo]["gevt_path"]}')
            path_completo_destino = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{gevts_template_executar[prefixo]["gevt_file_name"]}.mero')

            if not Copy.copy_file(path_completo_origem, path_completo_destino):
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Erro no GEVT.')

    def _obter_solucoes_existentes(self):
        try:
            caminho_solucoes_existentes = self._get_caminho_solucoes_existentes()
            if caminho_solucoes_existentes is not None:
                df_solucoes = CSV().ler(str(caminho_solucoes_existentes), index_col=False)
                colunas = list(df_solucoes.columns)

                iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
                solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao_para_avaliar(iteracoes)
                for it in solucoes:
                    for id in solucoes[it]:
                        serie_of = df_solucoes[df_solucoes.serializacao == solucoes[it][id].serializacao()].serializacao
                        if serie_of.shape[0] > 0:
                            try:
                                for coluna in colunas:
                                    of_nome = coluna.replace('of', '').replace(']', '').replace('[', '')
                                    if of_nome in solucoes[it][id].of and of_nome != 'serializacao':
                                        self.log(texto=f"Lendo da base de dados - {caminho_solucoes_existentes}")
                                        valor_of = df_solucoes[df_solucoes.serializacao == solucoes[it][id].serializacao()][coluna].iloc[0]
                                        if str(valor_of).upper() != "NAN" and \
                                            str(valor_of).upper() != "NONE" and \
                                            str(valor_of).upper() != "-INF" and \
                                            str(valor_of).upper() != 'INF:':

                                            solucoes[it][id].of[of_nome].valor = valor_of
                                            solucoes[it][id].set_avaliada()
                                            if not re.search('REPETIDA', solucoes[it][id].geral, re.IGNORECASE):
                                                solucoes[it][id].geral += f'[REPETIDA|it:BD|id:BD]'
                            except Exception as ex:
                                self.log(tipo=EnumLogStatus.ERRO, texto=f"Erro ao obter solução já existente na base de dados.", info_ex=str(ex))
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f"Erro ao obter solução já existente.", info_ex=str(ex))

    def _salvar_solucoes_avaliadas(self):
        try:
            caminho_solucoes_existentes = self._get_caminho_solucoes_existentes()
            if caminho_solucoes_existentes is not None:
                df_solucoes = CSV().ler(str(caminho_solucoes_existentes), index_col=False)

                tem_nova_coluna = False
                for nome_of in self._nomes_direcoes_of:
                    if str(f'of[{nome_of.upper()}]') not in list(df_solucoes.columns.values):
                        coluna_df = str(f'of[{nome_of.upper()}]')
                        df_solucoes[coluna_df] = None
                        tem_nova_coluna = True

                colunas_df = list(df_solucoes.columns.values)
                iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
                solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao(iteracoes)

                if tem_nova_coluna:
                    for it in solucoes:
                        for id in solucoes[it]:
                            if solucoes[it][id].has_erro is None or solucoes[it][id].has_erro == "":
                                if solucoes[it][id].avaliada:
                                    serializacao = solucoes[it][id].serializacao()
                                    serie = df_solucoes[df_solucoes['serializacao'] == serializacao].serializacao
                                    if serie.shape[0] <= 0:
                                        index = df_solucoes.shape[0]
                                        zeros = np.zeros((len(df_solucoes.columns)))
                                        df_solucoes.loc[index] = zeros
                                        df_solucoes.loc[index, 'serializacao'] = serializacao

                                    for coluna_df in colunas_df[1:]:
                                        of_nome = coluna_df.replace('of', '').replace(']', '').replace('[', '')
                                        if of_nome in solucoes[it][id].of:
                                            df_solucoes.loc[df_solucoes['serializacao'] == serializacao, coluna_df] = solucoes[it][id].of[of_nome].valor
                                        else:
                                            if colunas_df != 'serializacao':
                                                df_solucoes.loc[df_solucoes['serializacao'] == serializacao, coluna_df] = ""
                    str_solucoes_salvar = df_solucoes.to_csv(sep=';', index=False).replace('\r', '')

                    TXT().salvar(str(caminho_solucoes_existentes), str_solucoes_salvar, "+w")
                else:
                    str_solucoes_salvar = ""
                    for it in solucoes:
                        for id in solucoes[it]:
                            if solucoes[it][id].has_erro is None or solucoes[it][id].has_erro == "":
                                if solucoes[it][id].avaliada:
                                    serializacao = solucoes[it][id].serializacao()
                                    serie = df_solucoes[df_solucoes['serializacao'] == serializacao].serializacao
                                    if serie.shape[0] <= 0:
                                        str_solucoes_salvar += f'{solucoes[it][id].serializacao()};'
                                        for coluna_df in colunas_df:
                                            nome_of = coluna_df.replace('of[', '').replace(']', '')
                                            if nome_of in solucoes[it][id].of:
                                                str_solucoes_salvar += f"{solucoes[it][id].of[nome_of].valor};"
                                            else:
                                                if nome_of != 'serializacao':
                                                    str_solucoes_salvar += f";"
                                        str_solucoes_salvar = str_solucoes_salvar[:-1] + '\n'
                    if len(str_solucoes_salvar) > 0:
                        TXT().salvar(str(caminho_solucoes_existentes), str_solucoes_salvar, "+a")
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto='Erro ao salvar em arquivo', info_ex=str(ex))

    def _get_caminho_solucoes_existentes(self) -> object:
        if str(self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)).upper() == EnumValues.CAMPO_NAMORADO_POSICIONAMENTO.name:
            folder_data_base = os.path.dirname(src.modulo.problemas_fechados.campo_namorado_posicionamento.base.__file__)
            return os.path.join(folder_data_base, f'{EnumValues.AVALIACAO_CAMPO_NAMORADO_POSIC_SOLUCOES.name}.csv')
        elif str(self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)).upper() == EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name:
            folder_data_base = os.path.dirname(src.modulo.problemas_fechados.campo_namorado_numero_pocos.base.__file__)
            return os.path.join(folder_data_base, f'{EnumValues.AVALIACAO_CAMPO_NAMORADO_NUM_SOLUCOES.name}.csv')
        return None

    def _setar_variavel_ambiente(self):
        try:
            computername = os.environ.get(EnumValues.COMPUTERNAME.name, '')
            if computername != "":
                mero_lic = os.environ.get(EnumValues.MERO_LIC.name, '')
                if mero_lic != '':
                    self.log(texto=f"Definindo a variavel de ambiente {EnumValues.COMPUTERNAME.name} com valor de {computername}")
                    self.log(texto=f"A variavel de ambiente {EnumValues.MERO_LIC.name} com valor de {mero_lic}")
                    return
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_LIC):
                os.environ[EnumValues.MERO_LIC.name] = rf'{self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_LIC)}'
                mero_lic = os.environ[EnumValues.MERO_LIC.name]
                self.log(texto=f"Definindo a variavel de ambiente {EnumAtributo.AVALIACAO_MERO_LIC.name} com valor de {str(mero_lic)}")
            else:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Variavel de ambiente {EnumValues.MERO_LIC.name} não esta definida no Windows."
                                                              f" Defina seu valor no config no atributo AVALIACAO_MERO_LIC.")
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Variavel {EnumValues.MERO_LIC.name} não esta definida.", info_ex=str(ex))
