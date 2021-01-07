import plotly
import plotly.graph_objects as go

from src.loggin.Loggin import Loggin, EnumLogStatus


class Scatter(Loggin):
    def __init__(self, df):
        super(Scatter, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """
        self._df = df.copy(deep=True)

    def run(self) -> plotly.graph_objs.Figure:
        df = self._df
        df['of'] = df['of'].astype(float)
        fig = go.Figure()
        for method in df['method'].unique():
            self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando gráfico de dispersão do método {method}')
            df_method_aux = df[df['method'] == method]
            for run in df['run'].unique():
                df_run_aux = df_method_aux[(df_method_aux['run'] == run)]
                fig.add_trace(
                    go.Scattergl(
                        x=df_run_aux['id'],
                        y=df_run_aux['of'],
                        name=f'{method}',
                        mode='markers',
                        showlegend=True,
                        hovertemplate='of: %{y:.2f}' + '<br>id: %{x}',
                    )
                )

        max_y = df['of'].max()
        min_y = df['of'].min()
        dif_y = max_y - min_y
        max_x = df['id'].max()
        min_x = df['id'].min()
        fig.update_yaxes(range=[min_y - dif_y * 0.1, max_y + dif_y * 0.1], automargin=True)
        fig.update_xaxes(range=[min_x, max_x], automargin=True)
        fig.update_layout(legend_title="Experimento",
                          xaxis_title="Avaliações",
                          yaxis_title="Função Objetivo",
                          title='Gráfico de dispersão',
                          )

        return fig
