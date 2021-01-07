import plotly
import plotly.graph_objects as go

from src.loggin.Loggin import Loggin, EnumLogStatus


class MaxLines(Loggin):
    def __init__(self, df):
        super(MaxLines, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """
        self._df = df.copy(deep=True)

    def run(self) -> plotly.graph_objs.Figure:
        df = self._df
        df['of_max'] = df['of_max'].astype(float)
        fig = go.Figure()
        for method in df['method'].unique():
            self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando gráfico de linhas de valores máximos do método {method}')
            df_method_aux = df[df['method'] == method]
            for run in df['run'].unique():
                df_run_aux = df_method_aux[(df_method_aux['run'] == run)]
                fig.add_trace(
                    go.Scattergl(
                        x=df_run_aux['id'],
                        y=df_run_aux['of_max'],
                        name=f'{method}',
                        mode='lines',
                        showlegend=True,
                        hovertemplate='of: %{y:.2f}' + '<br>id: %{x}',
                    )
                )

        max_y = df['of_max'].max()
        min_y = df['of_max'].min()
        dif_y = max_y - min_y
        fig.update_yaxes(range=[min_y - dif_y * 0.1, max_y + dif_y * 0.1], automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_layout(legend_title="Experimento",
                          xaxis_title="Avaliações",
                          yaxis_title="Função Objetivo",
                          title='Gráfico de valores máximos por avaliação',
                          )

        return fig
