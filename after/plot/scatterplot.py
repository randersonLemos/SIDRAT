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


class ScatterPlot:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y

        self.ax  = None
        self.fig = None


    def plot(self, cp_obj):
        self.fig, self.ax = plt.subplots(figsize=(11, 8))
        fig = self.fig

        ax  = self.ax
        axy = ax.twinx()
        axx = ax.twiny()

        ax.spines["left"].set_position(  ("axes", -0.105))
        ax.spines["bottom"].set_position(("axes", -0.095))

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

        set_position = [0.180, 0.15, 0.650, 0.725]
        ax.set_position( set_position)  # set a new position
        axy.set_position(set_position)  # set a new position
        axx.set_position(set_position)  # set a new position

        # ### ### ###
        tick_params_labelsize = 14
        legend_fontsize = 14
        label_fontsize = 18

        # ### ### ###
        data = copy.deepcopy(self.data)
        x = self.x
        y = self.y
        hue = cp_obj.hue
        style = cp_obj.style
        size = cp_obj.size
        sizes = cp_obj.sizes
        s = cp_obj.s
        alpha = cp_obj.alpha
        style_order = cp_obj.sty_order
        markers = cp_obj.markers
        palette = cp_obj.palette
        edgecolors = cp_obj.edgecolors
        linewidth = cp_obj.linewidth
        title = cp_obj.title
        xlabel = cp_obj.xlabel
        ylabel = cp_obj.ylabel
        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=style
                       , size=size
                       , sizes=sizes
                       , s=s
                       , alpha=alpha
                       , style_order=style_order
                       , markers=markers
                       , palette=palette
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

        ax.set_xticks(np.round(np.linspace(xlim_min + xpad, xlim_max - xpad, 11), 1))
        ax.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 1))
        ax.xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

        ax.tick_params(  axis='both'
                       , labelsize=tick_params_labelsize
                       )

        #ax.set_title(tlt, fontsize=17, pad=15.0, ha='left', loc='left', bbox_trnasform=fig.transFigure)
        fig.suptitle(title, fontsize=20, x=0.005, y=0.995, ha='left')

        ax.set_xlabel(  xlabel
                      , fontsize=label_fontsize
                      )

        ax.set_ylabel(  ylabel
                      , fontsize=label_fontsize
                      )

        ax.legend(loc='center left'
                  , ncol=1
                  , frameon=False
                  , bbox_to_anchor=(1.00, 0.50)
                  , fontsize=legend_fontsize
                  , markerscale=1.33
                 )


        # ### ### ###
        data = copy.deepcopy(self.data)

        xmin = data[x].min()
        xmax = data[x].max()

        if not isinstance(cp_obj.xmin, type(None)):
            xmin = cp_obj.xmin
        if not isinstance(cp_obj.xmax, type(None)):
            xmax = cp_obj.xmax

        data[x] = (data[x] - xmin) / (xmax - xmin)

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=style
                       , size=size
                       , sizes=sizes
                       , s=s
                       , alpha=alpha
                       , markers=markers
                       , palette=palette
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

        axx.tick_params(  axis='both'
                        , labelsize=tick_params_labelsize
                        )

        # ### ### ###
        data = copy.deepcopy(self.data)

        ymin = data[y].min()
        ymax = data[y].max()

        if not isinstance(cp_obj.ymin, type(None)):
            ymin = cp_obj.ymin
        if not isinstance(cp_obj.ymax, type(None)):
            ymax = cp_obj.ymax

        data[y] = (data[y] - ymin) / (ymax - ymin)

        sb.scatterplot(  data=data
                       , x=x
                       , y=y
                       , hue=hue
                       , style=style
                       , size=size
                       , sizes=sizes
                       , s=s
                       , alpha=alpha
                       , markers=markers
                       , palette=palette
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

        axy.tick_params(  axis='both'
                        , labelsize=tick_params_labelsize
                        )

        return self


    def save(self, path):
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        print(path)
        plt.savefig(path, pad_inches=0.0, transparent=False)
        plt.close()
