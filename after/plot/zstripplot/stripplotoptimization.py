import header
import pathlib
import numpy as np
from zstripplot.stripplotconfig import StripPlotConfig
from zstripplot.stripplotclasses import StripPlotDefault


def run(experiments, dfRootpath, pngRootpath='', prefix='', suffix=''):
    if not isinstance(experiments, list):
        experiments = [experiments]

    for experiment in experiments:
        cOb, dfH = header.load(dfRootpath)
        df = dfH.pco

        msk = df.mt == experiment
        aux = df[msk]

        aux = aux.sort_values(by=['ru', 'it', 'value'], ascending=False)

        gb = aux.groupby(['ru', 'it'])['value']
        tr = gb.transform(lambda x: np.where(x.reset_index().index < 20, 'a', 'b'))
        aux['confusion'] = tr

        gb = aux.groupby(['ru', 'it'])['class']
        tr = gb.transform(lambda x: np.where(x == 1, 'c', 'd'))
        aux.confusion += tr

        TP = 'True Postive (TP)'
        FP = 'False Positive (FP)'
        FN = 'False Negative (FN)'
        TN = 'True Negative (TN)'
        aux.confusion = aux.confusion.str.replace('ac', TP)
        aux.confusion = aux.confusion.str.replace('bc', FP)
        aux.confusion = aux.confusion.str.replace('ad', FN)
        aux.confusion = aux.confusion.str.replace('bd', TN)

        piv = aux.pivot_table(index='confusion', columns='it', values='value', aggfunc='count').T
        piv = piv / aux.ru.max()
        piv = piv.fillna(0)

        if FN not in piv:
            piv[FN] = 0
        if TN not in piv:
            piv[TN] = 0

        of  = aux.of.unique()[0]
        nsi = aux.nsi.unique()[0]
        nsp = aux.nsp.unique()[0]
        nct = aux.nct.unique()[0]
        tcc = aux.tcc.unique()[0]
        nne = aux.nne.unique()[0]
        sba = aux.sba.unique()[0]

        config = StripPlotConfig()
        config.figsize = (16, 9)
        config.linewidth = 1
        config.alpha = 0.70
        config.markersize = 8
        config.hue = 'confusion'
        config.hue_order = [FP, TP, TN, FN]
        config.jitter = 0.25
        config.palette = {TP: 'tab:blue', FP: 'tab:orange', FN: 'tab:red', TN: 'tab:green'}

        config.xlabel = 'Iterations'
        config.ylabel = 'Num. of samples'
        config.ymin = 0

        aux = aux[aux.ru <= 5]

        nux = aux.copy()
        gb = nux.groupby(['ru', 'it'])['value']
        tr = gb.transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        nux.value = tr

        suptitle  = 'TP, FN, TN, FP of the samples from IDLHC with NNBC optimization on {} function\n'.format(of)
        #suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}\n'.format(nsi, nsp, nct, tcc)
        suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}, NNE = {}, SBA = {}\n'.format(nsi, nsp, nct, tcc, nne, sba)
        suptitle += 'Samples from 5 experiments'
        config.suptitle = suptitle
        spd = StripPlotDefault(data=aux, x=cOb.it, y=cOb.value)
        spd.plot(config)
        rootpath = pathlib.Path(pngRootpath)
        spd.save(rootpath / "{}{}_{}{}.png".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))

        suptitle  = 'TP, FN, TN, FP of the samples from IDLHC with NNBC optimization on {} function\n'.format(of)
        #suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}\n'.format(nsi, nsp, nct, tcc)
        suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}, NNE = {}, SBA = {}\n'.format(nsi, nsp, nct, tcc, nne, sba)
        suptitle += 'Samples from 5 experiments normalized'
        config.suptitle = suptitle
        spd = StripPlotDefault(data=nux, x=cOb.it, y=cOb.value)
        spd.plot(config)
        rootpath = pathlib.Path(pngRootpath)
        spd.save(rootpath / "{}{}normalized_{}{}.png".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))
