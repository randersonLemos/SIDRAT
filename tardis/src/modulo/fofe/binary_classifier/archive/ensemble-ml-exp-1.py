import os
if os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) not in os.sys.path: os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from simulation.manager.otm_manager_file import OtmManagerFile
from simulation.manager.otm_manager_data import OtmManagerData

OtmManagerFile.set_default_simulation_folder_prefix('otm_IT')
OtmManagerFile.set_default_simulation_file_prefix('run')
OtmManagerFile.set_default_result_file('otm.otm.csv')
OtmManagerFile.set_default_hldg_sample_file('hldg.txt')

import pandas as pd

from Data import *

from sklearn import preprocessing
from imblearn.over_sampling import SMOTE, SVMSMOTE, BorderlineSMOTE, ADASYN

Aux.oversampler = BorderlineSMOTE()
Aux.scaler = preprocessing.MinMaxScaler()

from Models import *

from Registers import *

plt.close()

if __name__ == "__main__":

    Num_models  = 10

    Threshold = np.linspace(0.10, 0.50, 9)
    Num_class_1 = np.linspace(10, 20, 3).astype('int')

    omd = OtmManagerData()
    omd.add_omf('18WIDE'
            , OtmManagerFile(project_root='/media/beldroega/DATA/DRIVE/TRANSFER/OTM_GOR_ICV1_WIDE18_1')
            )

    X, y = omd.data()
    I = pd.IndexSlice

    import itertools
    for threshold, num_class_1 in itertools.product(Threshold, Num_class_1):

        num_class_0 = 0
        num_best_samples = 0

        out_folder = 'NUM_CLASS_1_{}_THRESHOLD_{}'.format(num_class_1, (100*threshold).astype('int'))
        try:
            os.mkdir(out_folder)
        except FileExistsError:
            pass

        Trd = []
        Ted = []
        Cld = []

        mask = pd.Series(True, index=X.loc[I[:, 1, :], :].index, name='CLASS')
        for i in range(1, 20):
            stg  = '>\n>\n>\n>\n>\n'
            stg += 'Traning with iteration {} and classification of iteration {}\n'.format(i, i+1)
            stg += '<\n<\n<\n<\n<\n'
            print(stg)

            iteration = i

            trd = TrainData(X.loc[I[:, :iteration, :], :], y.loc[I[:, :iteration, :], :]
                    , iteration
                    , mask
                    , num_class_1
                    )

            ted = TestData( X.loc[I[:,  iteration + 1, :], :], y.loc[I[:,  iteration + 1, :], :]
                    , iteration + 1
                    )

            probabilities = np.zeros((100, 1), dtype='float32')
            for j in range(Num_models):
                stg  = '\n\n\n'
                stg += 'Model {}'.format(j)
                stg += '\n\n\n'
                print(stg)

                mo = Neural_Network(input_shape=(27, 1), epochs=15)
                mo.train(trd.Xos, trd.yo)
                probs = mo.classify(ted.Xs)
                probabilities += probs

            probabilities /= Num_models

            cld = ClassifiedData(ted, probabilities, threshold)
            save(trd, ted, cld, out_folder)

            _mask = (cld.y['CLASS'] == 1)
            mask = mask.append(_mask)

            num_class_0 += (cld.y['CLASS'] == 0).sum()
            num_best_samples += cld.y['CLASS'].iloc[:20].sum()

            Trd.append(trd)
            Ted.append(ted)
            Cld.append(cld)


        import pickle
        pickle.dump([Trd, Ted, Cld], open("{}/store.pkl".format(out_folder), "wb"))

        print('NUM_CLASS_0 {}'.format(num_class_0)
                , file=open('{}/out.txt'.format(out_folder), 'w'))
        print('NUM_BEST_SAMPLES {}'.format(num_best_samples)
                , file=open('{}/out.txt'.format(out_folder), 'a'))
