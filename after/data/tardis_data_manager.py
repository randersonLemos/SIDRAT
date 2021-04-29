import re
import pathlib
import numpy as np
import pandas as pd


class TardisDataManager:
    def __init__(self, files, probabilities=False, convergence=False):
        self.files = files

        self.df = self.load(convergence)

        self.mco, self.Mco = self.mean_compact()

        self.mex, self.Mex = self.mean_expand()

        if probabilities:
            self.dfp = self.loadp(convergence)

        self.df  = self.fix_shape(self.df,  self.mco)
        self.dfp = self.fix_shape(self.dfp, self.mco)


    def fix_shape(self, df, pt):
        df = df.set_index(['mt', 'of'])
        pt = pt.set_index(['mt', 'of'])
        lst = []
        for idx in df.index.unique():
            aux = df.loc[idx]
            auz = pt.loc[idx]
            mit = auz['it'].max()
            msk = aux['it'] <= mit
            lst.append(aux[msk].reset_index())

        df = pd.concat(lst)

        return df


    def load(self, convergence):
        lst = []
        for file in self.files:

            print('Loading: {}'.format(file))

            df = pd.read_csv(file, sep=";")
            if df.shape[1] == 1:
                df = pd.read_csv(file, sep=",")

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

        if convergence:
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

        df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

        return df


    def loadp(self, convergence):
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

        if convergence:
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

   
    def mean_compact(self):
        pt = pd.pivot_table(self.df
                           , index=['mt', 'of', 'ru', 'it']
                           , values=['value']
                           , aggfunc=['count', 'max']
                           )


        pt.columns = pt.columns.droplevel(1)


        pt = pt.rename(columns={'count':'n_sample', 'max':'value'})

        pt = pt.reset_index()
        
        #pt.columns.name = 'value'

        # ### Teste
        pt = pt.set_index(['mt', 'of'])
        lst = []
        for idx in pt.index.unique():
            aux = pt.loc[idx].reset_index()
            #ptt = aux.pivot(index=['mt', 'of', 'ru'], columns=['it'], values=['n_sample', 'value']).T.fillna(method='ffill').T
            ptt = aux.pivot(index=['mt', 'of', 'ru'], columns=['it'], values=['n_sample', 'value']).T.dropna().T
            lst.append(ptt.stack().reset_index())
        
        pt = pd.concat(lst)
        ###
        
        gb = pt.groupby(['mt', 'of', 'it']).mean().astype('int').reset_index()
        gb = gb.reset_index()

        #yb = pt.groupby(['mt', 'of', 'it']).sum() / pt['ru'].astype('int').max()
        #yb = yb.astype('int')
        #yb = yb.reset_index()
        #gb['n_sample'] = yb['n_sample']

        # ### Applying convergence criterion ###
        #gb = gb.set_index(['mt', 'of'])
        #lst = []
        #for idx in gb.index.unique():
        #    aux = gb.loc[idx]
        #    aux = aux.reset_index().set_index('it')
        #    pvl = vl = 0
        #    count = 0
        #    for jdx in aux.index.unique():
        #        vl = aux.loc[jdx]['value']
        #        if vl == pvl:
        #            count += 1
        #            if count == 3 - 1:
        #                break
        #        else:
        #            count = 0
        #        pvl = vl
        #    lst.append(aux.loc[:jdx].reset_index()[['mt', 'of', 'it', 'n_sample', 'value']])
        #
        #gb = pd.concat(lst).reset_index(drop=True)
        ###

        Gb = pt.groupby(['mt', 'it']).mean().astype('int').reset_index()

        Gb['of'] = ', '.join((gb['of'].unique().tolist()))

        Gb = Gb[['mt', 'of', 'it', 'n_sample', 'value']]

        # ### Applying convergence criterion ###
        #Gb = Gb.set_index(['mt', 'of'])
        #lst = []
        #for idx in Gb.index.unique():
        #    aux = Gb.loc[idx]
        #    aux = aux.reset_index().set_index('it')
        #    pvl = vl = 0
        #    count = 0
        #    for jdx in aux.index.unique():
        #        vl = aux.loc[jdx]['value']
        #        if vl == pvl:
        #            count += 1
        #            if count == 3 - 1:
        #                break
        #        else:
        #            count = 0
        #        pvl = vl
        #    lst.append(aux.loc[:jdx].reset_index()[['mt', 'of', 'it', 'n_sample', 'value']])
        #Gb = pd.concat(lst).reset_index(drop=True)
        ###


        return gb, Gb


    def mean_expand(self):
        mean, Mean = self.mean_compact()
        mean = self._mean_expand(mean)
        Mean = self._mean_expand(Mean)

        return mean, Mean


    def _mean_expand(self, mc):
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
