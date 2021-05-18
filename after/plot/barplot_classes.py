import warnings

import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter
from collections.abc import Iterable


class  BarPlotHandle:
    def __init__(self, data, x):

        self.data = data
        if not isinstance(data, list):
            self.data = [data]

        self.x = x
        #self.y = y

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
        #y = self.y

        hue = cp_obj.hue
        hue_order = cp_obj.hue_order
        title = cp_obj.title
        palette = cp_obj.palette
        xlabel = cp_obj.xlabel
        ylabel = cp_obj.ylabel
        stack = cp_obj.stack

        for data, ax in zip(Data, axs):
            data = data.fillna(0)

            order = data.columns.tolist()
            if hue_order:
                order = hue_order

            data = data[order]
            if stack:
                data = data.cumsum(axis=1)

            stk = data.stack()
            stk.name = 'y'
            stk = stk.reset_index()
            
            if stack:
                for col in reversed(order):
                    msk = stk['confusion'] == col
                    sb.barplot(  x=x
                               , y='y'
                               , hue=hue
                               , data=stk[msk]
                               , palette=palette
                               , ax=ax
                              )
            else:
                sb.barplot(  x=x
                           , y='y'
                           , hue=hue
                           , data=stk
                           , palette=palette
                           , ax=ax
                          )


            ax.legend(loc='center right')

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

        ylen = data.max().max() - 0
        ypad = ylen * 0.05
        ylim_min = 0
        ylim_max = data.max().max() + ypad

        ax.set_ylim(ylim_min, ylim_max)

        ax.set_yticks(np.round(np.linspace(ylim_min, ylim_max - ypad, 11), 1))
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
        if ylim_max < 1.0:
            ax.set_yticks(np.round(np.linspace(ylim_min, ylim_max - ypad, 11), 2))
            ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

        ax.grid()

        fig.tight_layout()

        return self


    def save(self, path):
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        print(path)
        plt.savefig(path, pad_inches=0.0, transparent=False)
        plt.close()
