import loader
import pandas as pd
import matplotlib.pyplot as plt

plt.close()

dic = {}
dic['mt'] = 'mt'
dic['of'] = 'of'
dic['id'] = 'id'
dic['value'] = 'vl'
dic['n_sample'] = 'num. sample'
dic['nsi'] = 'nsi'
dic['nsp'] = 'nsp'
dic['nct'] = 'nct'
dic['tcc'] = 'tcc'
dic['nsi_nsp'] = 'IDLHC: nsi, nsp'
dic['nct_tcc'] = 'nct, tcc'
dic['nnnt'] = 'IDLHC and NNBC: nsi, nsp, nct, tcc'
dic['nnbc'] = 'NNBC: state'

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

pv = pv.sort_values(by=[colsObj.nnnt], ascending=True)

from scatterplot import ScatterPlot
from scatterplot import ScatterPlotConfig

spc = ScatterPlotConfig()
spc.set_hue(colsObj.nsi_nsp)
spc.set_sty(colsObj.nnbc)
spc.set_siz(colsObj.nnbc)
spc.set_sizs((300, 600, ))
spc.set_linewidth(1)
spc.set_markers({'On': '^', 'Off': 'v'})
spc.set_palette(['aqua', 'royalblue', 'midnightblue', 'lightgreen', 'olivedrab', 'darkgreen', 'rosybrown', 'tomato', 'darkred'])
spc.set_xmin(0)
spc.set_ymax(0)

spcC = spc.copy()
spcC.set_hue(colsObj.nct_tcc)
spcC.set_palette(None)

sp = ScatterPlot(data=pv, x=colsObj.n_sample, y=colsObj.value)
sp.plot('Title 1', spc)

sp.plot('Title 1', spcC)
plt.show()

#sc.set_xmin(0).set_xmax(None).set_ymin(None).set_ymax(0)
#
#tlt = tlts[key]
#nfile = './fig/seq1/{}'.format(key)
#
#sc.set_hue(nct).set_stl(tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')
