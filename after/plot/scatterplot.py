import warnings

import pathlib

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


class ScatterPlot:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y

        self.hue = None
        self.stl = None

        self.tlt = None

        self.ax = None
        self.fig = None

        self.show = plt.show

        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None


    def set_hue(self, lst):
        self.hue = lst
        return self


    def set_stl(self, lst):
        self.stl = lst
        return self


    def set_tlt(self, tlt):
        self.tlt = tlt
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


    def plot_1(self):
        self.fig, self.ax = plt.subplots(figsize=(11, 8))
        fig = self.fig

        ax_ = self.ax
        axy = ax_.twinx()
        axx = ax_.twiny()

        ax_.spines["bottom"].set_position(("axes", -0.1))
        ax_.spines["left"].set_position(("axes", -0.1))

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

        ax_.grid(True)
        #axx.grid(True)
        #axy.grid(True)

        set_position = [0.20, 0.15, 0.625, 0.70]
        ax_.set_position(set_position) # set a new position
        axy.set_position(set_position) # set a new position
        axx.set_position(set_position) # set a new position

        ### ### ###
        x = self.x
        y = self.y
        hue = self.hue
        stl = self.stl
        tlt = self.tlt
        s = 300
        alpha = 0.90
  

        ### ### ###
        data = self.data.copy()

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=stl
                       , s=s
                       , alpha=alpha
                       , ax=ax_
                       )

        xlen = data[x].max() - data[x].min()
        xpad = xlen * 0.05
        xlim_min = data[x].min() - xpad
        xlim_max = data[x].max() + xpad

        ylen = data[y].max() - data[y].min()
        ypad = ylen * 0.05
        ylim_min = data[y].min() - ypad
        ylim_max = data[y].max() + ypad

        ax_.set_xlim(xlim_min, xlim_max)
        ax_.set_ylim(ylim_min, ylim_max)

        ax_.set_xticks(np.round(np.linspace(xlim_min + xpad, xlim_max - xpad, 11), 0))
        ax_.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 0))

        ax_.tick_params(axis='both', labelsize=14)

        #ax.set_title(tlt, fontsize=17, pad=15.0, ha='left', loc='left', bbox_trnasform=fig.transFigure)
        fig.suptitle(tlt, fontsize=20, x=0.02, ha='left')

        ax_.set_xlabel('Number of run', fontsize=16)
        ax_.set_ylabel('Max. value of obj. fun.', fontsize=16)

        #ax.legend(loc='center left', ncol=1, frameon=False, bbox_to_anchor=(0.75, 0.5), bbox_transform=fig.transFigure)
        ax_.legend(loc='center left', ncol=1, frameon=False, bbox_to_anchor=(1.00, 0.50), fontsize=12)


        ### ### ###
        data = self.data.copy()

        xmin = data[x].min()
        xmax = data[x].max()

        if not isinstance(self.xmin, type(None)) : xmin = self.xmin
        if not isinstance(self.xmax, type(None)) : xmax = self.xmax

        data[x] = (data[x] - xmin) / (xmax - xmin)

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=stl
                       , s=s
                       , alpha=alpha
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


        ### ### ###
        data = self.data.copy()

        ymin = data[y].min()
        ymax = data[y].max()

        if not isinstance(self.ymin, type(None)) : ymin = self.ymin
        if not isinstance(self.ymax, type(None)) : ymax = self.ymax
 
        data[y] = (data[y] - ymin) / (ymax - ymin)

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=stl
                       , s=s
                       , alpha=alpha
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
