import re
import pathlib
import numpy as np
import pandas as pd


class TardisDataManager:
    def __init__(self, files, add_probs=False, n_iter_convergence_criterio=0, fix_shape=True):
        self.files = files


        self.ori = self.load()
        if add_probs:
            self.pori = self.pload()


        if n_iter_convergence_criterio:
            self.cov = self.apply_n_iter_convergence_criterio(self.ori, n_iter_convergence_criterio)
            if add_probs:
                self.pcov = self.apply_n_iter_convergence_criterio(self.pori, n_iter_convergence_criterio)
        else:
            self.cov = self.ori
            if add_probs:
                self.pcov = self.cov


        if fix_shape:
            if add_probs:
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


        self.ori.to_csv('/media/beldroega/DATA/SHARED/ori.csv')
        self.cov.to_csv('/media/beldroega/DATA/SHARED/cov.csv')
        self.mco.to_csv('/media/beldroega/DATA/SHARED/mco.csv')
        self.mcc.to_csv('/media/beldroega/DATA/SHARED/mcc.csv')
        self.mxo.to_csv('/media/beldroega/DATA/SHARED/mxo.csv')
        self.mxc.to_csv('/media/beldroega/DATA/SHARED/mxc.csv')


        if add_probs:
            self.pori.to_csv('/media/beldroega/DATA/SHARED/pori.csv')
            self.pcov.to_csv('/media/beldroega/DATA/SHARED/pcov.csv')


    def load(self):
        lst = []
        for file in self.files:

            print('Loading: {}'.format(file))

            df = pd.read_csv(file, sep=';')
            if df.shape[1] == 1:
                df = pd.read_csv(file, sep=',')

            df = df.iloc[1:, [0, 1, 3]]

            df['of'] = df.columns[2][7:-1]
            df['_type'] = df.columns[2][3:6]
            df = df.rename(columns={  'iteracao': 'it'
                                    , df.columns[2]: 'value'
                                    , 'id': '_id'
                                    , 'probs': 'prob'
                                   })
            df['id'] = df.index
            df['mt'] = file.parent.name[:-2]
            df['ru'] = file.parent.name[-1]

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


    def save(self, path):
        path = pathlib.Path(path)
        path.mkdir(exist_ok=True)

        self.df.to_csv(path / 'all_data.csv', index=False)

        self.dfp.to_csv(path / 'zall_data.csv', index=False)

        self.mco.to_csv(path / 'mean_compact.csv', index=False)

        self.Mco.to_csv(path / 'Mean_compact.csv', index=False)

        self.mex.to_csv(path / 'mean_expand.csv', index=False)

        self.Mex.to_csv(path / 'Mean_expand.csv', index=False)


    def pload(self):
        lst = []
        for file in self.files:

            print('Loading: {}'.format(file))

            df = pd.read_csv(file, sep=";")
            if df.shape[1] == 1:
                df = pd.read_csv(file, sep=",")

            sucess, df = self._try_add_probabilities(df, file.parent / 'zall_samples.csv')

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
            df['mt'] = file.parent.name[:-2]
            df['ru'] = file.parent.name[-1]

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


    def _try_add_probabilities(self, df, file):
        try:
            dff = pd.read_csv(file, sep=";")
            if dff.shape[1] == 1:
                dff = pd.read_csv(file, sep=",")
            
            df = df[(df['iteracao'] == 0) | (df['iteracao'] == 1)]

            df = pd.concat([df, dff], ignore_index=True)

            return  True, df

        except FileNotFoundError:
            return False, df


