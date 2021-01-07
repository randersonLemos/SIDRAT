import numpy as np
import pandas as pd

from src.contexto.EnumAtributo import EnumAtributo
from src.loggin.Loggin import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.modulo.visualizacao.widgets.figuras.BoxPlot import BoxPlot
from src.modulo.visualizacao.widgets.figuras.MaxLines import MaxLines
from src.modulo.visualizacao.widgets.figuras.MaxLinesAverage import MaxLinesAverage
from src.modulo.visualizacao.widgets.figuras.Rank import Rank
from src.modulo.visualizacao.widgets.figuras.Scatter import Scatter
from src.modulo.visualizacao.widgets.tabelas.Sumario import Sumario


class GeraWidget(Loggin):
    def __init__(self, contexto):
        super(GeraWidget, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._contexto = contexto
        """
        Todas as informações necessárias
        """

        self._df_padrao: pd.DataFrame = self._carrega_df_padrao()

    def sumario(self):
        df = self._gera_df_sumario()
        fig = Sumario(df).run()
        return fig

    def scatter(self):
        df = self._retira_linhas_erros_df_padrao()
        fig = Scatter(df).run()
        return fig

    def maxlines(self):
        df = self._carrega_coluna_of_max_df_padrao()
        fig = MaxLines(df).run()
        return fig

    def averamaxlines(self):
        df = self._carrega_coluna_of_max_df_padrao()
        df = self._carrega_coluna_of_max_mean_df_padrao()
        fig = MaxLinesAverage(df).run()

        return fig

    def boxplot(self):
        df = self._carrega_coluna_of_max_df_padrao()
        intervalos = self._gera_intervalos_box_blot()
        fig = BoxPlot(df).run(intervalos)

        return fig

    def rank(self):
        df = self._carrega_coluna_of_max_df_padrao()
        df = self._carrega_coluna_of_max_mean_df_padrao()
        df = self._carrega_coluna_rank()
        fig = Rank(df).run()

        return fig

    def _gera_intervalos_box_blot(self) -> list:
        if self._contexto.tem_atributo(EnumAtributo.VISUALIZACAO_COMPARACAO_BOXPLOT_AVALIACOES):
            intervalos = self._contexto.get_atributo(EnumAtributo.VISUALIZACAO_COMPARACAO_BOXPLOT_AVALIACOES).split('#')
        else:
            var_intervalos = int(self._df_padrao['id'].max() / 3)
            intervalos = [var_intervalos, var_intervalos * 2, self._df_padrao['id'].max()]
        try:
            intervalos = [int(intervalo) for intervalo in intervalos]
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL,
                     texto=f'Intervalos do boxplot informados de maneira incorreta [{ex}]')
        if len(intervalos) == 0:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Intervalos do boxplot informados de maneira incorreta')
        return intervalos

    def _retira_linhas_erros_df_padrao(self) -> pd.DataFrame:
        df = self._df_padrao.copy(deep=True)
        return df[~((df['of'] == 'None') | (df['of'] == '-inf') | (df['of'].isna()))]

    def _carrega_coluna_of_max_mean_df_padrao(self) -> pd.DataFrame:
        if 'mean_of_max' not in self._df_padrao:
            self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando no DataFrame padrão a coluna de média da função objetivo máxima')
            df = self._df_padrao.copy(deep=True)
            df = df[~(df['of_max'] == 'None')]
            df['of_max'] = df['of_max'].astype(float)
            df['mean_of_max'] = df.groupby(['method', 'id'])['of_max'].transform(np.mean)
            self._df_padrao = df
        return self._df_padrao

    def _carrega_coluna_of_max_df_padrao(self) -> pd.DataFrame:
        if 'of_max' not in self._df_padrao.columns:
            self.log(tipo=EnumLogStatus.INFO,texto=f'Carregando no DataFrame padrão a coluna de função objetivo máxima')
            max_avaliacoes = self._df_padrao['id'].max()
            df = self._df_padrao.copy(deep=True)
            df['of_max'] = df.groupby(['method', 'run'])['of'].apply(self._max_value_in_series)
            df = df[df['of_max'] != 'None']
            df['of_max'].astype(float)
            grouped = df.groupby(['run', 'method'])
            id_max_grouped = grouped[['id', 'of_max']].max().reset_index()
            for i in range(id_max_grouped.shape[0]):
                if id_max_grouped.iloc[i]['id'] != max_avaliacoes:
                    primeiro_indice_novo = id_max_grouped.iloc[i]['id'] + 1
                    ultimo_indice_novo = max_avaliacoes + 1
                    df_aux = pd.DataFrame(index=range(primeiro_indice_novo, ultimo_indice_novo),
                                          columns=df.columns)
                    df_aux['id'] = df_aux.index
                    df_aux['of_max'] = id_max_grouped.iloc[i]['of_max']
                    df_aux['run'] = id_max_grouped.iloc[i]['run']
                    df_aux['method'] = id_max_grouped.iloc[i]['method']
                    df = pd.concat([df, df_aux], axis=0)
            self._df_padrao = df.copy(deep=True)
        return self._df_padrao

    def _carrega_coluna_rank(self) -> pd.DataFrame:
        if 'rank' not in self._df_padrao:
            self.log(tipo=EnumLogStatus.INFO,
                     texto=f'Carregando no DataFrame padrão a coluna rank')
            df = self._df_padrao.copy(deep=True)
            df['rank'] = df.groupby(['id', 'run'])['mean_of_max'].transform(lambda x: x.rank(ascending=False))
            self._df_padrao = df
        return self._df_padrao

    def _max_value_in_series(self, sr: pd.Series) -> pd.Series:
        """
        Metodo responsavel por receber uma serie e retonar a seria com valor para cada index de max(sr[index],sr[index-1])
        :param sr:
        :return: sr
        """
        first_index = sr.index[0]
        for index, value in sr.items():
            if index != first_index:
                preview_value = sr.loc[index - 1]
                if preview_value == 'None':
                    preview_value = float('-inf')

                actual_value = sr.loc[index]
                if (actual_value == 'None') or (actual_value == '-inf'):
                    if preview_value == float('-inf'):
                        actual_value = 0
                    else:
                        actual_value = float('-inf')
                else:
                    actual_value = float(actual_value)

                sr.loc[index] = actual_value if preview_value < actual_value else preview_value
        return sr

    def _carrega_df_padrao(self) -> pd.DataFrame:

        dict_experimento_caminhos = self._carrega_experimentos_caminhos()
        dfs = []

        if self._contexto.tem_atributo(EnumAtributo.VISUALIZACAO_COMPARACAO_MAX_AVALIACOES):
            max_avaliacoes = self._contexto.get_atributo(EnumAtributo.VISUALIZACAO_COMPARACAO_MAX_AVALIACOES)
        else:
            max_avaliacoes = None

        for method in dict_experimento_caminhos.keys():
            for n_run, path in enumerate(dict_experimento_caminhos[method]):
                rodada_str = f'{n_run + 1}'
                df_aux = pd.DataFrame()
                try:
                    self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando DataFrame da rodada {n_run}, método {method} no DataFrame padrão')
                    df_aux = pd.read_csv(path, sep=';', usecols=['of', 'id', 'iteracao'])
                except Exception as ex:
                    self.log(tipo=EnumLogStatus.ERRO_FATAL,
                             texto=f'Erro ao acessar arquivo de resultados {path} [{ex}]')
                df_aux['run'] = rodada_str
                df_aux['method'] = method
                df_aux['erro'] = False
                df_aux.loc[(df_aux['of'] == 'None') | (df_aux['of'] == '-inf'), ['erro']] = True

                dfs.append(df_aux)

        df = pd.concat(dfs, axis=0, ignore_index=True)

        if max_avaliacoes == None:
            max_avaliacoes = df['id'].max()
        df = df[df['id'] <= max_avaliacoes]

        return df

    def _carrega_experimentos_caminhos(self) -> dict:
        """

        carrega um dicionario de listas com experimentos e caminhos de seus resultados
        :return: dicionario com chave=nome experimento. valor=caminhos dos resultados deste experimentpo
        :rtype: dict
        """
        dict_experimento_caminhos = {}
        caminhos_experimento_list = self._contexto.get_atributo(
            EnumAtributo.VISUALIZACAO_COMPARACAO_PATH_RESULTADO_NOME)
        for num_resultado, (caminhos_experimento) in enumerate(caminhos_experimento_list):
            caminhos_experimento_split = caminhos_experimento.split('#')
            caminho = None
            experimento = None
            if len(caminhos_experimento_split) == 1:
                caminho = caminhos_experimento_split[0]
                experimento = f'Resultado {num_resultado}'
            elif len(caminhos_experimento_split) == 2:
                caminho, experimento = caminhos_experimento_split
            else:
                self.log(EnumLogStatus.ERRO_FATAL, texto='Passagem de caminhos e nomes experimentos nao esta correta')
            if experimento in dict_experimento_caminhos.keys():
                dict_experimento_caminhos[experimento].append(caminho)
            else:
                dict_experimento_caminhos[experimento] = [caminho]

        return dict_experimento_caminhos

    def _gera_df_sumario(self) -> pd.DataFrame:
        self.log(tipo=EnumLogStatus.INFO, texto=f'Processando DataFrame com sumario dos resultados')
        df = self._df_padrao
        df_sumario = pd.DataFrame(
            columns=['metodo', 'rodada', 'FO_max', 'FO_min', 'numero_iteracoes', 'numero_avaliacoes', 'erros'])
        for method in df['method'].unique():
            df_aux_method = df[df['method'] == method]
            for n_run in df_aux_method['run'].unique():
                df_aux_run = df_aux_method[df_aux_method['run'] == n_run]
                erros = (df_aux_run['erro'] == True).sum()
                df_aux_run = df_aux_run[~((df_aux_run['of'] == 'None') | (df_aux_run['of'] == '-inf'))]
                FO_max = df_aux_run['of'].astype(float).max()
                FO_min = df_aux_run['of'].astype(float).min()
                numero_iteracoes = df_aux_run['iteracao'].astype(int).max()
                numero_avaliacoes = df_aux_run['id'].astype(int).max()

                to_append = [method, n_run, FO_max, FO_min, numero_iteracoes, numero_avaliacoes, erros]

                a_series = pd.Series(to_append, index=df_sumario.columns)
                df_sumario = df_sumario.append(a_series, ignore_index=True)

        df_sumario[['FO_max','FO_min']] = df_sumario[['FO_max','FO_min']].round(2)

        return df_sumario
