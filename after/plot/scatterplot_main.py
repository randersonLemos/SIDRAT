import copy
import loader
import pandas as pd
import matplotlib.pyplot as plt

plt.close()

dic = {}
dic['mt'] = 'mt'
dic['of'] = 'of'
dic['id'] = 'id'
dic['value'] = 'Final max. obj. fun. value'
dic['n_sample'] = 'Number of runs'
dic['nsi'] = 'nsi'
dic['nsp'] = 'nsp'
dic['nct'] = 'nct'
dic['tcc'] = 'tcc'
dic['nsi_nsp'] = 'NSI, NSP'
dic['nct_tcc'] = 'NCT, TCC'
dic['nnnt'] = 'IDLHC and NNBC: nsi, nsp, nct, tcc'
dic['nnbc'] = ' NNBC: state'

class Columns:
    def __init__(self, dic):
        self.dic = dic

        for var in dic:
            exec("self.{} = '{}'".format(var, dic[var]))

    
    def __call__(self):
        return self.dic


    def __repr__(self):
        stg = self.dic.__repr__()
        stg = stg.replace(',', '\n')
        return stg


colsObj = Columns(dic)


mean_compact = loader.mean_compact
mean_compact = mean_compact.rename(columns=colsObj())

for var in ['nsi', 'nsp', 'nct', 'tcc']:
    mean_compact[dic[var]] = mean_compact[dic[var]].astype('str')

pv = pd.pivot_table(mean_compact
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
                    , values=[colsObj.n_sample, colsObj.value]
                    , aggfunc={colsObj.n_sample:sum, colsObj.value:max}
                   )

pv = pv.reset_index()

pv = pv[pv[colsObj.tcc] != '70']

pv = pv.sort_values(by=[colsObj.nnnt], ascending=True)

from scatterplot import ScatterPlot
from scatterplot import ScatterPlotConfig

spc = ScatterPlotConfig()
spc.set_hue(colsObj.nsi_nsp)
spc.set_sty(colsObj.nct_tcc)
spc.set_s(500)
spc.set_linewidth(2)
spc.set_palette({
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

spc.set_markers({
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

spc.set_sty_order([
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
#spc.set_siz(colsObj.nnbc)
#spc.set_sizs((300, 600, ))

tlt  = ''
tlt  += 'Sphere function optimization using IDLHC with NNBC in different settings\n'
tlt  += 'Ave. final number of runs versus ave. final max. obj. fun. value (5 trials)\n'
tlt  += 'Stop criterion of 30 iterations' 

aux = copy.deepcopy(pv)


spc.set_xmin(0).set_xmax(aux[colsObj.n_sample].max())
spc.set_ymax(0).set_ymin(aux[colsObj.value].min())

sp1 = ScatterPlot(data=aux, x=colsObj.n_sample, y=colsObj.value)
sp1.plot(tlt, spc).save("./fig/sphere_func_0.png")

msk =     (aux[colsObj.nsi_nsp] == "100, 020") \
        | (aux[colsObj.nsi_nsp] == "100, 030") \
        | (aux[colsObj.nsi_nsp] == "050, 010") \
        | (aux[colsObj.nsi_nsp] == "050, 020")
aux = aux[msk]

vl = aux[aux[colsObj.nnnt] == '050, 010, 000, 000'][colsObj.value]
msk = aux[colsObj.value] >= int(vl)
aux = aux[msk]

spc.set_xmin(0).set_xmax(aux[colsObj.n_sample].max())
spc.set_ymax(0).set_ymin(aux[colsObj.value].min())

sp1 = ScatterPlot(data=aux, x=colsObj.n_sample, y=colsObj.value)
sp1.plot(tlt, spc).save("./fig/sphere_func_1.png")

spc.set_sty_order([
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
sp1 = ScatterPlot(data=aux, x=colsObj.n_sample, y=colsObj.value)
sp1.plot(tlt, spc).save("./fig/sphere_func_2.png")
