import plotly
import plotly.graph_objects as go
import pandas as pd

from src.loggin.Loggin import Loggin, EnumLogStatus


class MaxLinesAverage(Loggin):
    def __init__(self, df: pd.DataFrame):
        super(MaxLinesAverage, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """
        self._df = df.copy(deep=True)

    def run(self) -> plotly.graph_objs.Figure:
        df = self._df
        df = df[df['run'] == '1']
        fig = go.Figure()
        for method in df['method'].unique():
            self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando gráfico de linhas de valores máximos médio do método {method}')
            df_method_aux = df[df['method'] == method]
            fig.add_trace(
                go.Scattergl(
                    x=df_method_aux['id'],
                    y=df_method_aux['mean_of_max'],
                    name=f'{method}',
                    mode='lines',
                    showlegend=True,
                    hovertemplate='of médio: %{y:.2f}' + '<br>id: %{x}',
                )
            )

        max_y = df['mean_of_max'].max()
        min_y = df['mean_of_max'].min()
        dif_y = max_y - min_y
        fig.update_yaxes(range=[min_y - dif_y * 0.1, max_y + dif_y * 0.1], automargin=True)
        fig.update_xaxes(automargin=True)

        fig.update_layout(legend_title="Experimento",
                          xaxis_title="Avaliações",
                          yaxis_title="Função Objetivo",
                          title='Gráfico de valores máximos médios por método',
                          )

        return fig
