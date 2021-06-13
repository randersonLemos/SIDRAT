import copy

from globalplotconfig import GlobalPlotConfig


class BarPlotConfig(GlobalPlotConfig):
    def __init__(self):
        super().__init__()

        self.hue  = None
        self.hue_order = None
        self.palette = None

        self.title  = ''
        self.xlabel = ''
        self.ylabel = ''
        self.suptitle = ''

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None
