import copy
import pickle
import pathlib
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

mpl.rcParams['axes.titlesize']  = 18.0
mpl.rcParams['axes.labelsize']  = 18.0
mpl.rcParams['xtick.labelsize'] = 17.0
mpl.rcParams['ytick.labelsize'] = 17.0
mpl.rcParams['legend.fontsize'] = 18.0
mpl.rcParams["legend.title_fontsize"] = 18.0
mpl.rcParams['lines.linewidth'] =  4.0

plt.close()

Path = pathlib.Path('./')

Pkl = {}

if not Pkl:
    for path in Path.glob('**/*.pkl'):
        with open(path, 'rb') as f:  # Python 3: open(..., 'rb')
            Pkl[path.parts[0]] = pickle.load(f)

Txt = {}

if not Txt:
    for path in Path.glob('**/*.txt'):
        with open(path, 'r') as f:  # Python 3: open(..., 'rb')
            Txt[path.parts[0]] = f.read().split('\n')


Keys = sorted(list(Pkl.keys()))

for key in Keys:
    trDs, teDs, clDs = Pkl[key]


    mult_index = pd.MultiIndex(levels=[[],[],[]],
                           codes=[[],[],[]],
                           names=['GRP', 'ITE', 'RUN']
                          )

    ys = pd.DataFrame(index = mult_index, columns=teDs[0].y.columns)

    for teD in teDs:
        ys = ys.append(teD.y)

    ys['NPV'] = (ys['NPV'] / 1000).astype('int')
    ys['NPV'] = (ys['NPV'] / 1000)

    ### NORMALIZING NPV ###
    ilevel1 = ys.index.get_level_values(1)
    group = ys.groupby('ITE')
    for i in ilevel1.unique():
        ys.loc[ilevel1 == i, 'MNPV' ] =      \
           ( ys.loc[ilevel1 == i, 'NPV' ] - group.min()['NPV'][i] )  / \
           ( group.max()['NPV'][i] - group.min()['NPV'][i] )



    fig, ax = plt.subplots(figsize=(12.5,8), tight_layout=True)
    ax = sb.stripplot(x='ITE', y='MNPV', hue='CLASS', data=ys.reset_index()
            , jitter = True
            , dodge = True
            , linewidth = 0.25
            , size=12.5
            , alpha = 0.70
            , ax=ax
            )

    ax.set_xlabel('ITERATION')
    ax.set_ylabel('NPV [MM$] (normalized per iteration)')

    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
    #ax.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%0.1f"))

    ax.set_xticks(np.linspace(0, 18 , 37), minor=True)
    ax.grid(which='minor', axis='x')

    ax.legend(loc='lower right', title='CLASS')

    title  = ''
    title += 'Samples (production strategies) classified as \"worth to be run\" (CLASS 1) and\n'
    title += '\"not worth to be run\" (CLASS 0) along optimization process with IDLHC'

    fig.suptitle(title, fontsize=20, ha='center', va='top')

    text  = ''
    text += 'SETTINGS:\n'
    text += '{} CLASS 1 samples for training (NC1T)\n'.format(key[12:14])
    text += '{}% for sample be classified as CLASS 1 (EC1T)'.format(key[-2:])
    ax.text(0, 1.15, text,
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes,
            size = 16)

    text  = ''
    text  = 'RESULTS:\n'

    bsh =  int(Txt[key][1].split(' ')[1])
    text += '{}/{} ({}%) total 20 best samples hit\n'.format(bsh, 400, int(100*bsh/400))

    runs =  2000 - int(Txt[key][0].split(' ')[1])
    text += '{}/{} ({}%) total simulation runs'.format(runs, 2000, int(100*runs/2000))
    ax.text(0.5, 1.15, text,
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes,
            size = 16)

    fig.savefig("./FIGS/NORM_{}.png".format(key))
