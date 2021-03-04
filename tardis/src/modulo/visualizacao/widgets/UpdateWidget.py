import plotly
import plotly.express as px


class UpdateWidget:
    @staticmethod
    def style(fig, template='plotly_white', font_size=24) -> plotly.graph_objs.Figure:
        fig.update_layout(
            template=template,
            margin=dict(b=125, t=150, l=125, r=125),
            font=dict(
                size=font_size
            )
        )
        return fig

    @staticmethod
    def titles(fig, legend="Experimento", xaxis='Avaliações', yaxis='Função Objetivo', title='Todos os resultados') -> plotly.graph_objs.Figure:
        fig.update_layout(legend_title=legend,
                          xaxis_title=xaxis,
                          yaxis_title=yaxis,
                          title=title,
                          )
        return fig

    @staticmethod
    def add_buttons_by_method(fig) -> plotly.graph_objs.Figure:
        fig.update_layout(updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.0,
                y=1.07,
                buttons=UpdateWidget._generate_buttons_list(fig),
                pad={"r": 10, "t": 10},
                showactive=True,
                xanchor="left",
                yanchor="top"
            )
        ]
        )
        return fig

    @staticmethod
    def add_combobox_by_method(fig) -> plotly.graph_objs.Figure:
        fig.update_layout(updatemenus=[
            dict(
                direction="down",
                active=0,
                x=0.0,
                y=1.07,
                buttons=UpdateWidget._generate_buttons_list(fig),
                pad={"r": 10, "t": 10},
                showactive=True,
                xanchor="left",
                yanchor="top"
            )
        ]
        )
        return fig

    @staticmethod
    def fix_color_by_method(fig) -> plotly.graph_objs.Figure:
        methods = sorted(set([trace.name for trace in fig.data]))
        color_dict_by_method = {method: color for method, color in
                                zip(methods, px.colors.qualitative.Dark24[0:len(methods)])}
        for i in range(len(fig.data)):
            fig['data'][i].fillcolor = color_dict_by_method[fig.data[i].name]
            if fig.data[i].__class__._path_str == 'box':
                fig['data'][i].marker.color = 'black'
            else:
                fig['data'][i].marker.color = color_dict_by_method[fig.data[i].name]
                fig['data'][i].line.color = color_dict_by_method[fig.data[i].name]
        return fig

    @staticmethod
    def _generate_skip_plot_position_dict(fig) -> dict:
        traces_names = []
        skip_plot_position_dict = {}
        for trace in fig.data:
            traces_names.append(trace.name)
        for trace_name_unique in set(traces_names):
            skip_plot_position_dict[trace_name_unique] = [True if trace_name_unique == trace_name else False for
                                                          trace_name in traces_names]
        return skip_plot_position_dict

    @staticmethod
    def _generate_buttons_list(fig) -> list:
        prefix = fig.layout.title['text']
        buttons = []
        skip_plot_position_dict = UpdateWidget._generate_skip_plot_position_dict(fig)
        buttons.append(dict(label='Todos os experimentos',
                            method="update",
                            args=[{'visible': [True] * len(list(skip_plot_position_dict.values())[0])},
                                  {"title": f'{prefix}'}]))
        for method_label in skip_plot_position_dict.keys():
            skip_plot_position = skip_plot_position_dict[method_label]
            buttons.append(dict(label=f'{method_label}',
                                method="update",
                                args=[{"visible": skip_plot_position},
                                      {"title": f'{prefix} {method_label}'}]))
        return list(buttons)
