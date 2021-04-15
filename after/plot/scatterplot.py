import warnings

import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter


plt.style.use('seaborn-talk')


def make_patch_spines_invisible(ax):
   ax.set_frame_on(True)
   ax.patch.set_visible(False)
   for sp in ax.spines.values():
       sp.set_visible(False)


class ScatterPlotConfig:
    def __init__(self):
        self.hue   = None
        self.sty   = None
        self.tlt   = None
        self.siz   = None
        self.sizs  = None
        self.s     = 250
        self.alpha = 0.9
        self.linewidth = 2.0

        self.markers = True
        self.palette = None
        self.edgecolors = 'black'

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None


    def set_hue(self, col_name):
        self.hue = col_name
        return self


    def set_sty(self, col_name):
        self.sty = col_name
        return self


    def set_siz(self, col_name):
        self.siz = col_name
        return self


    def set_sizs(self, tup):
        self.sizs = tup
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

    
    def set_markers(self, collection):
        self.markers = collection
        return self


    def set_palette(self, collection):
        self.palette = collection
        return self


    def set_tlt(self, title):
        self.tlt = title
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


class ScatterPlot:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y

        self.ax  = None
        self.fig = None


    def plot(self, tlt, spc_obj):
        self.fig, self.ax = plt.subplots(figsize=(11, 8))
        fig = self.fig

        ax  = self.ax
        axy = ax.twinx()
        axx = ax.twiny()

        ax.spines["left"].set_position(  ("axes", -0.1))
        ax.spines["bottom"].set_position(("axes", -0.1))

        axx.xaxis.set_label_position('bottom')
        axx.xaxis.set_ticks_position('bottom')
        axx.spines["bottom"].set_position(("axes", 0.0))
        make_patch_spines_invisible(axx)
        axx.spines["bottom"].set_visible(True)
 
        axy.yaxis.set_label_position('left')
        axy.yaxis.set_ticks_position('left')
        axy.spines["left"].set_position(("axes", 0.0))
        make_patch_spines_invisible(axy)
        axy.spines["left"].set_visible(True)

        ax.grid(True)

        set_position = [0.20, 0.15, 0.625, 0.70]
        ax.set_position( set_position)  # set a new position
        axy.set_position(set_position)  # set a new position
        axx.set_position(set_position)  # set a new position

        # ### ### ###
        data = copy.deepcopy(self.data)
        x = self.x
        y = self.y
        hue = spc_obj.hue
        sty = spc_obj.sty
        siz = spc_obj.siz
        sizs = spc_obj.sizs
        s = spc_obj.s
        alpha = spc_obj.alpha
        markers = spc_obj.markers
        palette = spc_obj.palette
        #facecolors = spc_obj.facecolors
        edgecolors = spc_obj.edgecolors
        linewidth = spc_obj.linewidth
        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=sty
                       , size=siz
                       , sizes=sizs
                       , s=s
                       , alpha=alpha
                       , markers=markers
                       , palette=palette
                       #, fc=facecolors
                       , ec=edgecolors
                       , linewidth=linewidth
                       , ax=ax
                       )

        xlen = data[x].max() - data[x].min()
        xpad = xlen * 0.05
        xlim_min = data[x].min() - xpad
        xlim_max = data[x].max() + xpad

        ylen = data[y].max() - data[y].min()
        ypad = ylen * 0.05
        ylim_min = data[y].min() - ypad
        ylim_max = data[y].max() + ypad

        ax.set_xlim(xlim_min, xlim_max)
        ax.set_ylim(ylim_min, ylim_max)

        ax.set_xticks(np.round(np.linspace(xlim_min + xpad, xlim_max - xpad, 11), 0))
        ax.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 0))

        ax.tick_params(axis='both', labelsize=14)

        #ax.set_title(tlt, fontsize=17, pad=15.0, ha='left', loc='left', bbox_trnasform=fig.transFigure)
        fig.suptitle(tlt, fontsize=20, x=0.02, ha='left')

        #ax.set_xlabel('Number of run', fontsize=16)
        #ax.set_ylabel('Max. value of obj. fun.', fontsize=16)

        ##ax.legend(loc='center left', ncol=1, frameon=False, bbox_to_anchor=(0.75, 0.5), bbox_transform=fig.transFigure)
        ax.legend(loc='center left'
                  , ncol=1
                  , frameon=False
                  , bbox_to_anchor=(1.00, 0.50)
                  , fontsize=12
                  , markerscale=0.75
                 )


        # ### ### ###
        data = copy.deepcopy(self.data)

        xmin = data[x].min()
        xmax = data[x].max()

        if not isinstance(spc_obj.xmin, type(None)):
            xmin = spc_obj.xmin
        if not isinstance(spc_obj.xmax, type(None)):
            xmax = spc_obj.xmax

        data[x] = (data[x] - xmin) / (xmax - xmin)

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=sty
                       , size=siz
                       , sizes=sizs
                       , s=s
                       , alpha=alpha
                       , markers=markers
                       , palette=palette
                       #, fc=facecolors
                       , ec=edgecolors
                       , linewidth=linewidth
                       , legend=False
                       , ax=axx
                       )

        xlen = data[x].max() - data[x].min()
        xpad = xlen * 0.05
        xlim_min = data[x].min() - xpad
        xlim_max = data[x].max() + xpad
        
        axx.set_xlim(xlim_min, xlim_max)

        axx.set_xticks(np.round(np.linspace(xlim_min + xpad, xlim_max - xpad, 11), 10))
        axx.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

        axx.set_xlabel('')

        # ### ### ###
        data = copy.deepcopy(self.data)

        ymin = data[y].min()
        ymax = data[y].max()

        if not isinstance(spc_obj.ymin, type(None)):
            ymin = spc_obj.ymin
        if not isinstance(spc_obj.ymax, type(None)):
            ymax = spc_obj.ymax
 
        data[y] = (data[y] - ymin) / (ymax - ymin)
     
        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=sty
                       , size=siz
                       , sizes=sizs
                       , s=s
                       , alpha=alpha
                       , markers=markers
                       , palette=palette
                       #, fc=facecolors
                       , ec=edgecolors
                       , linewidth=linewidth
                       , legend=False
                       , ax=axy
                       )

        ylen = data[y].max() - data[y].min()
        ypad = ylen * 0.05
        ylim_min = data[y].min() - ypad
        ylim_max = data[y].max() + ypad

        axy.set_ylim(ylim_min, ylim_max)

        axy.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 10))
        axy.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

        axy.set_ylabel('')

        return self


    def save(self, path):
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        print(path)
        plt.savefig(path, pad_inches=0.0)
        plt.close()
