import warnings

import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter
from collections.abc import Iterable


class  StripPlotHandle:
    def __init__(self, data, x, y):

        if not isinstance(data, list):
            self.data = [data]
        else:
            self.data = data
        

        self.x = x
        self.y = y

        self.axs = None
        self.fig = None


    def set_data(self, data):
        if not isinstance(data, list):
            self.data = [data]
        else:
            self.data = data


    def plot(self, cp_obj):
        figsize = cp_obj.figsize

        fig, axs = plt.subplots(  len(self.data)
                                , 1
                                , figsize=figsize
                                , sharex=True
                                , gridspec_kw={'hspace' : 0}
                               )

        self.fig = fig
        self.axs = axs

        if not isinstance(axs, Iterable):
            axs = [axs]


        # ### ### ###
        tick_params_labelsize = 14
        legend_fontsize = 14
        label_fontsize = 18
        ###

        Data = self.data
        x = self.x
        y = self.y
        hue = cp_obj.hue
        hue_order = cp_obj.hue_order
        jitter = cp_obj.jitter
        s = cp_obj.s
        alpha = cp_obj.alpha
        edgecolors = cp_obj.edgecolors
        linewidth = cp_obj.linewidth
        palette = cp_obj.palette
        title = cp_obj.title
        xlabel = cp_obj.xlabel
        ylabel = cp_obj.ylabel
        for data, ax in zip(Data, axs):

            sb.stripplot(  x=x
                         , y=y
                         , hue=hue
                         #, order=hue_order
                         , hue_order=hue_order
                         , jitter=jitter
                         , alpha=alpha
                         , data=data
                         , s=s
                         , linewidth=linewidth
                         , edgecolor=edgecolors
                         , palette=palette
                         , ax=ax
                        )

            ax.legend(loc='center right')

            ylen = data[y].max() - data[y].min()
            ypad = ylen * 0.05
            ylim_min = data[y].min() - ypad
            ylim_max = data[y].max() + ypad

            ax.set_ylim(ylim_min, ylim_max)

            ax.tick_params(  axis='both'
                           , labelsize=tick_params_labelsize
                           )

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

        fig.tight_layout()

        return self


    def save(self, path):
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        print(path)
        plt.savefig(path, pad_inches=0.0, transparent=False)
        plt.close()
