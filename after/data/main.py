import numpy as np
from tardis_data_manager import TardisDataManager
from tardis_files_manager import TardisFilesManager

import shutil

lst = []

lst.append('DONE/RES_SPH_REF')
lst.append('DONE/RES_SPH')

tfm = TardisFilesManager(lst, '/media/beldroega/DATA/SIDRAT/tardis')
tfm = tfm.clean(r'it_(\d+)')

#files = tfm.files('.*/it_ultima.csv')
files = tfm.files('./IDLHC_NSI100_NSP030.*TCC(000|010).*/it_ultima.csv')

tdm = TardisDataManager(files, add_probs=True, n_iter_convergence_criterio=3)

## ### SOME TWEAKING ###
#dic = {}
#dic['df']  = tdm.df
#dic['dfp'] = tdm.dfp
#dic['mco'] = tdm.mco
#dic['Mco'] = tdm.Mco
#dic['mex'] = tdm.mex
#dic['Mex'] = tdm.Mex
#
#for key in dic:
#    df = dic[key]
#    dic[key][['nsi', 'nsp', 'nct', 'tcc']] = df['mt'].str.split(r'_\D\D\D', expand=True)[[1, 2, 4, 5]]
#    dic[key][['nsi_nsp']] = df['nsi'] + ', ' + df['nsp']
#    dic[key][['nct_tcc']] = df['nct'] + ', ' + df['tcc']
#    dic[key][['nnnt']] = df['nsi'] + ', ' + df['nsp'] + ', '  + df['nct'] + ', ' + df['tcc']
#    dic[key]['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')
#
#tdm.save('/media/beldroega/DATA/SHARED/csv')
