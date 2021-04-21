import re
import pathlib
import numpy as np
import pandas as pd


class TardisDataManager:
    def __init__(self, files):
        self.files = files

        self.df = self.load()
        self.mco, self.Mco = self.mean_compact()

        self.mex, self.Mex = self.mean_expand()


    def load(self):
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
                                   })
            df['id'] = df.index
            df['mt'] = file.parent.name[:-2]
            df['ru'] = file.parent.name[-1]

            df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

            lst.append(df)
            
        df = pd.concat(lst).reset_index(drop=True)

        df = df.replace([np.inf, -np.inf], np.nan)

        df = df.dropna(how="any")

        return df

   
    def mean_compact(self):


        pt = pd.pivot_table(self.df
                           , index=['mt', 'of', 'ru', 'it']
                           , values=['value']
                           , aggfunc=['count', 'max']
                           )


        pt.columns = pt.columns.droplevel(1)


        pt = pt.rename(columns={'count':'n_sample', 'max':'value'})

        #pt.columns.name = 'value'
        
        gb = pt.groupby(['mt', 'of', 'it']).mean().astype('int').reset_index()


        # ### Applying convergence criterion ###
        gb = gb.set_index('mt')
        lst = []
        for idx in gb.index.unique():
            aux = gb.loc[idx]
            aux = aux.reset_index().set_index('it')
            pvl = vl = 0
            count = 0
            for jdx in aux.index.unique():
                vl = aux.loc[jdx]['value']
                if vl == pvl:
                    count += 1
                    if count == 3 - 1:
                        break
                else:
                    count = 0
                pvl = vl
            lst.append(aux.loc[:jdx].reset_index()[['mt', 'of', 'it', 'n_sample', 'value']])

        gb = pd.concat(lst).reset_index(drop=True)


        Gb = pt.groupby(['mt', 'it']).mean().astype('int').reset_index()

        Gb['of'] = ', '.join((gb['of'].unique().tolist()))

        Gb = Gb[['mt', 'of', 'it', 'n_sample', 'value']]

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

        self.mco.to_csv(path / 'mean_compact.csv', index=False)

        self.Mco.to_csv(path / 'Mean_compact.csv', index=False)

        self.mex.to_csv(path / 'mean_expand.csv', index=False)

        self.Mex.to_csv(path / 'Mean_expand.csv', index=False)
