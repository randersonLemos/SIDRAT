import header
import pathlib
import pandas as pd
from zlineplot.lineplotconfig import LinePlotConfig
from zlineplot.lineplotclasses import LinePlot


def get_aux(experiment, data):
    msk = data.mt == experiment
    aux = data[msk]
    return aux


def Get_aux(experiments, data):
    _aux = []
    for exp in experiments:
        _aux.append(get_aux(exp, data))

    aux = pd.concat(_aux)
    return aux


def run(experiments, dfRootpath, pngRootpath='', prefix='', suffix=''):
    cOb, dfH = header.load(dfRootpath)
    data = dfH.mxc

    data = cOb.rename(data, 'nsi_nsp', 'NSI, NSP')
    data = cOb.rename(data, 'nct_tcc', 'NCT, TCC')
    data = cOb.rename(data, 'nne_sba', 'NNE, SBA')

    if not isinstance(experiments, list):
        experiments = [experiments]

    aux = Get_aux(experiments, data)

    of  = aux.of.unique()[0]
    nsi = aux.nsi.unique()[0]
    nsp = aux.nsp.unique()[0]
    nct = aux.nct.unique()[0]
    tcc = aux.tcc.unique()[0]

    config = LinePlotConfig()
    config.figsize = (16, 9)
    config.hue = cOb.nne_sba
    config.style = cOb.nct_tcc
    config.linewidth = 4
    config.alpha = 1.0

    suptitle = ''
    suptitle += 'Evolution of IDLHC with NNBC optimization on {} function\n'.format(of)
    #suptitle += 'NSI = {}, NSP = {}, NCT = {}, TCC = {}\n'.format(nsi, nsp, nct, tcc)
    suptitle += 'NSI = {}, NSP = {}\n'.format(nsi, nsp, nct, tcc)
    suptitle += 'Mean values from 10 experiments'

    config.suptitle = suptitle
    config.xlabel = 'Num. of runs'
    config.ylabel = 'Obj. fun. values'

    #aux = aux.sort_values(by=cOb.nnnt, ascending=True)

    config.ymin = aux[cOb.value].min()
    config.ymax = aux[cOb.value].max()
    config.xmin = 1
    config.xmax = aux[cOb.id].max()

    lp = LinePlot(data=aux, x=cOb.id, y=cOb.value)
    lp.plot(config)
    rootpath = pathlib.Path(pngRootpath)

    experiment = experiments[0]
    #lp.save(rootpath / "{}{}_{}{}.png".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))
    #lp.save(rootpath / "{}{}_{}{}.eps".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))
    lp.save(rootpath / "{}{}_{}{}.svg".format(prefix, pathlib.Path(__file__).stem, experiment, suffix))
