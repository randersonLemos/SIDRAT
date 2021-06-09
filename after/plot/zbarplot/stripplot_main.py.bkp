import copy
import header
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
plt.close()


cOb = header.cOb
por = header.dfH.pco

from configplot import ConfigPlot
from stripplot_classes import StripPlotHandle
from barplot_classes import BarPlotHandle

cp = ConfigPlot()
cp.set_figsize((20, 10, ))
cp.set_hue('confusion')
cp.set_linewidth(1)
cp.set_alpha(0.80)
cp.set_jitter(0.30)
cp.set_s(10)

cp.set_palette(
    {
     'TP': 'blue'
   , 'TN': 'green'
   , 'FP': 'orange'
   , 'FN': 'red'
   }
)

cp.set_hue_order(
    [
        'TP'
      , 'FN'
      , 'TN'
      , 'FP'
    ]
)

cpBar = ConfigPlot()
cpBar.set_figsize((20, 10, ))
cpBar.set_linewidth(1)
cpBar.set_s(10)
cpBar.set_stack(True)
cpBar.set_hue('confusion')

cpBar.set_palette(
    {
     'TP': 'blue'
   , 'TN': 'green'
   , 'FP': 'orange'
   , 'FN': 'red'
   }
)

cpBar.set_hue_order(
    [
        'FP'
      , 'TN'
      , 'FN'
      , 'TP'
    ]
)

cpBar.set_xlabel('Iterations')
cpBar.set_ylabel('Drawn samples')

#for en, mt in enumerate(por.mt.unique()):
for en, mt in enumerate(por.mt.unique()[1:]):
    print(mt)

    msk = por.mt == mt
    aux = por[msk]

    aux = aux.sort_values(by=['ru', 'it', 'value'], ascending=False)

    gb = aux.groupby(['ru', 'it'])['value']
    tr = gb.transform(lambda x: np.where(x.reset_index().index < 20, 'a', 'b'))
    aux['confusion'] = tr

    gb = aux.groupby(['ru', 'it'])['class']
    tr = gb.transform(lambda x: np.where(x == 1, 'c', 'd'))
    aux.confusion += tr

    aux.confusion = aux.confusion.str.replace('ac', 'TP')
    aux.confusion = aux.confusion.str.replace('bc', 'FP')
    aux.confusion = aux.confusion.str.replace('ad', 'FN')
    aux.confusion = aux.confusion.str.replace('bd', 'TN')

    nux = aux.copy()
    gb = nux.groupby(['ru', 'it'])['value']
    tr = gb.transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    nux.value = tr

    of = aux.of.unique()[0]

    # AUX PLOT
    cp.set_title(mt + ' (10 experiments)')
    cp.set_xlabel('Iterations')
    cp.set_ylabel('Obj. fun. values')
    aux = aux.sort_values(by='class', ascending=False)
    sph = StripPlotHandle(aux, cOb.it, cOb.value)
    sph.plot(cp).save("/media/beldroega/DATA/SHARED/png/{}_STRIPPLOT_V1_{}.png".format(of, mt))

    # NUX PLOT
    cp.set_title(mt + ' (10 experiments) (normalized per iteration)')
    nux = nux.sort_values(by='class', ascending=False)
    sph.set_data(nux)
    sph.plot(cp).save("/media/beldroega/DATA/SHARED/png/{}_STRIPPLOT_V2_{}.png".format(of, mt))

    # BAR PLOT
    cpBar.set_title(mt + ' (Mean values from 10 experiments)')

    cpBar.set_palette(
        {
         'TP': 'blue'
       , 'TN': 'green'
       , 'FP': 'orange'
       , 'FN': 'red'
       }
    )

    cpBar.set_hue_order(
        [
            'FP'
          , 'TN'
          , 'FN'
          , 'TP'
        ]
    )


    cpBar.set_stack(True)

    piv = aux.pivot_table(index='confusion', columns='it', values='value', aggfunc='count').T

    piv = piv / 10

    bph = BarPlotHandle(piv, x='it')
    bph.plot(cpBar).save("/media/beldroega/DATA/SHARED/png/{}_BARPLOT_V1_{}.png".format(of, mt))

    piv['FN/(FN + TP)'] = piv.FN / (piv.FN + piv.TP)
    piv['TN/(TN + FP)'] = piv.TN / (piv.TN + piv.FP)

    cpBar.set_stack(False)

    cpBar.set_palette(
        {
         'FN/(FN + TP)': 'red'
       , 'TN/(TN + FP)': 'green'
       }
    )

    cpBar.set_hue_order(
        [
            'FN/(FN + TP)'
          , 'TN/(TN + FP)'
        ]
    )
    bph = BarPlotHandle(piv, x='it')
    bph.plot(cpBar).save("/media/beldroega/DATA/SHARED/png/{}_BARPLOT_V2_{}.png".format(of, mt))

    piv['DIFF'] = - (piv['FN/(FN + TP)'] - piv['TN/(TN + FP)'])

    cpBar.set_palette(
        {
         'DIFF': 'blue'
       }
    )

    cpBar.set_hue_order(
        [
            'DIFF'
        ]
    )
    bph = BarPlotHandle(piv, x='it')
    bph.plot(cpBar).save("/media/beldroega/DATA/SHARED/png/{}_BARPLOT_V3_{}.png".format(of, mt))


    break

    #zuxs = []
    #nuxs = []
    #for ru in aux.ru.unique():
    #    msk = aux.ru == ru
    #    zux = aux[msk]
    #    zuxs.append(zux)

    #    nux = zux.copy()
    #    gb = nux.groupby('it')['value']
    #    tr = gb.transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    #    nux.value = tr
    #    nuxs.append(nux)


    #cp.set_title(mt + ' (5 experiments)')
    #cp.set_xlabel('Iterations')
    #cp.set_ylabel('Obj. fun. values')
    #sph = StripPlotHandle(zuxs[:5], cOb.it, cOb.value)
    #sph.plot(cp).save("/media/beldroega/DATA/SHARED/png/crastrigin_stripplot_{}.png".format(en))

    #cp.set_title(mt + ' (5 experiments) (normalized per iteration)')
    #sph.set_data(nuxs[:5])
    #sph.plot(cp).save("/media/beldroega/DATA/SHARED/png/drastrigin_stripplot_{}.png".format(en))

