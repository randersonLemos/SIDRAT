import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close()

from scatterplot import ScatterPlot

sph = 'sph'
rst = 'rst'
rsb = 'rsb'

dfs = {}
dfs[sph] = pd.read_csv('/media/beldroega/DATA/SIDRAT/after/data/DATA_SPHERE/mdf.csv')
dfs[rst] = pd.read_csv('/media/beldroega/DATA/SIDRAT/after/data/DATA_RASTRIGIN/mdf.csv')
dfs[rsb] = pd.read_csv('/media/beldroega/DATA/SIDRAT/after/data/DATA_ROSENBROCK/mdf.csv')

value   = 'value'
nsi     = 'IDLHC: nsi     '
nsp     = 'IDLHC: nsp     '
nct     = 'NNBC: nct      '
tcc     = 'NNBC: tcc      '
nsi_nsp = 'IDLHC: nsi, nsp'
nct_tcc = 'NNBC: nct, tcc '
nnnt    = 'IDLHC: nsi, nsp NNBC nct, tcc'
nnbc    = 'NNBC: state    '

def get_pv(df):
    df[[nsi, nsp, nct, tcc]] = df['mt'].str.split('_\D\D\D', expand=True).iloc[:, [1, 2, 4, 5]]
    df[nsi_nsp] = df[nsi] + ', ' + df[nsp]
    df[nct_tcc] = df[nct] + ', ' + df[tcc]

    df[nnbc] = '-1'
    df.loc[df[nct_tcc] == '99, 99', nnbc] = 'OFF'
    df.loc[df[nct_tcc] != '99, 99', nnbc] = 'ON'

    df.loc[df[nct] == '99', nct] = 'XX'
    df.loc[df[tcc] == '99', tcc] = 'XX'
    df.loc[df[nct_tcc] == '99, 99', nct_tcc] = 'XX, XX'

    df[nnnt] = df[nsi_nsp] + ', ' + df[nct_tcc]

    pv = pd.pivot_table(df
                       , index=['mt', 'of', nsi, nsp, nct, tcc, nsi_nsp, nct_tcc, nnnt, nnbc]
                       , values=['id', 'value']
                       , aggfunc='max'
                       ).reset_index()
    return pv


tlts = {}

tlt  = ''
tlt  += 'Sphere function optimization using IDLHC integrated with NNBC\n'
tlt  += 'Final number of runs versus final max. value of obj. fun.\n'
tlt  += 'Mean of 5 trials'

tlts[sph] = tlt

tlt  = ''
tlt  += 'Rastrigin function optimization using IDLHC integrated with NNBC\n'
tlt  += 'Final number of runs versus final max. value of obj. fun.\n'
tlt  += 'Mean of 5 trials'

tlts[rst] = tlt

tlt  = ''
tlt  += 'Rosenbrock function optimization using IDLHC integrated with NNBC\n'
tlt  += 'Final number of runs versus final max. value of obj. fun.\n'
tlt  += 'Mean of 5 trials'
 
tlts[rsb] = tlt


for key in dfs:
    pv = get_pv(dfs[key])

    sc = ScatterPlot(data=pv, x='id', y='value')
    sc.set_xmin(0).set_xmax(None).set_ymin(None).set_ymax(0)

    tlt = tlts[key]
    nfile = './fig/seq1/{}'.format(key)

    sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')

    sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
    sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
    sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')

    sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
    sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
    sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')


for key in dfs:
    pv = get_pv(dfs[key])

    xmin = 0
    xmax = None
    ymin = pv['value'].min()
    ymax = 0

    mk = (pv[tcc] == '10') | \
         (pv[tcc] == '30') | \
         (pv[tcc] == '50') | \
         (pv[tcc] == 'XX')
    pv = pv[mk]

    #mk = (pv[nsi_nsp] != '50, 30')
    #pv = pv[mk]

    #mk = (pv[nsi_nsp] != '50, 10')
    #pv = pv[mk]

    sc = ScatterPlot(data=pv, x='id', y='value')
    sc.set_xmin(xmin).set_xmax(xmax).set_ymin(ymin).set_ymax(ymax)

    tlt = tlts[key]
    nfile = './fig/seq2/{}'.format(key)

    sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')

    sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
    sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
    sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')

    sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
    sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
    sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')


