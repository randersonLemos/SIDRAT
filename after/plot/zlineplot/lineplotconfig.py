from globalplotconfig import GlobalPlotConfig


class LinePlotConfig(GlobalPlotConfig):
    def __init__(self):
        super().__init__()

        self.hue  = None
        self.hue_order = None

        self.style = None
        self.style_order = None

        self.alpha = None

        self.palette = None

        self.linewidth = None

        self.title  = ''
        self.xlabel = ''
        self.ylabel = ''
        self.suptitle = ''

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None
