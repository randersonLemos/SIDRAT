import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.loggin.Loggin import Loggin, EnumLogStatus


class BoxPlot(Loggin):
    def __init__(self, df: pd.DataFrame):
        super(BoxPlot, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """
        self._df = df

    def run(self, intervalos: list) -> plotly.graph_objs.Figure:
        df = self._df

        df = df[df['id'].isin(intervalos)]

        fig = make_subplots(rows=1, cols=len(intervalos),
                            subplot_titles=[f'{id} avaliações' for id in intervalos],
                            shared_yaxes=True)

        methods_in_legend = []
        for i, id in enumerate(df['id'].unique()):
            for method in df['method'].unique():
                self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando gráfico de boxplot do método {method}')
                if method in methods_in_legend:
                    show_legend = False
                else:
                    show_legend = True
                    methods_in_legend.append(method)

                df_method_aux = df[df['method'] == method]
                df_id_aux = df_method_aux[(df_method_aux['id'] == id)]

                fig.add_trace(
                    go.Box(
                        y=df_id_aux['of_max'],
                        name=f'{method}',
                        showlegend=show_legend,
                        legendgroup=method),
                    row=1, col=i + 1
                )

        max_y = df['of_max'].max()
        min_y = df['of_max'].min()
        dif_y = max_y - min_y

        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

        fig.update_yaxes(range=[min_y - dif_y * 0.1, max_y + dif_y * 0.1], automargin=True)
        fig.update_xaxes(tickangle=45, showticklabels=False, automargin=True)

        fig.update_layout(legend_title="Experimento",
                          yaxis_title="Função Objetivo",
                          title='BoxPlot',
                          )

        return fig

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
                sr.loc[index] = sr.loc[index] if preview_value < sr.loc[index] else preview_value
        return sr
