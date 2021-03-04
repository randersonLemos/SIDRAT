# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:57:44 2021

@author: randerson
"""


import pandas as pd



class File_Manager:
    def __init__(self, root_path, csv_file):
        self.root_path = root_path
        self.csv_file = csv_file
        self.file_lst = []
    
        
    def load(self):
        import glob

        
        self.files = []
        for file in glob.glob(self.root_path + '\\*'):
            self.file_lst.append(file + "\\" + self.csv_file)
        self.file_lst = sorted(self.file_lst)
        return self   


class Data_Manager:
    def __init__(self, file_lst, of):
        self.file_lst = file_lst
        self.of = of        
        self.df_lst = []
             
        
        
    def load(self):
        for file in self.file_lst:
            df = pd.read_csv(file, sep=";", usecols=['iteracao', self.of])
            if  'IDLHC_ML_C10T10' in file or \
                'IDLHC_ML_C10T20' in file or \
                'IDLHC_ML_C10T30' in file or \
                'IDLHC_ML_C10T40' in file or \
                'IDLHC_ML_C10T50' in file or \
                'IDLHC_STANDARD'  in file \
                :
                    df['method'] = file.split('\\')[-2][:-2] 
                    df['experiment'] = file.split('\\')[-2][-1] 
                    df['of'] = self.of[7:-1]
                    df['value'] = df[self.of]
                    df['iteration'] = df['iteracao']
                    df = df.reset_index()
                    del df[self.of]
                    del df['iteracao']
    
                    self.df_lst.append(df)   

        self.df = pd.concat(self.df_lst).reset_index(drop=True)
        
        self.df = self.df.loc[self.df['iteration'] != 0]
        
        self.method_lst = self.df['method'].unique().tolist()
        return self


    def _agg_1(self):
        agg = pd.pivot_table(self.df
                             , values='value'
                             , index=['of', 'method', 'iteration', 'index']                        
                             , aggfunc='mean'
                            )        
        
        # IS = pd.IndexSlice
        # dummy = agg.reset_index().groupby(['of', 'method', 'iteration']).max()
        # agg['max_index'] = -1
        # agg['max_value'] = -1       


        # for of, me, it in dummy.index:
        #     agg.loc[IS[of, me, it, :], 'max_value'] = dummy.loc[(of, me, it ,), 'value']
        #     agg.loc[IS[of, me, it, :], 'max_index'] = dummy.loc[(of, me, it ,), 'index']
        
        agg = agg.reset_index()
        
        # for method in self.method_lst:
        #     agg.loc[agg['method'] == method, 'index'] = \
        #         range(len(agg.loc[agg['method'] == method, 'index']))
        
        index = agg.loc[:, ['method','index']].drop_duplicates(keep='last').index
        
        agg = agg.loc[index, :]
        
        return agg
    
    
    def _agg_2(self):
        agg = pd.pivot_table(self.df
                             , values=['index', 'value']
                             , index=['of', 'method', 'experiment', 'iteration']                        
                             , aggfunc='max'
                            )        


        agg = pd.pivot_table(agg
                             , values=['index', 'value']
                             , index=['of', 'method', 'iteration']                        
                             , aggfunc='mean'
                            )
        
        return agg
    

    def agg(self):
        if hasattr(self, '_agg'):
            return self._agg
        
        df = self._agg_1() 
        dummy = self._agg_2()
        
        df['meanmax_index'] = -1
        df['meanmax_value'] = -1   
        
        df = df.set_index(['of', 'method', 'iteration'])
        Index = dummy.index
        for index in Index:            
            df.loc[index, 'meanmax_index'] = dummy.loc[index, 'index']
            df.loc[index, 'meanmax_value'] = dummy.loc[index, 'value']        
        
        df_lst = []
        for index in Index:
            mask = df.loc[index, 'index'] <= df.loc[index, 'meanmax_index'].max()
            df_lst.append(df.loc[index, :].loc[mask].reset_index())
            
        df = pd.concat(df_lst).reset_index(drop=True)

        df['norm_index'] = (df['index'] - df['index'].min()) / (df['index'].max() - df['index'].min())
        df['norm_meanmax_value'] = (df['meanmax_value'] - df['meanmax_value'].min()) / (df['meanmax_value'].max() - df['meanmax_value'].min())

        self._agg = df
        return self._agg
    
      
OF = []
OF.append('SPHERE')
OF.append('RASTRIGIN')
OF.append('ROSENBROCK')

df_lst = []
for of in OF:   
    fm = File_Manager("U:\\SIDRAT\\tardis\\RES_"+of, "it_ultima.csv").load()
    dm = Data_Manager(fm.file_lst, of='of[MAX_'+of+']').load()
    df_lst.append(dm.agg())

df = pd.concat(df_lst).reset_index(drop=True)

grp = df.groupby(['of', 'method']).max()
grp.to_csv('final_values_of.csv')

ggrp = grp.groupby(['method']).mean()
ggrp.to_csv('final_values_of_mean.csv')

ggrp = grp.groupby(['method']).std()
ggrp.to_csv('final_values_of_std.csv')