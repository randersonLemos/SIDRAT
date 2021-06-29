import pathlib
import pandas as pd


class Columns:
    def __init__(self):
        self.mt = 'mt'
        self.of = 'of'
        self.id = 'id'
        self.it = 'it'
        self.ru = 'ru'
        self.value = 'value'
        self.n_sample = 'n_sample'
        self.nsi = 'nsi'
        self.nsp = 'nsp'
        self.nct = 'nct'
        self.tcc = 'tcc'
        self.nne = 'nne'
        self.sba = 'sba'
        self.cls = 'class'

        self.nsi_nsp = 'nsi_nsp'
        self.nct_tcc = 'nct_tcc'
        self.nne_sba = 'nne_sba'



    def rename(self, df, att, name):
        dic = {self.__dict__[att] : name}
        self.__dict__[att] = name
        df = df.rename(columns=dic)
        return df


class DataFramesHolder:
    def __init__(self, path):
        path = pathlib.Path(path)
        self.ori = pd.read_csv(path / 'ori.csv')
        self.mco = pd.read_csv(path / 'mco.csv')
        self.mxo = pd.read_csv(path / 'mxo.csv')
        self.por = pd.read_csv(path / 'por.csv')

        self.cov = pd.read_csv(path / 'cov.csv')
        self.mcc = pd.read_csv(path / 'mcc.csv')
        self.mxc = pd.read_csv(path / 'mxc.csv')
        self.pco = pd.read_csv(path / 'pco.csv')


    def getDataFrameDic(self):
        return self.__dict__


    def updateDataFrame(self, key, df):
        self.__dict__[key] = df


def load(dfRootpath):
    path = dfRootpath
    dfH = DataFramesHolder(path)
    cOb = Columns()

    dic = dfH.getDataFrameDic()
    for key, df in dic.items():
        df[cOb.nsi_nsp] = ''
        df[cOb.nct_tcc] = ''
        df[cOb.nne_sba] = ''

        for col in [cOb.nsi, cOb.nsp, cOb.nct, cOb.tcc, cOb.nne, cOb.sba]:
            df[col] = df[col].apply(lambda x: '{:02d}'.format(x)).astype('str')

        df[cOb.nsi_nsp] = df[cOb.nsi] + ', ' + df[cOb.nsp]
        df[cOb.nct_tcc] = df[cOb.nct] + ', ' + df[cOb.tcc]
        df[cOb.nne_sba] = df[cOb.nne] + ', ' + df[cOb.sba]

        dfH.updateDataFrame(key, df)
    return cOb, dfH
