import copy
import header
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from collections.abc import Iterable

plt.close()


cOb = header.cOb
por = header.dfH.pco


figsize = (20, 10)


def stripplot_handle(dfs, prefix='', suffix=''):

    if not isinstance(dfs, list):
        dfs = [dfs]

    fig, axs = plt.subplots(len(dfs), 1, figsize=figsize, sharex=True, gridspec_kw={'hspace' : 0})

    if not isinstance(axs, Iterable):
        axs = [axs]

    for df, ax in zip(dfs, axs):
        sb.stripplot(  x=cOb.it
                     , y=cOb.value
                     , hue='ab'
                     #, hue_order=['a+', 'b+', 'a-', '+ -']
                     #, dodge=True
                     , jitter=0.30
                     , alpha=0.70
                     , data=df
                     , s=10
                     , linewidth=0.5
                     , edgecolor='black'
                     , ax=ax
                    )

        ax.legend(loc='center right')

    fig.suptitle(mt)
    fig.tight_layout()
    fig.savefig("./fig/" + prefix + mt + suffix + ".png")


for mt in por.mt.unique():
    msk = por.mt == mt
    aux = por[msk]

    aux = aux.sort_values(by=['ru', 'it', 'value'], ascending=False)

    gb = aux.groupby(['ru', 'it'])['value']
    tr = gb.transform(lambda x: np.where(x.reset_index().index < 20, 'a', 'b'))
    aux['ab'] = tr

    gb = aux.groupby(['ru', 'it'])['class']
    tr = gb.transform(lambda x: np.where(x == 1, 'c', 'd'))
    aux.ab += tr

    aux = aux.sort_values(by='ab', ascending=True)

    nux = aux.copy()
    gb = nux.groupby('it')['value']
    tr = gb.transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    nux.value = tr


    stripplot_handle(aux, prefix='a')
    stripplot_handle(nux, prefix='b')


    zuxs = []
    nuxs = []
    for ru in aux.ru.unique():
        msk = aux.ru == ru
        zux = aux[msk]
        zuxs.append(zux)

        nux = zux.copy()
        gb = nux.groupby('it')['value']
        tr = gb.transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        nux.value = tr
        nuxs.append(nux)


    stripplot_handle(zuxs, prefix='c')
    stripplot_handle(nuxs, prefix='d')


    aux.to_csv('csv/' + mt + '.csv', index=False)

    piv = aux.pivot_table(index='ab', columns='it', values='value', aggfunc='count').T
    break
