from tardis_files_manager import TardisFilesManager
from tardis_data_manager import TardisDataManager


import shutil

tfm = TardisFilesManager(['RES_REF', 'RES_SPHERE'], '/media/beldroega/DATA/SIDRAT/tardis')

tfm.clean(r'it_(\d+)')

files = tfm.files('.*/it_ultima.csv')

tdm = TardisDataManager(files)

### SOME TWEAKING ###
tdm.df[['nsi', 'nsp', 'nct', 'tcc']]  =  tdm.df['mt'].str.split('_\D\D\D', expand=True)[[1,2,4,5]]
tdm.mco[['nsi', 'nsp', 'nct', 'tcc']] = tdm.mco['mt'].str.split('_\D\D\D', expand=True)[[1,2,4,5]]
tdm.Mco[['nsi', 'nsp', 'nct', 'tcc']] = tdm.Mco['mt'].str.split('_\D\D\D', expand=True)[[1,2,4,5]]

tdm.mex[['nsi', 'nsp', 'nct', 'tcc']] = tdm.mex['mt'].str.split('_\D\D\D', expand=True)[[1,2,4,5]]
tdm.Mex[['nsi', 'nsp', 'nct', 'tcc']] = tdm.Mex['mt'].str.split('_\D\D\D', expand=True)[[1,2,4,5]]
###

tdm.save('/media/beldroega/DATA/SHARED/SIDRAT/DATA')
