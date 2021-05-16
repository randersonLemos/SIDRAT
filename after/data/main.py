import numpy as np
from tardis_data_manager import TardisDataManager
from tardis_files_manager import TardisFilesManager

import shutil

lst = []

#lst.append('DONE/RES_SPH_REF')
#lst.append('DONE/RES_SPH')
lst.append('TESTE')

tfm = TardisFilesManager(lst, '/media/beldroega/DATA/SIDRAT/tardis')
tfm = tfm.clean(r'it_(\d+)')

files = tfm.files('.*/it_ultima.csv')
#files = tfm.files('./IDLHC_NSI100_NSP020.*TCC(000|010).*/it_ultima.csv')
#files = tfm.files('./IDLHC_NSI100_NSP020.*TCC(000|010|020|030|040|050).*/it_ultima.csv')

tdm = TardisDataManager(files, add_probs=True, n_iter_convergence_criterio=3)

# ### SOME TWEAKING ###
for key in tdm.dic:
    df = tdm.dic[key]

    tdm.dic[key][['nsi', 'nsp', 'nct', 'tcc']] = df['mt'].str.split(r'_\D\D\D', expand=True)[[1, 2, 4, 5]]

    tdm.dic[key][['nsi_nsp']] = df['nsi'] + ', ' + df['nsp']

    tdm.dic[key][['nct_tcc']] = df['nct'] + ', ' + df['tcc']

    tdm.dic[key][['nnnt']] = df['nsi'] + ', ' + df['nsp'] + ', '  + df['nct'] + ', ' + df['tcc']

    tdm.dic[key]['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')

dirr = '/media/beldroega/DATA/SHARED/csv'
tdm.save(dirr)

from nnbc_data_manager import NnbcDataManager


ndm = NnbcDataManager(dirr + '/pcov.csv')
