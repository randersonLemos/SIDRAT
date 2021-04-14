import loader
import pandas as pd
import matplotlib.pyplot as plt


dic = {}
dic['mt'] = 'mt'
dic['of'] = 'of'
dic['id'] = 'id'
dic['value'] = 'vl'
dic['n_sample'] = 'num. sample'
dic['nsi'] = 'nsi'
dic['nsp'] = 'nsp'
dic['nct'] = 'ncp'
dic['tcc'] = 'tcc'


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

pv = pd.pivot_table(mean_compact
                    , index=[colsObj.mt, colsObj.of]
                    , values=[colsObj.n_sample, colsObj.value]
                    , aggfunc={colsObj.n_sample:sum, colsObj.value:max}
                   )


from scatterplot import ScatterPlot
sc = ScatterPlot(data=pv, x=colsObj.n_sample, y=colsObj.value)

#sc.set_xmin(0).set_xmax(None).set_ymin(None).set_ymax(0)
#
#tlt = tlts[key]
#nfile = './fig/seq1/{}'.format(key)
#
#sc.set_hue(nct).set_stl(tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')
