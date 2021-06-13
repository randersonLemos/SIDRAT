import re
import pathlib
import numpy as np
import pandas as pd


class NnbcDataManager:
    def __init__(self, filepath):
        self.df = self._read_csv(filepath)


    def _read_csv(self, filepath):
        df = pd.read_csv(filepath, sep=';')
        if df.shape[1] == 1:
            df = pd.read_csv(filepath, sep=',')

        return df


 
