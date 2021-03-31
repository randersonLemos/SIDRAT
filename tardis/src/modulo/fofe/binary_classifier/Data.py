import copy
import pandas as pd

class Aux:
    oversampler = None
    scaler = None


class TrainData(Aux):
    def __init__(self, X, y, iteration, nlargest):
        self.X = copy.deepcopy(X); self._X = copy.deepcopy(X) # bkp
        self.y = copy.deepcopy(y); self._y = copy.deepcopy(y) # bkp

        self.nlargest = nlargest
        self.iteration = iteration

        self._processing()


    def _processing(self):

        col = self.y.columns[0]

        index = self.y.sort_values(by=col, ascending=False).index
        self.X = self.X.loc[index, :]
        self.y = self.y.loc[index, :]

        nlargest = (self.y[col]).astype('int').nlargest(self.nlargest, keep='all')

        self.y['CLASS'] = 0
        self.y.loc[nlargest.index, 'CLASS'] = 1

        self.Xo = copy.deepcopy(self.X)
        self.yo = copy.deepcopy(self.y.loc[:, 'CLASS'])
        if self.oversampler:
            self.Xo, self.yo = self.oversampler.fit_resample(self.Xo, self.yo)

        self.Xos = copy.deepcopy(self.Xo)
        if self.scaler:
            self.Xos = self.scaler.fit_transform(self.Xos)
            self.Xos = pd.DataFrame(self.Xos, index=self.Xo.index, columns=self.Xo.columns)


    def Xy(self):
        return pd.concat([self.X, self.y], axis=1)


    def save(self, path):
        pd.concat([self.X, self.y], axis=1).to_csv(path)


class TestData(Aux):
    def __init__(self, X, y, iteration):
        self.X = copy.deepcopy(X); self._X = copy.deepcopy(X) # bkp
        self.y = copy.deepcopy(y); self._y = copy.deepcopy(y) # bkp

        self.iteration = iteration

        self._processing()


    def _processing(self):
        col = self.y.columns[0]

        index = self.y.sort_values(by=col, ascending=False).index
        self.X = self.X.loc[index, :]
        self.y = self.y.loc[index, :]

        self.Xs = copy.deepcopy(self.X)
        if self.scaler:
            self.Xs = self.scaler.transform(self.Xs)
            self.Xs = pd.DataFrame(self.Xs, index=self.X.index, columns=self.X.columns)


    def Xy(self):
        return pd.concat([self.X, self.y], axis=1)


    def save(self, path):
        pd.concat([self.X, self.y], axis=1).to_csv(path)


class ClassifiedData:
    def __init__(self, TestDataObj, probabilities, threshold):
        self.tedObj = copy.deepcopy(TestDataObj)

        self.y = copy.deepcopy(self.tedObj.y)

        self.threshold = threshold

        self.y['PROBS'] = probabilities
        self.y['CLASS'] = [1 if el > threshold else 0 for el in probabilities]


