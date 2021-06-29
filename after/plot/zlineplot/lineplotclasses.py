import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


class _LinePlot:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data
        self.fi = None
        self.ax = None


    def save(self, path):
        print(path)
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        plt.savefig(path, pad_inches=0.0, transparent=False)
        plt.close()


class LinePlot(_LinePlot):
    def plot(self, config):
        figsize = config.figsize

        data = copy.deepcopy(self.data)
        x = self.x
        y = self.y

        fi, ax = plt.subplots(1, 1, figsize=figsize)
        self.fi = fi
        self.ax = ax

        ax  = self.ax
        axy = ax.twinx()
        axx = ax.twiny()

        ax.spines["left"].set_position(  ("axes", -0.090))
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

        #set_position = [0.180, 0.15, 0.650, 0.725]
        #ax.set_position( set_position)  # set a new position
        #axy.set_position(set_position)  # set a new position
        #axx.set_position(set_position)  # set a new position

        # ### ### ###
        sb.lineplot(   data=data
                     , x=x
                     , y=y
                     , hue=config.hue
                     , style=config.style
                     , alpha=config.alpha
                     , linewidth=config.linewidth
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
                       , labelsize=config.tick_params_labelsize
                      )

        fi.suptitle(   config.suptitle
                     , fontsize=config.suptitle_fontsize
                     , x=config.xsuptitle
                     , y=config.ysuptitle
                     #, x=0.500
                     #, y=0.995
                     , ha='center'
                    )

        ax.set_xlabel(  config.xlabel
                      , fontsize=config.label_fontsize
                     )

        ax.set_ylabel(  config.ylabel
                      , fontsize=config.label_fontsize
                     )
        leg = ax.legend(
                    loc='center left'
                    #loc='lower center'
                  , ncol=1
                  , frameon=False
                  #, bbox_transform=fi.transFigure
                  #, bbox_to_anchor=(config.xlegend, config.ylegend-0.0225)
                  , bbox_to_anchor=(1.0, 0.5)
                  , fontsize=config.legend_fontsize
                  #, title=config.hue
                  , title_fontsize=config.legend_fontsize
                 )

        for line in leg.get_lines():
            line.set_linewidth(config.linewidth*0.75)

        # ### ### ###
        data = copy.deepcopy(self.data)

        xmin = data[x].min()
        xmax = data[x].max()

        if not isinstance(config.xmin, type(None)):
            xmin = config.xmin
        if not isinstance(config.xmax, type(None)):
            xmax = config.xmax

        data[x] = (data[x] - xmin) / (xmax - xmin)

        sb.lineplot(   data=data
                     , x=x
                     , y=y
                     , hue=config.hue
                     , style=config.style
                     , alpha=config.alpha
                     , linewidth=config.linewidth
                     , legend=False
                     , ax=axx
                     )

        xlen = data[x].max() - data[x].min()
        xpad = xlen * 0.05
        xlim_min = data[x].min() - xpad
        xlim_max = data[x].max() + xpad

        axx.set_xlim(xlim_min, xlim_max)

        axx.set_xticks(np.round(np.linspace(xlim_min + xpad, xlim_max - xpad, 11), 10))
        axx.xaxis.set_major_formatter(StrMethodFormatter("{x:.3f}"))

        axx.set_xlabel('')

        axx.tick_params(   axis='both'
                         , labelsize=config.tick_params_labelsize
                         )

        # ### ### ###
        data = copy.deepcopy(self.data)

        ymin = data[y].min()
        ymax = data[y].max()

        if not isinstance(config.ymin, type(None)):
            ymin = config.ymin
        if not isinstance(config.ymax, type(None)):
            ymax = config.ymax

        data[y] = (data[y] - ymin) / (ymax - ymin)

        sb.lineplot(   data=data
                     , x=x
                     , y=y
                     , hue=config.hue
                     , style=config.style
                     , alpha=config.alpha
                     , linewidth=config.linewidth
                     , legend=False
                     , ax=axy
                     )

        ylen = data[y].max() - data[y].min()
        ypad = ylen * 0.05
        ylim_min = data[y].min() - ypad
        ylim_max = data[y].max() + ypad

        axy.set_ylim(ylim_min, ylim_max)

        axy.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 10))
        axy.yaxis.set_major_formatter(StrMethodFormatter("{x:.3f}"))

        axy.set_ylabel('')

        axy.tick_params(  axis='both'
                        , labelsize=config.tick_params_labelsize
                        )

        fi.tight_layout()

        return self



