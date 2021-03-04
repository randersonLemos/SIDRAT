import os

import plotly

from src.contexto.EnumAtributo import EnumAtributo
from src.inout.TXT import TXT
from src.loggin.Loggin import EnumLogStatus
from src.modulo.visualizacao.painel.PainelPadrao import PainelPadrao
from src.modulo.visualizacao.widgets.GeraWidget import GeraWidget
from src.modulo.visualizacao.widgets.UpdateWidget import UpdateWidget


class Comparacao(PainelPadrao):
    """
    Classe destinada para a ser o pai de todos os sorteios
    """

    def __init__(self):
        super(Comparacao, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.VISUALIZACAO_COMPARACAO_PATH_RESULTADO_NOME,
                             EnumAtributo.VISUALIZACAO_COMPARACAO_PATH_SAIDA] + super(Comparacao, self).necessidade

    def run(self):
        """
        Executa o modulo de painel de comparacao.
        """
        super(Comparacao, self).run()
        # TODO: GERAWIDGET RECEBE CAMINHOS DE RESULTADOS
        # TODO: GERAWIDGET VAI TER SET DE MAXIMOS AVALIACOES, CAMINHOS, BOXPLOT(PODERIA ATE SER ENTRADA DO METODO BOXPLOT
        # TODO: , ETC... TUDO QUE ESTAVA UTILIZANDO QUE ESTAVA DENTRO DO CONTEXTO
        gera_widget = GeraWidget(self._contexto)

        fig_scatter = gera_widget.scatter()
        fig_sumario = gera_widget.sumario()
        fig_max_lines = gera_widget.maxlines()
        fig_max_lines_mean = gera_widget.averamaxlines()
        fig_boxplot = gera_widget.boxplot()
        fig_rank = gera_widget.rank()

        fig_scatter = UpdateWidget.add_combobox_by_method(fig_scatter)
        fig_max_lines = UpdateWidget.add_combobox_by_method(fig_max_lines)

        fig_boxplot = UpdateWidget.fix_color_by_method(fig_boxplot)
        fig_max_lines_mean = UpdateWidget.fix_color_by_method(fig_max_lines_mean)
        fig_rank = UpdateWidget.fix_color_by_method(fig_rank)

        figs = [UpdateWidget.style(fig, template='none') for fig in
                [fig_sumario, fig_scatter, fig_max_lines, fig_max_lines_mean, fig_boxplot, fig_rank]]

        html = self._monta_html(figs)

        path_resultado = os.path.join(self._contexto.get_atributo(EnumAtributo.VISUALIZACAO_COMPARACAO_PATH_SAIDA))

        if not TXT().salvar(path_resultado, html):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Erro ao gerar arquivo {path_resultado}')

    def _monta_html(self, figs: list):
        cont = """
        <html>
        
        <head><meta charset="ISO-8859-1" />
            <title>TARDIS</title>
        </head>
        <body>
            <h1><b><center>Relatório Comparação de Estudos</center></b></h1>
            <h2><b><center>Tardis</center></b></h2>
            <h3>Este é um estudo comparativo entre diferentes métodos de otimização. Cada método pode possuir diversas rodadas. Os gráficos e tabelas deste estudo são:</h3>
            <ul>
                <li>Sumário de resultados. Tabela contendo um resumo das principais características de cada rodada de otimização</li>
                <li>Gráfico de dispersão. Gráfico contendo os resultados de todas as rodadas de otimização</li>
                <li>Gráfico de valores máximos por avaliação. Gráfico contendo apenas os maiores valores encontrados em relação ao número de avaliaçõe para cada rodada</li>
                <li>Gráfico de valores máximos médios por avaliação. Gráfico contendo a média do agrupamento por método dos maiores valores encontrados em relação ao número de avaliaçõe para cada rodada</li>
                <li>Gráfico de Boxplot. Gráfico contendo os boxplots agrupados por experimento para diferentes para diferente quantidades de avaliações</li>
                <li>Gráfico de Rank. Gráfico contendo a ordenação entre os métodos de acordo com o número de avaliações</li>
            </ul>
            <hr/>
            <hr/>
            
            ${divs}
            
        </body>
        </html>
            """

        divs = []
        divs_base = """<div>
        ${fig_html}		
        </div>
        <hr/>
        <hr/>"""

        config = {
            'toImageButtonOptions': {
                'format': 'jpeg',  # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 800,
                'width': 1500,
                'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        for fig in figs:
            divs.append(divs_base.replace("${fig_html}", plotly.io.to_html(fig=fig, config=config)))
        html_str = cont.replace("${divs}", '\n'.join(divs))
        return html_str
