import warnings

import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter
from collections.abc import Iterable


class  _StripPlot:
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


class  StripPlotDefault(_StripPlot):
    def plot(self, config):
        figsize = config.figsize

        data = copy.deepcopy(self.data)
        x = self.x
        y = self.y

        fi, ax = plt.subplots(1, 1, figsize=figsize)
        self.ax = ax

        order = config.hue_order

        if order:
            data[config.hue] = data[config.hue].astype("category")
            data[config.hue] = data[config.hue].cat.set_categories(order)
            data = data.sort_values(config.hue)

        sb.stripplot(  x=x
                     , y=y
                     , data=data
                     , hue=config.hue
                     , hue_order=config.hue_order
                     , jitter=config.jitter
                     , alpha=config.alpha
                     , size=config.markersize
                     , linewidth=config.linewidth
                     , edgecolor='k'
                     , palette=config.palette
                     , ax=ax
                    )

        ax.tick_params(  axis='both'
                       , labelsize=config.tick_params_labelsize
                       )

        fi.suptitle(  config.suptitle
                     , fontsize=config.suptitle_fontsize
                     #, x=0.500
                     , x=config.xsuptitle
                     #, y=0.960
                     , y=config.ysuptitle
                     , ha='center'
                    )

        ax.set_xlabel(  config.xlabel
                      , fontsize=config.label_fontsize
                     )

        ax.set_ylabel(  config.ylabel
                      , fontsize=config.label_fontsize
                     )

        ax.legend(loc='lower center'
                  , ncol=6
                  , frameon=False
                  #, bbox_to_anchor=(0.525, -0.04)
                  , bbox_to_anchor=(config.xlegend, config.ylegend)
                  , bbox_transform=fi.transFigure
                  , fontsize=config.legend_fontsize
                 )

        fi.tight_layout()

        return self
