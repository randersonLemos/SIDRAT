import header
import copy
import pathlib
import numpy as np
import pandas as pd
from zscatterplot.scatterPlotConfig import ScatterPlotConfig
from zscatterplot.scatterPlotClasses import ScatterPlot


def run(experiments, dfRootpath, pngRootpath='', prefix='', suffix=''):
    if not isinstance(experiments, list):
        experiments = [experiments]

    for experiment in experiments:
        cOb, dfH = header.load(dfRootpath)
        mxo = dfH.mxo

        mxo = cOb.rename(mxo, cOb.nsi_nsp, 'NSI, NSP')
        mxo = cOb.rename(mxo, cOb.nct_tcc, 'NCT, TCC')

        pv = pd.pivot_table(  mxo
                            , index=[  cOb.mt
                                     , cOb.of
                                     , cOb.nsi
                                     , cOb.nsp
                                     , cOb.nct
                                     , cOb.tcc
                                     , cOb.nsi_nsp
                                     , cOb.nct_tcc
                                     , cOb.nnnt
                                     , cOb.nnbc
                                    ]
                            , values=[cOb.id, cOb.value]
                            , aggfunc={cOb.id : max, cOb.value : max}
                           ).reset_index()

        aux = copy.deepcopy(pv)

        config = ScatterPlotConfig()
        config.figsize = (16, 5)
        config.hue = cOb.nsi_nsp
        config.style = cOb.nct_tcc

        config.palette =  \
            {
              '050, 010': 'aqua'
            , '050, 020': 'royalblue'
            , '050, 030': 'midnightblue'
            , '100, 010': 'lightgreen'
            , '100, 020': 'olivedrab'
            , '100, 030': 'darkgreen'
            , '150, 010': 'rosybrown'
            , '150, 020': 'tomato'
            , '150, 030': 'darkred'
            }

        config.markers = \
            {
              '000, 000': 'o'
            , '010, 010': 's'
            , '010, 020': '^'
            , '010, 030': 'v'
            , '020, 010': 'P'
            , '020, 020': '*'
            , '020, 030': 'X'
            , '030, 010': '>'
            , '030, 020': '<'
            , '030, 030': 'D'
            }

        #cp.set_sty_order(
        #    [
        #      '000, 000'
        ##    , '030, 010'
        ##    , '030, 030'
        ##    , '030, 050'
        ##    , '020, 010'
        ##    , '020, 030'
        ##    , '020, 050'
        ##    , '010, 010'
        ##    , '010, 030'
        ##    , '010, 050'
        #    ]
        #)

        suptitle = ''
        suptitle += 'Optimization experiments of the Sphere function using IDLHC with NNBC\n'
        suptitle += 'Stop criterion of a max. of 30 iterations\n'
        suptitle += 'Experiments repeated 10 times\n'

        xlabel = 'Avg. final number of runs'
        ylabel = 'Avg. max. obj. fun. values'

        config.suptitle = suptitle
        config.xlabel = xlabel
        config.ylabel = ylabel

        config.ymin = aux[cOb.value].min()
        config.ymax = aux[cOb.value].max()
        config.xmin = 1
        config.xmax = aux[cOb.id].max()

        aux = aux.sort_values(by=cOb.nnnt, ascending=False)
        sp = ScatterPlot(data=aux, x=cOb.id, y=cOb.value)
        #sp = ScatterPlotHandle(data=aux[aux[cOb.nnbc] == 'Off'], x=cOb.id, y=cOb.value)
        #sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_0.png")

        #cp.set_sty_order(
        #    [
        #      '000, 000'
        #    , '030, 010'
        #    , '030, 020'
        #    , '030, 030'
        #    , '020, 010'
        #    , '020, 020'
        #    , '020, 030'
        #    , '010, 010'
        #    , '010, 020'
        #    , '010, 030'
        #    ]
        #)

        #sp = ScatterPlotHandle(data=aux, x=cOb.id, y=cOb.value)
        #sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_1.png")

        ##msk =     (aux[colsObj.nsi_nsp] == "100, 020") \
        ##        | (aux[colsObj.nsi_nsp] == "100, 030") \
        ##        | (aux[colsObj.nsi_nsp] == "050, 010") \
        ##        | (aux[colsObj.nsi_nsp] == "050, 020")
        ##aux = aux[msk]
        ##
        ###vl = aux[aux[colsObj.nnnt] == '050, 010, 000, 000'][colsObj.value]
        ###msk = aux[colsObj.value] >= int(vl)
        ###aux = aux[msk]
        ##
        ##cp.set_xmin(1).set_xmax(aux[colsObj.id].max())
        ##
        ##sp = ScatterPlot(data=aux, x=colsObj.id, y=colsObj.value)
        ##sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_2.png")
        ##
        ##cp.set_sty_order([
        ##      '000, 000'
        ##    , '030, 010'
        ###    , '030, 030'
        ###    , '030, 050'
        ##    , '020, 010'
        ###    , '020, 030'
        ###    , '020, 050'
        ##    , '010, 010'
        ###    , '010, 030'
        ###    , '010, 050'
        ##    ]
        ##)
        ##
        ##msk =     (aux[colsObj.nct_tcc] != "010, 050") \
        ##        & (aux[colsObj.nct_tcc] != "020, 050") \
        ##        & (aux[colsObj.nct_tcc] != "030, 050") \
        ##        & (aux[colsObj.nct_tcc] != "010, 030") \
        ##        & (aux[colsObj.nct_tcc] != "020, 030") \
        ##        & (aux[colsObj.nct_tcc] != "030, 030")
        ##aux = aux[msk]
        ##
        ##sp = ScatterPlot(data=aux, x=colsObj.id, y=colsObj.value)
        ##sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_3.png")
