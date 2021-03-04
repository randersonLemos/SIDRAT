# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:43:06 2021

@author: randerson
"""

import matplotlib.pyplot as plt
plt.style.use('seaborn-talk')


import matplotlib as mpl
mpl.rcParams['figure.titlesize']  = 22.0
mpl.rcParams['axes.titlesize']  = 18.0
mpl.rcParams['axes.labelsize']  = 18.0
mpl.rcParams['xtick.labelsize'] = 17.0
mpl.rcParams['ytick.labelsize'] = 17.0
mpl.rcParams['legend.fontsize'] = 18.0
mpl.rcParams['legend.title_fontsize'] = 18.0
mpl.rcParams['lines.linewidth'] =  5

from matplotlib.ticker import FuncFormatter


def Graphing(of):
    
    import pos_processing as pp

    fm = pp.File_Manager("U:\\SIDRAT\\tardis\\RES_"+of, "it_ultima.csv").load()
    dm = pp.Data_Manager(fm.file_lst, of='of[MAX_'+of+']').load()

    
    
    lst = []
    lst.append({'method':'IDLHC_STANDARD',  'color':'k'})
    lst.append({'method':'IDLHC_ML_C10T10', 'color':'b'})
    lst.append({'method':'IDLHC_ML_C10T20', 'color':'c'})
    lst.append({'method':'IDLHC_ML_C10T30', 'color':'r'})
    lst.append({'method':'IDLHC_ML_C10T40', 'color':'y'})
    lst.append({'method':'IDLHC_ML_C10T50', 'color':'g'})
    
    
    fig, ax = plt.subplots(figsize=(10,8))
    for dic in lst:
        ax.plot('norm_index', 'norm_meanmax_value', data=dm.agg().loc[dm.agg()['method'] == dic['method'], :]
        , c=dic['color']
        , alpha=1.0,
        )
    
    
    ax.set_xlabel('Runs (normalized)')
    ax.set_ylabel('Values (normalized)')
    
    labels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ax.set_yticks(labels)
    ax.set_xticks(labels)
    
    ax.legend([dic['method'] for dic in lst]
             )    
       
    text  = ''
    text += of+' FUNCTION OPTIMIZATION\n' 
    plt.text(  x=0.0, y=1.03, s=text
             , fontsize=24
             , ha='left'
             , transform=plt.gca().transAxes
            )
    
    text  = ''
    #text += '20 iterations stop criterio\n'
    text += '5 trials mean performance\n'
    text += 'Maximum value per iteration'
    
    plt.text(  x=0.0, y=1.02, s=text
             , fontsize=14
             , ha='left'
             , transform=plt.gca().transAxes
            )
    
    ax.grid()
    fig.tight_layout()
    plt.margins(x=0.01, y=0.01)
    plt.subplots_adjust(top=0.875)
    
    plt.savefig(of+'_max_mean_values.png',  pad_inches=0.0)
    plt.ioff()    

OF = []
OF.append('SPHERE')
OF.append('RASTRIGIN')
OF.append('ROSENBROCK')

for of in OF:
    Graphing(of)

#Graphing('SPHERE')