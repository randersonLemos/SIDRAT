from globalplotconfig import GlobalPlotConfig


class StripPlotConfig(GlobalPlotConfig):
    def __init__(self):
        super().__init__()

        self.hue  = None
        self.hue_order = None

        self.style = None
        self.style_order = None

        self.palette = None

        self.linewidth = None

        self.markersize = 5

        self.alpha = None

        self.jitter = None

        self.title  = ''
        self.xlabel = ''
        self.ylabel = ''
        self.suptitle = ''

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None
