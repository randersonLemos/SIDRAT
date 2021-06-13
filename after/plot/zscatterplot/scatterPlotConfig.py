import copy


class ScatterPlotConfig:
    def __init__(self):
        self.hue  = None
        self.hue_order = None

        self.style = None
        self.style_order = None

        self.palette = None

        self.linewidth = None

        self.alpha = None

        self.title  = ''
        self.xlabel = ''
        self.ylabel = ''

        self.suptitle = ''

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None

        self.figsize = None

        self.title_fontsize = 22
        self.suptitle_fontsize = 22
        self.tick_params_labelsize = 14
        self.legend_fontsize = 14
        self.label_fontsize = 18