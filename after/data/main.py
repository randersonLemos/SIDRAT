import numpy as np
from tardis_data_manager import TardisDataManager
from tardis_files_manager import TardisFilesManager

import shutil

lst = []

#lst.append('WORK/RASTRIGIN_NNE032_SBA008')
#dirr = '/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA008'

lst.append('WORK/RASTRIGIN_NNE032_SBA004')
dirr = '/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA004'

#lst.append('WORK/ROSEMBROCK_NNE032_SBA008')
#dirr = '/media/beldroega/DATA/SHARED/csv/ROSEMBROCK_NNE032_SBA008'

tfm = TardisFilesManager(lst, '/media/beldroega/DATA/SIDRAT/tardis')

tfm = tfm.clean(r'it_(\d+)')

files = tfm.files('.*/it_ultima.csv')
#files = tfm.files('./IDLHC_NSI100_NSP020.*TCC(000|010).*/it_ultima.csv')
#files = tfm.files('./IDLHC_NSI100_NSP020.*TCC(000|010|020|030|040|050).*/it_ultima.csv')

tdm = TardisDataManager(files, add_probs=True, n_iter_convergence_criterio=3)

# ### SOME TWEAKING ###

columns = []
columns.append('NSI')
columns.append('NSP')
columns.append('NCT')
columns.append('TCC')
columns.append('NNE')
columns.append('SBA')

for key in tdm.dic:

    df = tdm.dic[key]

    for col in columns:
        df[col] = ''
        for mt in df.mt.unique():
            idx = mt.find(col)
            if idx != -1:
                vl = mt[idx + 3 : idx + 6]
                df.loc[df.mt == mt, col] = vl
            else:
                df.loc[df.mt == mt, col] = '0'

    df.columns = df.columns.str.lower()
    tdm.dic[key] = df

    #tdm.dic[key]['nnbc'] = np.where(df['nct'] == '000', 'Off', 'On')

tdm.save(dirr)
