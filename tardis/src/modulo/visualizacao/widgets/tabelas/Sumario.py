import plotly.graph_objects as go

from src.loggin.Loggin import Loggin, EnumLogStatus


class Sumario(Loggin):
    def __init__(self, df):
        super(Sumario, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._df = df.copy(deep=True)

    def run(self):
        self.log(tipo=EnumLogStatus.INFO, texto=f'Carregando sumário')
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(self._df.columns),
                        fill_color='paleturquoise',
                        font_size=30,
                        height=40,
                        align=['left', 'center']),
            cells=dict(values=[self._df.iloc[:, i] for i in range(self._df.shape[1])],
                       fill_color='lavender',
                       align=['left', 'center'],
                       font_size=30,
                       height=40))
        ])

        fig.update_layout(title='Sumário de resultados', margin=dict(t=60))

        return fig
