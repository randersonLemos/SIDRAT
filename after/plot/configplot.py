import copy


class ConfigPlot:
    def __init__(self):
        self.hue   = None
        self.style   = None
        self.size   = None
        self.sizes  = None
        self.s     = 250
        self.alpha = 0.7
        self.linewidth = 2.0
        self.markersize = 20

        self.sty_order = None

        self.markers = False
        self.dashes  = False
        self.palette = None
        self.edgecolors = 'black'

        self.title  = ''
        self.xlabel = ''
        self.ylabel = ''

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None


    def set_hue(self, col_name):
        self.hue = col_name
        return self


    def set_style(self, col_name):
        self.style = col_name
        return self


    def set_size(self, col_name):
        self.size = col_name
        return self


    def set_sizes(self, tup):
        self.sizes = tup
        return self


    def set_s(self, vl):
        self.s = vl
        return self


    def set_alpha(self, vl):
        self.alpha = vl
        return self


    def set_linewidth(self, vl):
        self.linewidth = vl
        return self


    def set_markersize(self, vl):
        self.markersize = vl
        return self


    def set_sty_order(self, lst):
        self.sty_order = lst
        return self


    def set_markers(self, collection):
        self.markers = collection
        return self


    def set_dashes(self, collection):
        self.dashes = collection
        return self


    def set_palette(self, collection):
        self.palette = collection
        return self


    def set_title(self, title):
        self.title = title
        return self


    def set_xlabel(self, label):
        self.xlabel = label
        return self


    def set_ylabel(self, label):
        self.ylabel = label
        return self


    def set_xmax(self, vl):
        self.xmax = vl
        return self


    def set_xmin(self, vl):
        self.xmin = vl
        return self


    def set_ymax(self, vl):
        self.ymax = vl
        return self


    def set_ymin(self, vl):
        self.ymin = vl
        return self


    def copy(self):
        return copy.deepcopy(self)
