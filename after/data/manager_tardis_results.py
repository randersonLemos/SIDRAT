import re
import pathlib
import pandas as pd


class TardisFilesManager:
    def __init__(self, results_path, root_project=''):

        self.results_path = []
        if isinstance(results_path, list):
            for path in results_path:
                self.results_path.append(pathlib.Path(path))
        else:
            self.results_path.append(pathlib.Path(path))

        self.results_apath = []
        if root_project:
            self.root_project = pathlib.Path(root_project)
            for path in self.results_path:
                self.results_apath.append(self.root_project / path)
        else:
            self.results_apath = self.results_path


    def dirs(self):
        lst = []
        for Dir in self.results_apath:
            for dir in Dir.iterdir():
                lst.append(dir)

        return sorted(lst)


    def files(self, r_expression=''):
        lst = []
        for dir in self.dirs():
            for file in dir.iterdir():
                if re.search(r_expression, str(file)):
                    lst.append(file)
        return sorted(lst)


    def clean(self, r_expression):
        for file in self.files():
            if re.search(r_expression, str(file)):
                file.unlink()


class TardisDataManager:
    def __init__(self, files):
        self.files = files

        self.df = self._load()

        self.mdfa, self.mdfb = self.mean_values_expanded()


    def _load(self):
        lst = []
        for file in self.files:
            df = pd.read_csv(file, sep=";")
            df = df.iloc[1:, [0, 1, 3]]
            df['of'] = df.columns[2][7:-1]
            df['_type'] = df.columns[2][3:6]
            df = df.rename(columns={'iteracao': 'it', df.columns[2]: 'value', 'id': '_id'})
            df['id'] = df.index
            df['mt'] = file.parent.name[:-2]
            df['ru'] = file.parent.name[-1]

            df = df[['mt', 'of', 'ru', 'it', 'id', 'value', '_type', '_id']]

            lst.append(df)

        return pd.concat(lst).reset_index(drop=True)

   
    def mean_values_summary(self):
        pt = pd.pivot_table(self.df
                           , index=['mt', 'of', 'ru', 'it']
                           , values=['value']
                           , aggfunc=['count', 'max']
                           )
        pt.columns = pt.columns.droplevel(1)
        pt.columns.name = 'value'

        gba = pt.groupby(['mt', 'of', 'it']).mean().astype('int').reset_index()

        gbb = pt.groupby(['mt', 'it']).mean().astype('int').reset_index()

        gbb['of'] = ', '.join((gba['of'].unique().tolist()))

        gbb = gbb[['mt', 'of', 'it', 'count', 'max']]
    
        return gba, gbb


    def mean_values_expanded(self):
        mvsa, mvsb = self.mean_values_summary()
        mvxa = self._mean_values_expanded(mvsa)
        mvxb = self._mean_values_expanded(mvsb)

        return mvxa, mvxb


    def _mean_values_expanded(self, mvs):
        lst = []
        aux = mvs.set_index(['mt', 'of'])
        for index in aux.index.unique():
            se = aux.loc[index, 'count'].reset_index(drop=True)
            df = pd.DataFrame(index=range(se.sum()))
            df['mt'] = index[0]
            df['of'] = index[1]
            df['it'] = -1
 
            bng = 0
            end = 0
            for index_ in se.index:
                end = bng + se[index_]
                df.loc[bng: end, 'it'] = index_ + 1
                bng = end

            lst.append(df)

        df = pd.concat(lst).reset_index()

        df = df.rename(columns={'index': 'id'})
        df['id'] = df['id'] + 1
        df = df[['mt', 'of', 'it', 'id']]

        df['value'] = -1
        df = df.set_index(['mt', 'of', 'it'])

        aux = aux.reset_index().set_index(['mt', 'of', 'it'])
        for index in df.index.unique():
            #print(index)
            df.loc[index, 'value'] = aux.loc[index, 'max'].astype('int')

        return df.reset_index()


    def save(self, path):
        path = pathlib.Path(path)
        path.mkdir(exist_ok=True)

        self.df.to_csv(path / 'original.csv', index=False)

        self.mdfa.to_csv(path / 'mean_objfun.csv', index=False)

        self.mdfb.to_csv(path / 'mean_overall.csv', index=False)

        a, b = self.mean_values_summary()

        a.to_csv(path / 'mean_objfun_sum.csv', index=False)

        b.to_csv(path / 'mean_overall_sum.csv', index=False)

