import plotly.express as px
import plotly

from src.loggin.Loggin import Loggin, EnumLogStatus


class Rank(Loggin):
    def __init__(self, df):
        super(Rank, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """
        self._df = df

    def run(self) -> plotly.graph_objs.Figure:
        df = self._df
        df = df[df['run'] == '1'].copy(deep=True)
        self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando gráfico de rank')
        df_rank_aux = df.loc[df['id'].isin(list(range(0, df['id'].max() + 1, 50)))].copy(deep=True)

        df_rank_aux['mean_of_max'] = df_rank_aux['mean_of_max'].round(2)

        fig = px.line(df_rank_aux.rename(columns={'mean_of_max': 'of médio'}), x='id', y='rank', color='method',
                      title='Rank', hover_data=['of médio'])

        fig.update_layout(legend_title="Experimento",
                          xaxis_title="Avaliações",
                          yaxis_title="Rank",
                          title='Rank da função objetivo entre métodos por número de avaliações',
                          )

        fig.update_layout(
            yaxis=dict(
                tickmode='linear',
                dtick=1
            )
        )

        fig['layout']['yaxis']['autorange'] = "reversed"
        fig.update_xaxes(automargin=True)
        fig.update_yaxes(automargin=True)

        return fig
