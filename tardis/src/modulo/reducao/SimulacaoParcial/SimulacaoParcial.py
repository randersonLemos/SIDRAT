"""
:author: Rafael
:data: 06/12/2019
"""
import copy
import re
import sys
from datetime import date as format_date

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.CSV import CSV
from src.inout.Exportacao import Exportacao
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.Modulo import Modulo
from src.modulo.reducao.RedutorPadrao import RedutorPadrao
from src.modulo.reducao.SimulacaoParcial.SimulacaoTotal import SimulacaoTotal


class SimulacaoParcial(RedutorPadrao):
    """
    Classe destinada para redução de anos de simulação
    """

    def __init__(self):
        super(SimulacaoParcial, self).__init__()

        self._necessidade = [EnumAtributo.REDUCAO_MERO_GEVT_MARCAS_PATH] + super(SimulacaoParcial, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def run(self, contexto: Contexto):
        """
        Executa o redutor parcial

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(SimulacaoParcial, self).run(contexto)

        gevts_tempales = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)
        uniecos = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR)
        if (len(uniecos) > 1) or (len(gevts_tempales) > 1):
            self.log(tipo=EnumLogStatus.ERRO_FATAL,
                     texto="O redutor não esta preparado para lidar com otimização robusta.")

        if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_DATA_FINAL):

            if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_DIA_FINAL):

                if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_TIME_LIST):
                    self._seta_qualificador_template_de_sim_parcial()

                    return self._contexto

            self._data_sim_parcial = self._contexto.get_atributo(EnumAtributo.REDUCAO_GEVT_DATA_FINAL)

            self._avaliacao_gevt()

            self._gera_e_seta_dias_datas_sim_parcial()

            self._seta_qualificador_template_de_sim_parcial()

            return

        qtd_simulacao_total = self._contexto.get_atributo(EnumAtributo.REDUCAO_QUANTIDADE_SIMULACAO_TOTAL)
        solucao_base = self._contexto.get_atributo(EnumAtributo.SOLUCAO_BASE)

        sorteio = self._contexto.get_modulo(EnumModulo.SORTEIO)

        self._contexto = sorteio.run(self._contexto,
                                     solucao_base,
                                     qtd_simulacao_total)

        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
        self._contexto = avaliacao.run(self._contexto)

        self._avalia_rankeamento_simulacoes_parciais()

        self.log(tipo=EnumLogStatus.INFO, texto='Estudo de recall gerado na pasta de resultados')

        ultima_iteracao = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)

        self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes_it_para_menos1(ultima_iteracao)

        Exportacao().csv(self._contexto)
        Exportacao().obejto(self._contexto)

        self.log(tipo=EnumLogStatus.INFO,
                 texto='Finalizando Tardis. Resumir a otimizacao com REDUCAO_GEVT_DATA_FINAL escolhida pelo arquivo de estudo de recall por data')
        sys.exit()

    def after(self, contexto):
        super(SimulacaoParcial, self).after(contexto)

        simulador_total = Modulo(SimulacaoTotal()).run(self._contexto)
        simulador_total.run(self._contexto)
        self._contexto = simulador_total.contexto

    def _seta_qualificador_template_de_sim_parcial(self):
        """

        Método responsavel por setar no contexto o template gevt com marcas e qualificador parcial
        : AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR, AVALIACAO_QUALIFICADOR
        """

        path_mero_gevt_marcas = self._contexto.get_atributo(EnumAtributo.REDUCAO_MERO_GEVT_MARCAS_PATH)

        gevts_tpls = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)
        key = list(gevts_tpls.keys())[0]

        gevts_tpls[key]['gevt_path'] = path_mero_gevt_marcas

        self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR, gevts_tpls, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR, EnumValues.PARCIAL.name, True)

    def _avalia_rankeamento_simulacoes_parciais(self):
        """

        Gera tabela de recall do ranqueamento em relacao ao tempo de simulacao dos n_melhores_estudos
        """
        ultima_iteracao = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
        solucoes_estudo = self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes[ultima_iteracao]

        dfs_dates = []

        for key, solucao in solucoes_estudo.items():
            df_economico = solucao.economico['dataframe']
            df_NPV = df_economico[df_economico['OF'] == 'NPV']
            nome_modelo = df_NPV['MODEL'].iloc[0]

            df_date = df_NPV[['DATE', 'VALUE']].T

            datas_disponiveis = df_date.iloc[0, :]
            df_date = df_date.iloc[1:, :]
            df_date.columns = datas_disponiveis
            df_date.index = [nome_modelo]
            dfs_dates.append(copy.deepcopy(df_date))

        df_date_all = pd.concat(dfs_dates, axis=0, sort=True)

        dates = list(df_date_all.columns)
        dates.sort(key=lambda x: (x.split('/')[2], x.split('/')[1], x.split('/')[0]))

        df_date_all = df_date_all[dates]

        df_rank = df_date_all.rank().sort_values(by=dates[-1])

        df_date_top = df_rank.iloc[0:self._contexto.get_atributo(EnumAtributo.REDUCAO_RANK_ANALISE), :] <= \
                      self._contexto.get_atributo(EnumAtributo.REDUCAO_RANK_ANALISE)

        df_precisao_por_data = df_date_top.sum(axis=0) / self._contexto.get_atributo(EnumAtributo.REDUCAO_RANK_ANALISE)

        df_precisao_por_data.index.name = 'DATA POR RECALL'

        path_csv_estudo = InOut.ajuste_path('\\'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
                                                       self._contexto.get_atributo(
                                                           EnumAtributo.PATH_RESULTADO)])).format('estudo_recall.csv')

        CSV().salvar(path_csv_estudo, df_precisao_por_data)

        # data_otima = None
        # for data in df_precisao_por_data.index:
        #     if df_precisao_por_data[data] >= self._contexto.get_atributo(EnumAtributo.REDUCAO_PRECISAO):
        #         data_otima = data
        #         break
        #
        # self.log(texto=f'data otima de simulacao = {data_otima}')
        #
        # self._data_otima = data_otima
        # self._contexto.set_atributo(EnumAtributo.REDUCAO_GEVT_DATA_FINAL, self._data_otima)

    def _avaliacao_gevt(self):
        """

        Le gevt e seta o  self._data_inicial, self._data_final e self._dia_inicio_previsao que serao utilizados
        para calcular lista de dias e dia final de simulacao que
        """
        # disponivel ainda somente para otimização nominal
        gevts_tpls = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)
        for key in gevts_tpls.keys():
            path_gevt = gevts_tpls[key]['gevt_path']
        path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        path_completo_gevt = InOut.ajuste_path(f'{path_projeto}/{path_gevt}')

        linhas_gevt = TXT().ler(path_completo_gevt)

        conteudo_gvt = ''

        for linha in linhas_gevt:
            conteudo_gvt += linha

        matches = re.findall(r'\n\*INITIAL_DATE\s*([^\s]+)', conteudo_gvt)
        data_inicial = matches[0]

        matches = re.findall(r'\n\*FINAL_DATE\s*([^\s]+)', conteudo_gvt)
        data_final = matches[0]

        matches = re.findall(r'\n\*TIME_LIST\s*(\w*)', conteudo_gvt)
        dia_inicio_previsao = matches[0]

        self._data_inicial = data_inicial
        self._data_final = data_final
        self._dia_inicio_previsao = int(dia_inicio_previsao)

    def _gera_e_seta_dias_datas_sim_parcial(self):
        """

        Metodo responsavel por atribuir ao contexto o valor referente ao dia final de simulacao e lista de tempos para serem
        simulados e que serao substituidos no gevt marcas: REDUCAO_GEVT_TIME_LIST e REDUCAO_GEVT_DIA_FINAL.
        :return:
        """

        data_otima = self._data(self._data_sim_parcial)
        data_inicial = self._data(self._data_inicial)

        diferenca_data_em_meses = (data_otima.year - data_inicial.year) * 12 + data_otima.month - data_inicial.month

        avaible_dates = []
        for months in range(diferenca_data_em_meses + 1):
            avaible_dates.append(data_inicial + relativedelta(months=months))

        avaible_days = []
        for date in avaible_dates:
            avaible_days.append((date - self._data(self._data_inicial)).days)

        datas_disponiveis = avaible_dates
        dias_disponiveis = avaible_days

        dias_disponiveis_previsao_otima = [dia for dia in dias_disponiveis if dia >= self._dia_inicio_previsao]
        dias_disponiveis_previsao_otima.sort()
        ultimo_dia_disponivel_previsao_otima = dias_disponiveis_previsao_otima[-1]

        self._contexto.set_atributo(EnumAtributo.REDUCAO_GEVT_TIME_LIST,
                                    dias_disponiveis_previsao_otima)
        self._contexto.set_atributo(EnumAtributo.REDUCAO_GEVT_DIA_FINAL,
                                    ultimo_dia_disponivel_previsao_otima)

    @staticmethod
    def _data(data):
        data_splitted = data.split('/')
        ano = data_splitted[2]
        mes = data_splitted[1]
        dia = data_splitted[0]

        return format_date(int(ano), int(mes), int(dia))
