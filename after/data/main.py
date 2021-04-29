import numpy as np
from tardis_data_manager import TardisDataManager
from tardis_files_manager import TardisFilesManager


import shutil

lst = []

lst.append('DONE/RES_SPH_REF')
lst.append('DONE/RES_SPH')
#lst.append('DONE/RES_RST_REF')
#lst.append('DONE/RES_RSB_REF')

tfm = TardisFilesManager(lst, '/media/beldroega/DATA/SIDRAT/tardis')
tfm.clean(r'it_(\d+)')

files = tfm.files('.*/it_ultima.csv')
#files = tfm.files('./IDLHC_NSI100_NSP020_NNBC_NCT020.*/it_ultima.csv')

tdm = TardisDataManager(files, probabilities=True, convergence=True)

# ### SOME TWEAKING ###
dic = {}
dic['df']  = tdm.df
dic['dfp'] = tdm.dfp
dic['mco'] = tdm.mco
dic['Mco'] = tdm.Mco
dic['mex'] = tdm.mex
dic['Mex'] = tdm.Mex

for key in dic:
    df = dic[key]
    dic[key][['nsi', 'nsp', 'nct', 'tcc']] = df['mt'].str.split(r'_\D\D\D', expand=True)[[1, 2, 4, 5]]
    dic[key][['nsi_nsp']] = df['nsi'] + ', ' + df['nsp']
    dic[key][['nct_tcc']] = df['nct'] + ', ' + df['tcc']
    dic[key][['nnnt']] = df['nsi'] + ', ' + df['nsp'] + ', '  + df['nct'] + ', ' + df['tcc']
    dic[key]['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')

tdm.save('/media/beldroega/DATA/SHARED/csv')
