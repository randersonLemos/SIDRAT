import re
import pathlib
import numpy as np
import pandas as pd


class TardisDataManager:
    def __init__(self, filepaths, add_probs=False, n_iter_convergence_criterio=0, fix_shape=True):
        self.filepaths = filepaths
        self.add_probs = add_probs


        self.ori = self.load()
        if self.add_probs:
            self.pori = self.pload()


        if n_iter_convergence_criterio:
            self.cov = self.apply_n_iter_convergence_criterio(self.ori, n_iter_convergence_criterio)
            if self.add_probs:
                self.pcov = self.apply_n_iter_convergence_criterio(self.pori, n_iter_convergence_criterio)
        else:
            self.cov = self.ori
            if self.add_probs:
                self.pcov = self.cov


        if fix_shape:
            if self.add_probs:
                self.ori = self.fix_shape(self.pori, self.ori)
                self.cov = self.fix_shape(self.pcov, self.cov)

                self.pori = self.fix_shape(self.pori, self.pori)
                self.pcov = self.fix_shape(self.pcov, self.pcov)
            else:
                self.ori = self.fix_shape(self.ori, self.ori)
                self.cov = self.fix_shape(self.cov, self.cov)


        self.mco = self.mean_compact(self.ori)
        self.mcc = self.mean_compact(self.cov)
        self.mxo = self.mean_expand(self.mco)
        self.mxc = self.mean_expand(self.mcc)


        self.dic = {}
        self.dic['ori'] = self.ori
        self.dic['cov'] = self.cov
        self.dic['mco'] = self.mco
        self.dic['mcc'] = self.mcc
        self.dic['mxo'] = self.mxo
        self.dic['mxc'] = self.mxc

        if add_probs:
            self.dic['pori'] = self.pori
            self.dic['pcov'] = self.pcov


    def load(self):
        lst = []
        for filepath in self.filepaths:

            print('Loading: {}'.format(filepath))

            df = pd.read_csv(filepath, sep=';')
            if df.shape[1] == 1:
                df = pd.read_csv(filepath, sep=',')

            df = df.iloc[1:, [0, 1, 3]]

            df['of'] = df.columns[2][7:-1]
            df['_type'] = df.columns[2][3:6]
            df = df.rename(columns={  'iteracao': 'it'
                                    , df.columns[2]: 'value'
                                    , 'id': '_id'
                                    , 'probs': 'prob'
                                   })
            df['id'] = df.index
            df['mt'] = filepath.parent.name[:-3]
            df['ru'] = filepath.parent.name[-2:]
            
            lst.append(df)

        df = pd.concat(lst)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(how='any')
        df = df.reset_index()

        df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

        return df


    def apply_n_iter_convergence_criterio(self, df, n_iter_convergence_criterio):
        columns = df.columns.tolist()

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

        return df[columns]


    def fix_shape(self, reference, destiny):
        ref = reference.copy()
        des = destiny.copy()

        columns = des.columns.tolist()

        ref = ref.set_index(['mt', 'of'])
        des = des.set_index(['mt', 'of'])
        lst = []
        for idx in ref.index.unique():
            rux = ref.loc[idx]
            pt = rux.pivot_table(index=['mt', 'of', 'ru'], columns='it', values='value')
            mit = pt.T.dropna().index.max()

            dux = des.loc[idx]
            msk = dux['it'] <= mit
            lst.append(dux[msk].reset_index())

        df = pd.concat(lst)[columns]

        return df


    def mean_compact(self, df):
        pt = pd.pivot_table(df
                           , index=['mt', 'of', 'ru', 'it']
                           , values=['value']
                           , aggfunc=['count', 'max']
                           )


        pt.columns = pt.columns.droplevel(1)


        pt = pt.rename(columns={'count':'n_sample', 'max':'value'})

        pt = pt.reset_index()


        gb = pt.groupby(['mt', 'of', 'it']).mean().astype('int').reset_index()
        gb = gb.reset_index()

        return gb


    def mean_expand(self, mc):
        lst = []
        mc = mc.set_index(['mt', 'of'])
        for index in mc.index.unique():
            se = mc.loc[index, 'n_sample'].reset_index(drop=True)
            df = pd.DataFrame(index=range(se.sum()))
            df['mt'] = index[0]
            df['of'] = index[1]
            df['it'] = -1
 
            bng = 0
            end = 0
            for indexx in se.index:
                end = bng + se[indexx]
                df.loc[bng: end, 'it'] = indexx + 1
                bng = end

            lst.append(df)

        df = pd.concat(lst).reset_index()

        df = df.rename(columns={'index': 'id'})
        df['id'] = df['id'] + 1
        df = df[['mt', 'of', 'it', 'id']]

        df['value'] = -1
        df = df.set_index(['mt', 'of', 'it'])

        mc = mc.reset_index().set_index(['mt', 'of', 'it'])
        for index in df.index.unique():
            #print(index)
            df.loc[index, 'value'] = mc.loc[index, 'value'].astype('int')

        return df.reset_index()


    def pload(self):
        lst = []
        for filepath in self.filepaths:

            print('Loading: {}'.format(filepath))

            df = pd.read_csv(filepath, sep=";")
            if df.shape[1] == 1:
                df = pd.read_csv(filepath, sep=",")

            sucess, df = self._try_add_probabilities(df, filepath.parent / 'zall_samples.csv')

            if sucess:
                df = df.iloc[1:, [0, 1, 3, -2, -1]]
            else:
                df = df.iloc[1:, [0, 1, 3]]

            df['of'] = df.columns[2][7:-1]
            df['_type'] = df.columns[2][3:6]
            df = df.rename(columns={  'iteracao': 'it'
                                    , df.columns[2]: 'value'
                                    , 'id': '_id'
                                    , 'probs': 'prob'
                                   })

            df['id'] = df.index
            df['mt'] = filepath.parent.name[:-3]
            df['ru'] = filepath.parent.name[-2:]
 
            if sucess:
                df = df[['mt', 'of', 'ru', 'it', 'id', 'value', 'prob', 'class', '_type', '_id']]
            else:
                df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

            lst.append(df)

        df = pd.concat(lst)
        df = df.fillna(1)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(how='any')
        df = df.reset_index()

        try:
            df = df[['mt', 'of', 'ru', 'it', 'id', 'value', 'prob', 'class', '_type', '_id']]
        except KeyError:
            df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

        return df


    def save(self, path):
        path = pathlib.Path(path)
        path.mkdir(exist_ok=True)


        self.ori.to_csv(path / 'ori.csv', index=False)
        self.cov.to_csv(path / 'cov.csv', index=False)
        self.mco.to_csv(path / 'mco.csv', index=False)
        self.mcc.to_csv(path / 'mcc.csv', index=False)
        self.mxo.to_csv(path / 'mxo.csv', index=False)
        self.mxc.to_csv(path / 'mxc.csv', index=False)


        if self.add_probs:
            self.pori.to_csv(path / 'por.csv', index=False)
            self.pcov.to_csv(path / 'pco.csv', index=False)


        self.ori.mt.drop_duplicates().to_csv(path / 'exp.csv', index=False)


    def _try_add_probabilities(self, df, filepath):
        try:
            dff = pd.read_csv(filepath, sep=";")
            if dff.shape[1] == 1:
                dff = pd.read_csv(filepath, sep=",")
            
            df = df[(df['iteracao'] == 0) | (df['iteracao'] == 1)]

            df = pd.concat([df, dff], ignore_index=True)

            return  True, df

        except FileNotFoundError:
            return False, df
