import pandas as pd

path = '/media/beldroega/DATA/SHARED/csv/'

mean_compact = pd.read_csv(path + 'mean_compact.csv')
Mean_compact = pd.read_csv(path + 'Mean_compact.csv')
mean_expand  = pd.read_csv(path + 'mean_expand.csv')
Mean_expand  = pd.read_csv(path + 'Mean_expand.csv')
all_data  = pd.read_csv(path + 'all_data.csv')

dic = {}
dic['mt'] = 'mt'
dic['of'] = 'of'
dic['id'] = 'id'
dic['it'] = 'it'
dic['value'] = 'vl'
dic['n_sample'] = 'n_sample'
dic['nsi'] = 'NSI'
dic['nsp'] = 'NSP'
dic['nct'] = 'NCT'
dic['tcc'] = 'TCC'
dic['nsi_nsp'] = 'NSI, NSP'
dic['nct_tcc'] = 'NCT, TCC'
dic['nnnt'] = 'nnnt'
dic['nnbc'] = 'nnbc'


class Columns:
    def __init__(self, dic):
        self.dic = dic
        self._update_vars()

    def _update_vars(self):
        for var in dic:
            exec("self.{} = '{}'".format(var, dic[var]))

    def update_name(self, key, name):
        if key in self.dic:
            self.dic[key] = [self.dic[key], name]
        else:
            raise KeyError(key)

    def apply_rename(self, data):
        for key, item in self.dic.items():
            if isinstance(item, list):
                data = data.rename(columns={item[0]: item[1]})
                self.dic[key] = item[1]
            else:
                data = data.rename(columns={key: item})
                self.dic[key] = item

        self._update_vars()

        return data
 
    def __call__(self):
        return self.dic


    def __repr__(self):
        stg = self.dic.__repr__()
        stg = stg.replace(',', '\n')
        return stg


colsObj = Columns(dic)

all_data     = colsObj.apply_rename(all_data)

mean_compact = colsObj.apply_rename(mean_compact)
Mean_compact = colsObj.apply_rename(Mean_compact)

mean_expand = colsObj.apply_rename(mean_expand)
Mean_expand = colsObj.apply_rename(Mean_expand)


for var in ['nsi', 'nsp', 'nct', 'tcc']:

    all_data[dic[var]] = all_data[dic[var]].astype('str')

    mean_compact[dic[var]] = mean_compact[dic[var]].astype('str')
    Mean_compact[dic[var]] = Mean_compact[dic[var]].astype('str')

    mean_expand[dic[var]] = mean_expand[dic[var]].astype('str')
    Mean_expand[dic[var]] = Mean_expand[dic[var]].astype('str')


all_data = all_data[all_data[colsObj.tcc] != '70']

mean_compact = mean_compact[mean_compact[colsObj.tcc] != '70']
Mean_compact = Mean_compact[Mean_compact[colsObj.tcc] != '70']

mean_expand = mean_expand[mean_expand[colsObj.tcc] != '70']
Mean_expand = Mean_expand[Mean_expand[colsObj.tcc] != '70']


if __name__ == '__main__':
    mean_compact = mean_compact.set_index('mt')
    mean_expand =  mean_expand.set_index('mt')

    index = mean_compact.index.unique()

    for idx in index:
        print(idx)
        print(mean_expand.loc[idx, colsObj.id].max())
        print(mean_compact.loc[idx, colsObj.n_sample].sum())
