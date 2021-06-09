import warnings

import pathlib

import copy
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter
from collections.abc import Iterable


class  _BarPlot:
    def __init__(self, data):
        self.data = data
        self.fi = None
        self.ax = None
        self.ax = None


    def save(self, path):
        print(path)
        path = pathlib.Path(path)
        path.parent.mkdir(exist_ok=True)
        plt.savefig(path, pad_inches=0.0, transparent=False)
        plt.close()


class BarPlotStack(_BarPlot):
    def plot(self, config):
        figsize = config.figsize

        fi, ax  = plt.subplots(1, 1, figsize=figsize)
        self.fi = fi
        self.ax = ax

        data = self.data
        x = data.index.name
        y = 'value'

        order = data.columns.tolist()
        if config.hue_order:
            order = list(reversed(config.hue_order))

        data = data[order]

        data = data.cumsum(axis=1)

        stk = data.stack()
        stk.name = y
        stk = stk.reset_index()

        for col in reversed(order):
            msk = stk['confusion'] == col
            sb.barplot(  x=x
                       , y=y
                       , hue=config.hue
                       , data=stk[msk]
                       , palette=config.palette
                       , linewidth=config.linewidth
                       , edgecolor='k'
                       , ax=ax
                      )

        ax.tick_params(  axis='both'
                       , labelsize=config.tick_params_labelsize
                       )

        fi.suptitle(  config.suptitle
                     , fontsize=config.suptitle_fontsize
                     , x=0.500
                     , y=0.960
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
                  #, bbox_to_anchor=(0.50, -0.04)
                  , bbox_to_anchor=(0.525, -0.04)
                  , bbox_transform=fi.transFigure
                  , fontsize=config.legend_fontsize
                 )

        ymin = data.min().min()
        if not isinstance(config.ymin, type(None)):
            ymin = config.ymin

        ymax = data.max().max()
        if not isinstance(config.ymax, type(None)):
            ymax = config.ymax

        ylen = ymax - ymin
        ypad = ylen * 0.05
        ylim_min = ymin - ypad
        ylim_max = ymax + ypad

        ax.set_ylim(ylim_min, ylim_max)

        ax.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 1))
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

        ax.grid()

        fi.tight_layout()

        return self


class BarPlotStackWithoutCumsum(_BarPlot):
    def plot(self, config):
        figsize = config.figsize

        fi, ax = plt.subplots(1, 1, figsize=figsize)
        self.ax = ax
        self.fi = fi

        data = self.data
        x = data.index.name
        y = 'value'

        order = data.columns.get_level_values(1).unique().tolist()
        if config.hue_order:
            order = config.hue_order

        stk = data.stack()
        hatchs = ['///', '']
        ec = ['tab:red', 'k']
        for idx in [0, 1]:
            aux = stk.iloc[:, idx]
            aux.name = y
            aux = aux.reset_index()
            sb.barplot(  x=x
                       , y=y
                       , hue=config.hue
                       , hue_order=order
                       , data=aux
                       , palette=config.palette
                       , alpha=config.alpha
                       , ax=ax
                       #, edgecolor=(0.0, 0.0, 0.0, 1.0)
                       , edgecolor=ec[idx]
                       , linewidth=config.linewidth
                       , hatch=hatchs[idx]
                      )

            if idx == 1:
                idx = 0
                msk = (stk.diff(axis=1) > 0).iloc[:, 1]
                aux = stk.where(msk, 0)
                aux = aux.iloc[:, idx]
                aux.name = y
                aux = aux.reset_index()
                sb.barplot(  x=x
                           , y=y
                           , hue=config.hue
                           , hue_order=order
                           , data=aux
                           , palette=config.palette
                           , alpha=config.alpha
                           , ax=ax
                           #, edgecolor=(0.0, 0.0, 0.0, 1.0)
                           , edgecolor=ec[idx]
                           , linewidth=config.linewidth
                           , hatch=hatchs[idx]
                          )

        ax.tick_params(  axis='both'
                       , labelsize=config.tick_params_labelsize
                       )

        fi.suptitle(  config.suptitle
                     , fontsize=config.suptitle_fontsize
                     , x=0.500
                     , y=0.960
                     , ha='center'
                    )

        ax.set_xlabel(  config.xlabel
                      , fontsize=config.label_fontsize
                      )

        ax.set_ylabel(  config.ylabel
                      , fontsize=config.label_fontsize
                      )

        handles, labels = ax.get_legend_handles_labels()

        _idx = int(len(handles) / 3)
        ax.legend(  handles[:-_idx]
                  , labels[:-_idx]
                  , loc='lower center'
                  , ncol=6
                  , frameon=False
                  #, bbox_to_anchor=(0.5, -0.040)
                  , bbox_to_anchor=(0.525, -0.04)
                  , bbox_transform=fi.transFigure
                  , fontsize=config.legend_fontsize
                 )

        ymin = data.min().min()
        if not isinstance(config.ymin, type(None)):
            ymin = config.ymin

        ymax = data.max().max()
        if not isinstance(config.ymax, type(None)):
            ymax = config.ymax

        ylen = ymax - ymin
        ypad = ylen * 0.05
        ylim_min = ymin - ypad
        ylim_max = ymax + ypad

        ax.set_ylim(ylim_min, ylim_max)

        ax.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 3))
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

        ax.grid()

        #ax.axhspan(0, ylim_max, facecolor='blue', alpha=0.10, zorder=0)
        #ax.axhspan(ylim_min, 0, facecolor='red', alpha=0.10, zorder=0)



        fi.tight_layout()

        return self


class  BarPlot(_BarPlot):
    def plot(self, config):
        figsize = config.figsize

        fi, ax = plt.subplots(1, 1, figsize=figsize)
        self.ax = ax
        self.fi = fi

        data = self.data
        x = data.index.name
        y = 'value'

        order = data.columns.tolist()
        if config.hue_order:
            order = list(reversed(config.hue_order))

        data = data[order]

        stk = data.stack()
        stk.name = y
        stk = stk.reset_index()
      
        sb.barplot(  x=x
                   , y=y
                   , hue=config.hue
                   , data=stk
                   , palette=config.palette
                   , edgecolor=(0.0, 0.0, 0.0, 1.0)
                   , linewidth=config.linewidth
                   , ax=ax
                  )

        ax.tick_params(  axis='both'
                       , labelsize=config.tick_params_labelsize
                       )

        fi.suptitle(  config.suptitle
                     , fontsize=config.suptitle_fontsize
                     , x=0.500
                     , y=0.960
                     , ha='center'
                    )

        ax.set_xlabel(  config.xlabel
                      , fontsize=config.label_fontsize
                      )

        ax.set_ylabel(  config.ylabel
                      , fontsize=config.label_fontsize
                      )

        ax.legend(  loc='lower center'
                  , ncol=10
                  , frameon=False
                  , bbox_to_anchor=(0.525, -0.04)
                  , bbox_transform=fi.transFigure
                  , fontsize=config.legend_fontsize
                 )

        ymin = data.min().min()
        if not isinstance(config.ymin, type(None)):
            ymin = config.ymin

        ymax = data.max().max()
        if not isinstance(config.ymax, type(None)):
            ymax = config.ymax

        ylen = ymax - ymin
        ypad = ylen * 0.05
        ylim_min = ymin - ypad
        ylim_max = ymax + ypad

        ax.set_ylim(ylim_min, ylim_max)

        ax.set_yticks(np.round(np.linspace(ylim_min + ypad, ylim_max - ypad, 11), 3))
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

        ax.grid()

        fi.tight_layout()

        return self
