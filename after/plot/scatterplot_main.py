import copy
import loader
import pandas as pd
import matplotlib.pyplot as plt


plt.close()


colsObj = loader.colsObj
mean_expand = loader.mean_expand


pv = pd.pivot_table(mean_expand
                    , index=[colsObj.mt
                             , colsObj.of
                             , colsObj.nsi
                             , colsObj.nsp
                             , colsObj.nct
                             , colsObj.tcc
                             , colsObj.nsi_nsp
                             , colsObj.nct_tcc
                             , colsObj.nnnt
                             , colsObj.nnbc
                            ]
                    , values=[colsObj.id, colsObj.value]
                    , aggfunc={colsObj.id : max, colsObj.value : max}
                   )

pv = pv.reset_index()

from configplot import ConfigPlot
from scatterplot import ScatterPlot

cp = ConfigPlot()
cp.set_hue(colsObj.nsi_nsp)
cp.set_sty(colsObj.nct_tcc)
cp.set_s(300)
cp.set_linewidth(2)
cp.set_alpha(0.70)
cp.set_palette({
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
)

cp.set_markers({
      '000, 000': 'o'
    , '010, 010': 's'
    , '010, 030': '^'
    , '010, 050': 'v'
    , '020, 010': 'P'
    , '020, 030': '*'
    , '020, 050': 'X'
    , '030, 010': '>'
    , '030, 030': '<'
    , '030, 050': 'D'
    }
)

cp.set_sty_order([
      '000, 000'
#    , '030, 010'
#    , '030, 030'
#    , '030, 050'
#    , '020, 010'
#    , '020, 030'
#    , '020, 050'
#    , '010, 010'
#    , '010, 030'
#    , '010, 050'
    ]
)

tlt  = ''
tlt  += 'Sphere function optimization using IDLHC with NNBC in different settings\n'
tlt  += 'Aver. final number of runs versus aver. max. obj. fun. values (5 trials)\n'
tlt  += 'Stop criterion of 30 iterations' 

xlb = 'Final number of runs'
ylb = 'Max obj. fun. values'

cp.set_title(tlt)
cp.set_xlabel(xlb)
cp.set_ylabel(ylb)

aux = copy.deepcopy(pv)
aux = aux.sort_values(by=colsObj.nnnt, ascending=False)

cp.set_ymin(mean_expand[colsObj.value].min()).set_ymax(mean_expand[colsObj.value].max())
cp.set_xmin(1).set_xmax(aux[colsObj.id].max())

sp = ScatterPlot(data=aux[aux[colsObj.nnbc] == 'Off'], x=colsObj.id, y=colsObj.value)
sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_0.png")

cp.set_sty_order([
      '000, 000'
    , '030, 010'
    , '030, 030'
    , '030, 050'
    , '020, 010'
    , '020, 030'
    , '020, 050'
    , '010, 010'
    , '010, 030'
    , '010, 050'
    ]
)

sp = ScatterPlot(data=aux, x=colsObj.id, y=colsObj.value)
sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_1.png")

msk =     (aux[colsObj.nsi_nsp] == "100, 020") \
        | (aux[colsObj.nsi_nsp] == "100, 030") \
        | (aux[colsObj.nsi_nsp] == "050, 010") \
        | (aux[colsObj.nsi_nsp] == "050, 020")
aux = aux[msk]

#vl = aux[aux[colsObj.nnnt] == '050, 010, 000, 000'][colsObj.value]
#msk = aux[colsObj.value] >= int(vl)
#aux = aux[msk]

cp.set_xmin(1).set_xmax(aux[colsObj.id].max())

sp = ScatterPlot(data=aux, x=colsObj.id, y=colsObj.value)
sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_2.png")

cp.set_sty_order([
      '000, 000'
    , '030, 010'
#    , '030, 030'
#    , '030, 050'
    , '020, 010'
#    , '020, 030'
#    , '020, 050'
    , '010, 010'
#    , '010, 030'
#    , '010, 050'
    ]
)

msk =     (aux[colsObj.nct_tcc] != "010, 050") \
        & (aux[colsObj.nct_tcc] != "020, 050") \
        & (aux[colsObj.nct_tcc] != "030, 050") \
        & (aux[colsObj.nct_tcc] != "010, 030") \
        & (aux[colsObj.nct_tcc] != "020, 030") \
        & (aux[colsObj.nct_tcc] != "030, 030")
aux = aux[msk]

sp = ScatterPlot(data=aux, x=colsObj.id, y=colsObj.value)
sp.plot(cp).save("/media/beldroega/DATA/SHARED/png/sphere_scatterplot_3.png")
