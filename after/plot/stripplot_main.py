import pathlib
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import StrMethodFormatter


class Columns:
    def __init__(self):
        self.mt = 'mt'
        self.of = 'of'
        self.id = 'id'
        self.it = 'it'
        self.ru = 'ru'
        self.value = 'value'
        self.n_sample = 'n_sample'
        self.nsi = 'nsi'
        self.nsp = 'nsp'
        self.nct = 'nct'
        self.tcc = 'tcc'
        self.nsi_nsp = 'nsi_nsp'
        self.nct_tcc = 'nct_tcc'
        self.nnnt = 'nnnt'
        self.nnbc = 'nnbc'
        self.cls = 'class'

    def rename(self, df, att, name):
        dic = {self.__dict__[att] : name}
        self.__dict__[att] = name
        df = df.rename(columns=dic)
        return df


def get_data():
    co = Columns()

    path = '/media/beldroega/DATA/SHARED/csv/'
    zll_data = pd.read_csv(path + 'zall_data.csv')

    for col in ['nsi', 'nsp', 'nct', 'tcc']:
        zll_data[col] = zll_data[col].astype('str')

    zll_data = zll_data[zll_data[co.tcc] != '70']

    return zll_data


def scatterplot(data, co, fig=None, ax=None, ec=None, title='', xlabel='', ylabel=''):
    if not ax:
        fig, ax = plt.subplots(figsize=(11, 8))

    x = co.id
    y = co.value

    ax = sb.scatterplot(  x=x
                        , y=y
                        , hue=co.cls
                        #, hue_order=[1.0, 0.0]
                        , style=co.nnnt
                        , data=data
                        , ax=ax
                        , ec=ec
                        , legend=True
                       )


    #fig.suptitle(title, fontsize=20, x=0.05, ha='left')
    fig.suptitle(title, fontsize=20)
    #ax.set_title(title, fontsize=20, x=0.05, ha='center')

    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)

    set_position = [0.20, 0.15, 0.625, 0.70]
    ax.set_position( set_position)  # set a new position

    ax.tick_params(axis='both', labelsize=14)

    ax.legend( loc='lower right'
              , ncol=1
              , frameon=True
              , bbox_to_anchor=(1.00, 0.00)
              , fontsize=12
              , markerscale=1.33
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

    return fig, ax

def plot1():
    co = Columns()

    zll_data = get_data()

    tlt  = ''
    tlt  += 'Sphere function optimization using IDLHC with NNBC\n'
    tlt  += 'Number of runs versus Obj. fun. values (all 5 trials)\n'
    tlt  += 'Stop criterion of 30 iterations or 3 iterations with equal max. value'

    xlb = 'Number of runs'
    ylb = 'Obj. fun. values'

    zdt = zll_data
    zdt = co.rename(zdt, 'cls', 'DRAWN SAMPLES')
    zdt = co.rename(zdt, 'nnnt', 'NSI, NSP, NCT, TCC')

    zdt.loc[zdt[co.cls] != 0.0, co.cls] = "Run"
    zdt.loc[zdt[co.cls] == 0.0, co.cls] = "Not run"

    zdt = zdt[(zdt[co.nsi_nsp] == '100, 020')]
    zdt = zdt[(zdt[co.nct_tcc] == '020, 010')]

    #zdt = zdt.set_index(co.ru)
    #lst = []
    #for idx in zdt.index.unique():
    #    aux = zdt.loc[idx]
    #    mvl = aux.loc[aux[co.cls] == 'Run', co.id].shape[0]
    #    aux.loc[aux[co.cls] == 'Run', co.id] = range(1, mvl+1)
    #    lst.append(aux.reset_index())
    #zdt = pd.concat(lst)

    zdt = zdt.sort_values(by=co.cls, ascending=False)
    fig, ax = scatterplot(zdt, co, title=tlt, xlabel=xlb, ylabel=ylb)

    ax.axhline(y=-19, color='r', linestyle='-')
    ax.axvline(x=1683, color='r', linestyle='-')

    ax.axhline(y=-17, color='g', linestyle='-')
    ax.axvline(x=1624, color='g', linestyle='-')


    plt.savefig("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_100020020010_0.png", pad_inches=0.0)


def plot2():
    co = Columns()

    zll_data = get_data()

    tlt  = ''
    tlt  += 'Sphere function optimization using IDLHC with NNBC\n'
    tlt  += 'Number of runs versus Obj. fun. values (all 5 trials)\n'
    tlt  += 'Stop criterion of 30 iterations or 3 iterations with equal max. value'

    xlb = 'Number of runs'
    ylb = 'Obj. fun. values'

    zdt = zll_data
    zdt = co.rename(zdt, 'cls', 'DRAWN SAMPLES')
    zdt = co.rename(zdt, 'nnnt', 'NSI, NSP, NCT, TCC')

    zdt.loc[zdt[co.cls] != 0.0, co.cls] = "Run"
    zdt.loc[zdt[co.cls] == 0.0, co.cls] = "Not run"

    zdt = zdt[(zdt[co.nsi_nsp] == '100, 020')]
    zdt = zdt[(zdt[co.nct_tcc] == '010, 010')]

    #zdt = zdt.set_index(co.ru)
    #lst = []
    #for idx in zdt.index.unique():
    #    aux = zdt.loc[idx]
    #    mvl = aux.loc[aux[co.cls] == 'Run', co.id].shape[0]
    #    aux.loc[aux[co.cls] == 'Run', co.id] = range(1, mvl+1)
    #    lst.append(aux.reset_index())
    #zdt = pd.concat(lst)

    zdt = zdt.sort_values(by=co.cls, ascending=False)
    fig, ax = scatterplot(zdt, co, title=tlt, xlabel=xlb, ylabel=ylb)

    ax.axhline(y=-19, color='r', linestyle='-')
    ax.axvline(x=1683, color='r', linestyle='-')

    ax.axhline(y=-20, color='g', linestyle='-')
    ax.axvline(x=1511, color='g', linestyle='-')

    plt.savefig("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_100020010010_0.png", pad_inches=0.0)


if __name__ == "__main__":
    plot1()
    plot2()


#    #ax = scatterplot(zdt[zdt[co.cls] == 0.0], fig=fig, ax=ax, ec='red', title=tlt, xlabel=xlb, ylabel=ylb)
#
#    print(zdt.shape)
#    print(zdt[zdt[co.cls] == 0].shape)

    #zdt = zll_data
    #zdt = zdt[(zdt[co.nsi_nsp] == '100, 020')]
    #zdt = zdt[(zdt[co.nct_tcc] == '010, 010')]
    #ax = scatterplot(zdt)
    #ax = scatterplot(zdt[zdt[co.cls] == 0.0], ax=ax, ec='red')

    #print(zdt.shape)
    #print(zdt[zdt[co.cls] == 0].shape)

    #zdt = zll_data
    #zdt = zdt[(zdt[co.nsi_nsp] == '100, 030')]
    #zdt = zdt[(zdt[co.nct_tcc] == '020, 010')]
    #ax = scatterplot(zdt)
    #ax = scatterplot(zdt[zdt[co.cls] == 0.0], ax=ax, ec='red')

    #print(zdt.shape)
    #print(zdt[zdt[co.cls] == 0].shape)

    #zdt = zll_data
    #zdt = zdt[(zdt[co.nsi_nsp] == '100, 030')]
    #zdt = zdt[(zdt[co.nct_tcc] == '010, 010')]
    #ax = scatterplot(zdt)
    #ax = scatterplot(zdt[zdt[co.cls] == 0.0], ax=ax, ec='red')

    #print(zdt.shape)
    #print(zdt[zdt[co.cls] == 0].shape)



#ax.set_title("IDLHC: 100, 020")
#