for key in dfs:
    pv = get_pv(dfs[key])

    xmin = 0
    xmax = None
    ymin = pv['value'].min()
    ymax = 0

    mk = (pv[tcc] == '10') | \
         (pv[tcc] == '30') | \
         (pv[tcc] == '50') | \
         (pv[tcc] == 'XX')
    pv = pv[mk]

    mk = (pv[nsi_nsp] != '50, 30')
    pv = pv[mk]

    mk = (pv[nsi_nsp] != '100, 10')
    pv = pv[mk]

    mk = (pv[nsi_nsp] != '150, 10')
    pv = pv[mk]

    #mk = (pv[nsi_nsp] != '50, 10')
    #pv = pv[mk]

    sc = ScatterPlot(data=pv, x='id', y='value')
    sc.set_xmin(xmin).set_xmax(xmax).set_ymin(ymin).set_ymax(ymax)

    tlt = tlts[key]
    nfile = './fig/seq3/{}'.format(key)

    sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')

    sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
    sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
    sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')

    sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
    sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
    sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')


#for vl in ['50', '100', '150']:
#
#    for key in dfs:
#        pv = get_pv(dfs[key])
#
#        mk = pv[nsi] == vl
#        pv = pv[mk]
#
#        sc = ScatterPlot(data=pv, x='id', y='value')
#        sc.set_xmin(0).set_xmax(None).set_ymin(None).set_ymax(0)
#
#        tlt = tlts[key]
#        nfile = './fig/seq1_{}/{}'.format(vl, key)
#
#        sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')
#
#        sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
#        sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
#        sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')
#
#        sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
#        sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
#        sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')
#
#
#    for key in dfs:
#        pv = get_pv(dfs[key])
#
#        mk = pv[nsi] == vl
#        pv = pv[mk]
# 
#        xmin = 0
#        xmax = None
#        ymin = pv['value'].min()
#        ymax = 0
#
#        mk = (pv[tcc] == '10') | \
#             (pv[tcc] == '30') | \
#             (pv[tcc] == '50') | \
#             (pv[tcc] == 'XX')
#        pv = pv[mk]
#
#        #mk = (pv[nsi_nsp] != '50, 30')
#        #pv = pv[mk]
#
#        #mk = (pv[nsi_nsp] != '50, 10')
#        #pv = pv[mk]
#
#        sc = ScatterPlot(data=pv, x='id', y='value')
#        sc.set_xmin(xmin).set_xmax(xmax).set_ymin(ymin).set_ymax(ymax)
#
#        tlt = tlts[key]
#        nfile = './fig/seq2_{}/{}'.format(vl, key)
#
#        sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')
#
#        sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
#        sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
#        sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')
#
#        sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
#        sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
#        sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')
#
#
#    for key in dfs:
#        pv = get_pv(dfs[key])
#
#        mk = pv[nsi] == vl
#        pv = pv[mk]
#
#        xmin = 0
#        xmax = None
#        ymin = pv['value'].min()
#        ymax = 0
#
#        mk = (pv[tcc] == '10') | \
#             (pv[tcc] == '30') | \
#             (pv[tcc] == '50') | \
#             (pv[tcc] == 'XX')
#        pv = pv[mk]
#
#        mk = (pv[nsi_nsp] != '50, 30')
#        pv = pv[mk]
#
#        mk = (pv[nsi_nsp] != '50, 10')
#        pv = pv[mk]
#
#        mk = (pv[nct_tcc] != '10, 50')
#        pv = pv[mk]
#     
#        sc = ScatterPlot(data=pv, x='id', y='value')
#        sc.set_xmin(xmin).set_xmax(xmax).set_ymin(ymin).set_ymax(ymax)
#
#        tlt = tlts[key]
#        nfile = './fig/seq3_{}/{}'.format(vl, key)
#
#        sc.set_hue(nsi_nsp).set_stl(nct_tcc).set_tlt(tlt).plot_1().save(nfile + '1.png')
#
#        sc.set_hue(nsi_nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '2.png')
#        sc.set_hue(nsi).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '3.png')
#        sc.set_hue(nsp).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '4.png')
#
#        sc.set_hue(nct_tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '5.png')
#        sc.set_hue(nct).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '6.png')
#        sc.set_hue(tcc).set_stl(nnbc).set_tlt(tlt).plot_1().save(nfile + '7.png')