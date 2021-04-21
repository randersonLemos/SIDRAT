import numpy as np
from tardis_data_manager import TardisDataManager
from tardis_files_manager import TardisFilesManager


import shutil

tfm = TardisFilesManager(['DONE/RES_REF', 'DONE/RES_SPHERE'], '/media/beldroega/DATA/SIDRAT/tardis')
#tfm = TardisFilesManager(['DONE/RES_REF'], '/media/beldroega/DATA/SIDRAT/tardis')
#tfm = TardisFilesManager(['_RES_SPH_REF'], '/media/beldroega/DATA/SIDRAT/tardis')

tfm.clean(r'it_(\d+)')

files = tfm.files('.*/it_ultima.csv')

tdm = TardisDataManager(files)

### SOME TWEAKING ###
dic = {}
dic['df']  = tdm.df
dic['mco'] = tdm.mco
dic['Mco'] = tdm.Mco
dic['mex'] = tdm.mex
dic['Mex'] = tdm.Mex

for key in dic:
    df = dic[key]
    dic[key][['nsi', 'nsp', 'nct', 'tcc']] = df['mt'].str.split( '_\D\D\D', expand=True)[[1,2,4,5]]
    dic[key][['nsi_nsp']] = df['nsi'] + ', ' + df['nsp']
    dic[key][['nct_tcc']] = df['nct'] + ', ' + df['tcc']
    dic[key][['nnnt']] = df['nsi'] + ', ' + df['nsp'] + ', '  + df['nct'] + ', ' + df['tcc']
    dic[key]['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')

tdm.save('/media/beldroega/DATA/SHARED/SIDRAT/DATA')
