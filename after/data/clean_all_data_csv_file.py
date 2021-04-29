import numpy as np
import pandas as pd


dfs = {}

dfs['all_data'] = pd.read_csv('/media/beldroega/DATA/SHARED/csv/all_data.csv')
dfs['zall_data'] = pd.read_csv('/media/beldroega/DATA/SHARED/csv/zall_data.csv')

for key, df in dfs.items():
    df = df.set_index(['mt', 'of', 'ru'])
    lst = []
    for idx in df.index.unique():
        aux = df.loc[idx]
        aux = aux.reset_index().set_index(['it'])
        pvl = vl = 0
        count = 0
        for jdx in aux.index.unique():
            vl = aux.loc[jdx]['value'].max()
            if vl == pvl:
                count += 1
                if count == 3 - 1:
                    break
            else:
                count = 0
            pvl = vl
        lst.append(aux.loc[:jdx].reset_index())

    df = pd.concat(lst).reset_index(drop=True)

    try:
        df = df[['mt', 'of', 'ru', 'it', 'id', 'value', 'prob', 'class', '_type', '_id']]
    except Exception:
        df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

    df[['nsi', 'nsp', 'nct', 'tcc']] = df['mt'].str.split(r'_\D\D\D', expand=True)[[1, 2, 4, 5]]
    df[['nsi_nsp']] = df['nsi'] + ', ' + df['nsp']
    df[['nct_tcc']] = df['nct'] + ', ' + df['tcc']
    df[['nnnt']] = df['nsi'] + ', ' + df['nsp'] + ', '  + df['nct'] + ', ' + df['tcc']
    df['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')

    df.to_csv("/media/beldroega/DATA/SHARED/csv/{}_convergence.csv".format(key), index=False)
