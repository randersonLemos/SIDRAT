"""
:author: Randerson Lemos
:data: 01/01/2021
"""

import os
import numpy as np
import pandas as pd

from src.contexto.Contexto import EnumAtributo
from src.modulo.fofe.FofePadrao import FofePadrao
import src.modulo.fofe.binary_classifier.Data as Data


from sklearn import preprocessing
from imblearn.over_sampling import SMOTE, SVMSMOTE, BorderlineSMOTE, ADASYN

Data.Aux.oversampler = BorderlineSMOTE()
Data.Aux.scaler = preprocessing.MinMaxScaler()

import src.modulo.fofe.binary_classifier.Models as Models


class BinaryClassifier(FofePadrao):
    """
    FOFE baseda em classificador binário para identificação (prévia) de soluções
    que valem apena ser simuladas
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        EA = EnumAtributo

        if EA.NN_BINARY_CLASSIFIER_NCLASS1 not in self._necessidade:
            self._necessidade.append(EA.NN_BINARY_CLASSIFIER_NCLASS1)

        if EA.NN_BINARY_CLASSIFIER_NMODELS not in self._necessidade:
            self._necessidade.append(EA.NN_BINARY_CLASSIFIER_NMODELS)

        if EA.NN_BINARY_CLASSIFIER_THRESHOLD not in self._necessidade:
            self._necessidade.append(EA.NN_BINARY_CLASSIFIER_THRESHOLD)


    def run(self, contexto):

        self._contexto = contexto

        EA = EnumAtributo
        cga = self._contexto.get_atributo
        csa = self._contexto.set_atributo

        iteracao_corrente = cga(EA.AVALIACAO_ITERACAO_AVALIAR)

        if self._aplicar_fofe(iteracao_corrente):
            solucoes = cga(EA.SOLUCOES)
            nclass1 = cga(EA.NN_BINARY_CLASSIFIER_NCLASS1)
            nmodels = cga(EA.NN_BINARY_CLASSIFIER_NMODELS)
            threshold = cga(EA.NN_BINARY_CLASSIFIER_THRESHOLD)
            npopulation = len(solucoes.solucoes[iteracao_corrente])

            key = list(solucoes.solucoes[iteracao_corrente])[0]
            nvariables = len(solucoes.solucoes[iteracao_corrente][key].variaveis._variaveis['VARIAVEL'])

            solucoes = self._run(iteracao_corrente
                                 , solucoes
                                 , threshold
                                 , nclass1
                                 , nmodels
                                 , npopulation
                                 , nvariables
                                )

            csa(EA.SORTEIO_SOLUCOES_NOVAS, solucoes, True)
 

    def _aplicar_fofe(self, iteracao_corrente):
        return iteracao_corrente > 1


    def _run(self, iteracao_corrente, solucoes, threshold, nclass1, nmodels, npopulation, nvariables):
        EA = EnumAtributo
        cga = self._contexto.get_atributo

        index, X, y = self._para_dataframe(solucoes)


        IS = pd.IndexSlice

        trd = Data.TrainData(X.loc[IS[:iteracao_corrente - 1, :] , :], y.loc[IS[:iteracao_corrente - 1, :], :]
                , iteracao_corrente - 1
                , nclass1
                )

        ted = Data.TestData( X.loc[IS[iteracao_corrente, :], :], y.loc[IS[iteracao_corrente, :], :]
                , iteracao_corrente
                )

        probabilities = np.zeros((npopulation, 1), dtype='float32')

        import time
        start_time = time.time()

        for j in range(nmodels):
            stg  = '---\n'
            stg += '---\n'
            stg += '---\n'
            stg += 'Iteração {}\n'.format(iteracao_corrente)
            stg += 'Model {}\n'.format(j)
            stg  = '---\n'
            stg += '---\n'
            stg += '---'
            print(stg)

            mo = Models.Neural_Network(input_shape=(nvariables, 1), epochs=20)
            index = trd.Xo.sample(frac=1).index  # Shuffling data
            mo.train(trd.Xos.loc[index, :], trd.yo.loc[index])
            probs = mo.classify(ted.Xs)
            probabilities += probs

        final_time = time.time() - start_time

        probabilities /= nmodels

        cl = Data.ClassifiedData(ted, probabilities, threshold)
        cl.y = cl.y.sort_values('PROBS', ascending=False)


        min_samples = cga(EA.OTIMIZACAO_IDLHC_AMOSTRAS_PDF)
        count = 0
        for ite, ide in cl.y.index:
            if count < min_samples:
                if cl.y.loc[(ite, ide), 'CLASS'] == 0:
                    cl.y.loc[(ite, ide), 'CLASS'] = 2
            else:
                break
            count += 1


        index = cl.y[cl.y['CLASS'] == 0].index
        for ite, ide in index:
            del solucoes.solucoes[ite][ide]
 

        ### CODE ADDED JUST FOR SAVE ALL SAMPLES ###
        path_prj = cga(EA.PATH_PROJETO)
        path_res = '/'.join(cga(EA.PATH_RESULTADO).split('/')[:-1])


        path = path_prj + '/' + path_res + '/' + 'ztraining_time.txt'
        if iteracao_corrente == 2:
            print('{}'.format(final_time), file=open(path, mode='w'))
        else:
            print('{}'.format(final_time), file=open(path, mode='a'))
 

        Xy = ted.X.copy()
        Xy[cl.y.columns] = cl.y.copy()

        path = path_prj + '/' + path_res + '/' + 'zall_samples.csv'
        if iteracao_corrente == 2:
            Xy.to_csv(path, header=True)
        else:
            Xy.to_csv(path, mode='a', header=False)
        ###


        return solucoes


    def _para_dataframe(self, solucoes):

        ite_qualquer = list(solucoes._solucoes.keys())[0]
        ide_qualquer = list(solucoes._solucoes[ite_qualquer].keys())[0]
        sol_qualquer = solucoes._solucoes[ite_qualquer][ide_qualquer]

        vars_nome = list(sol_qualquer._variaveis._variaveis['VARIAVEL'].keys())
        vars_dict = {}
        for nome in vars_nome:
            vars_dict[nome] = []

        ofs_dict = {}
        for nome in sol_qualquer.of:
            ofs_dict[nome] = []

        ids_dict = {}
        ids_dict['ITE'] = []
        ids_dict['IDE'] = []

        for iteracao in solucoes._solucoes:
            for ide in solucoes._solucoes[iteracao]:
                solucao = solucoes._solucoes[iteracao][ide]

                variaveis = solucao._variaveis._variaveis['VARIAVEL']

                for nome in variaveis:
                    vars_dict[nome].append(variaveis[nome].valor)

                for nome in solucao.of:
                    ofs_dict[nome].append(solucao.of[nome].valor)

                ids_dict['ITE'].append(iteracao)
                ids_dict['IDE'].append(ide)

        index = pd.MultiIndex.from_frame(pd.DataFrame.from_dict(ids_dict))

        X = pd.DataFrame.from_dict(vars_dict)
        X.index = index
        X.columns = X.columns.str.upper()

        y = pd.DataFrame.from_dict(ofs_dict)
        y.index = index
        y.columns = y.columns.str.upper()

        return index, X, y
