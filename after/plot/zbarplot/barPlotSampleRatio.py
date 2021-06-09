import header
import pathlib
import numpy as np
from zbarplot.barPlotConfig import BarPlotConfig
from zbarplot.barPlotClasses import BarPlot


def run(experiment, dfRootpath, pngRootpath=''):

    cOb, dfH = header.load(dfRootpath)
    por = dfH.pco

    msk = por.mt == experiment
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

    piv = aux.pivot_table(index='confusion', columns='it', values='value', aggfunc='count').T
    piv = piv / aux.ru.max()
    piv = piv.fillna(0)

    if 'FN' not in piv:
        piv['FN'] = 0
    if 'TN' not in piv:
        piv['TN'] = 0

    piv['FNR'] = piv.FN / (piv.FN + piv.TP)
    piv['TNR'] = piv.TN / (piv.TN + piv.FP)

    of  = aux.of.unique()[0]
    nsi = aux.nsi.unique()[0]
    nsp = aux.nsp.unique()[0]
    nct = aux.nct.unique()[0]
    tcc = aux.tcc.unique()[0]

    suptitle  = 'TNR and FNR of the samples from IDLHC with NNBC optimization on {} function\n'.format(of)
    suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}\n'.format(nsi, nsp, nct, tcc)
    suptitle += 'Mean values from 10 experiments'

    config = BarPlotConfig()
    config.figsize = (16, 9)
    config.hue = 'confusion'
    config.hue_order = ['FNR', 'TNR']
    config.palette = {'FNR': 'red', 'TNR': 'blue'}
    config.suptitle = suptitle
    config.xlabel = 'Iterations'
    config.ylabel = 'Ratios'
    config.ymin = 0

    bps = BarPlot(piv)
    bps.plot(config)
    rootpath = pathlib.Path(pngRootpath)
    bps.save(rootpath / 'barPlotRatio_{}.png'.format(experiment))
