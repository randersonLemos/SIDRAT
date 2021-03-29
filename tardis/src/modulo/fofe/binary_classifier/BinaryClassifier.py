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

        for j in range(nmodels):
            stg  = '\n\n\n'
            stg += 'Model {}'.format(j)
            stg += '\n\n\n'
            print(stg)

            mo = Models.Neural_Network(input_shape=(nvariables, 1), epochs=15)
            mo.train(trd.Xos, trd.yo)
            probs = mo.classify(ted.Xs)
            probabilities += probs

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

        path_prj = cga(EA.PATH_PROJETO)
        path_res = '/'.join(cga(EA.PATH_RESULTADO).split('/')[:-1])
        path = path_prj + '/' + path_res + '/' + 'fofe.csv'
        if os.path.exists(path):
            cl.y[['PROBS', 'CLASS']].to_csv(path, mode='a', header=False)
        else:
            cl.y[['PROBS', 'CLASS']].to_csv(path, header=True)


        #import IPython; IPython.embed()
        #print("\nTRAIN DATA\n", file=open(path, "a"))
        #print(trd.Xy().to_string(), file=open(path, "a"))
        #print("\nTEST DATA\n", file=open(path, "a"))
        #print(ted.Xy().to_string(), file=open(path, "a"))
        #print(cl.y[['PROBS', 'CLASS']].to_string() + '\n', file=open(path, "a"))
        for ite, ide in index:
            del solucoes.solucoes[ite][ide]
 

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
