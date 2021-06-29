import header
import pathlib
import numpy as np
import pandas as pd
from zbarplot.barplotconfig import BarPlotConfig
from zbarplot.barplotclasses import BarPlot


def get_aux(experiment, data):
    msk = data.mt == experiment
    aux = data[msk]

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

    return aux


def run(experiments, dfRootpath, pngRootpath='', prefix='', suffix=''):
    if not isinstance(experiments, list):
        experiments = [experiments]

    cOb, dfH = header.load(dfRootpath)
    data = dfH.pco

    _aux = []
    for exp in experiments:
        _aux.append(get_aux(exp, data))

    aux = pd.concat(_aux)

    piv = aux.pivot_table(index=[cOb.nct_tcc, cOb.nne_sba, cOb.it], columns='confusion', values='value', aggfunc='count')
    #piv = aux.pivot_table(index=[cOb.nct_tcc, cOb.it], columns='confusion', values='value', aggfunc='count')
    piv = piv / aux.ru.max()
    piv = piv.fillna(0)


    if 'FN' not in piv:
        piv['FN'] = 0
    if 'TN' not in piv:
        piv['TN'] = 0

    piv['TNR'] = piv.TN / (piv.TN + piv.FP)
    piv['FNR'] = piv.FN / (piv.FN + piv.TP)
    #piv['FNR'] = 1.5*(piv.FN / (piv.FN + piv.TP))

    piv['TNR - FNR'] = piv['TNR'] - piv['FNR']

    #ppiv = piv.pivot_table(index=cOb.it, columns=cOb.nct_tcc, values='TNR - FNR')
    ppiv = piv.pivot_table(index=cOb.it, columns=[cOb.nne_sba], values='TNR - FNR')
    ppiv = ppiv.dropna()

    of  = aux.of.unique()[0]
    nsi = aux.nsi.unique()[0]
    nsp = aux.nsp.unique()[0]
    nct = aux.nct.unique()[0]
    tcc = aux.tcc.unique()[0]
    nne = aux.nct.unique()[0]
    sba = aux.tcc.unique()[0]

    suptitle  = 'TNR minus FNR of the samples from IDLHC with NNBC optimization on {} function\n'.format(of)
    #suptitle += 'NSI = {}, NSP = {}\n'.format(nsi, nsp)
    suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}\n'.format(nsi, nsp, tcc, nct)
    suptitle += 'Mean values from 10 experiments'
    
    config = BarPlotConfig()
    config.figsize = (16, 9)
    config.hue = cOb.nne_sba
    config.linewidth = 2
    config.suptitle = suptitle
    config.xlabel = 'Iterations'
    config.ylabel = 'Differences'
    config.ymin = -0.25
    config.ymax =  0.25

    #ppiv = ppiv[ppiv.index > 1]

    bps = BarPlot(ppiv)
    bps.plot(config)
    rootpath = pathlib.Path(pngRootpath)

    experiment = experiments[0]

    bps.save(rootpath / "{}{}_{}{}.png".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))

    path = rootpath / '{}{}_{}_README{}.txt'.format(prefix, pathlib.Path(__file__).stem, experiment, suffix)

    #import IPython; IPython.embed()
    with open(path , 'w') as fh:
        fh.write('\n'.join(experiments))
        fh.write('\n')
        fh.write(ppiv.sum().to_string())
