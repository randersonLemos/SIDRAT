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

Txt = {}

if not Txt:
    for path in Path.glob('**/*.txt'):
        with open(path, 'r') as f:  # Python 3: open(..., 'rb')
            Txt[path.parts[0]] = f.read().split('\n')

if 'BKP' in Txt:
    del Txt['BKP']

Keys = sorted(list(Txt.keys()))

Num_class_1 = []
Threshold = []
for key in Keys:
    Num_class_1.append(key[12:14])
    Threshold.append(key[-2:])

Num_class_0 = []
Num_b20samples = []
for key in Keys:
    Num_class_0.append(int(Txt[key][0].split(' ')[1]))
    Num_b20samples.append(int(Txt[key][1].split(' ')[1]))

MId = pd.MultiIndex.from_arrays([Num_class_1, Threshold], names=['NC1T', 'EC1C'])

Df = pd.DataFrame(index=Keys, columns=['CLASS0', 'B20SAMPLES'])
Df.index = MId

Df['CLASS0'] = Num_class_0
Df['CLASS1'] = 2000 - Df['CLASS0']
Df['B20SAMPLES'] = Num_b20samples

filter1 = list(range(0,9,2))
filter2 = list(range(9,18,2))
filter3 = list(range(18,27,2))

filterr = filter1 + filter2 + filter3

#Df = Df.iloc[filterr, :]

I = pd.IndexSlice
fig, ax = plt.subplots(figsize=(12.5,8), tight_layout=True)

sb.scatterplot(x='CLASS1', y='B20SAMPLES', hue='NC1T', style='EC1C', s=400, data=Df.reset_index())

ax.set_xlabel('Total samples classified as \"worth to run\" (CLASS 1)')
ax.set_ylabel('Total 20 best samples classified correctly')

# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def major_formatter(x, pos):
    return "{:.0f}".format(x)

ax.xaxis.set_major_locator(ticker.LinearLocator(8))
ax.yaxis.set_major_locator(ticker.LinearLocator(8))
ax.xaxis.set_major_formatter(major_formatter)
ax.yaxis.set_major_formatter(major_formatter)

title  = ''
title += 'Tradeoff between simulations runs (x-axis) and classifier accuracy (y-axis) according\n'
title += 'the $\it{Number\ of\ CLASS\ 1\ in\ training\ (NC1T)}$\n'
title += 'and the $\it{Enough\ probability\ to\ a\ sample\ be\ of\ CLASS\ 1\ in\ the\ classification\ (EC1C)}$'

fig.suptitle(title, fontsize=20, ha='center', va='top')

text  = ''
text += 'OPTIMIZATION WITH IDLHC (REFERENCE):\n'
text += '100 samples per iteration and 20 best samples for pdf updating\n'.format(key[12:14])
text += 'Total of 2000 simulations run and 400 total 20 best samples'.format(key[-2:])
ax.text(0, 1.15, text,
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes,
        size = 16)

ax.grid()

plt.legend(bbox_to_anchor=(1.02, 1.02), loc=2, borderaxespad=0.)

fig.savefig("./FIGS/SUMMARY.png".format(key))




Df['CLASS1PER'] = ( 100 * (Df['CLASS1'] / 2000 ))
Df['B20SAMPLESPER'] = (100 * (Df['B20SAMPLES'] / 400 ))

I = pd.IndexSlice
fig, ax = plt.subplots(figsize=(12.5,8), tight_layout=True)

sb.scatterplot(x='CLASS1PER', y='B20SAMPLESPER', hue='NC1T', style='EC1C', s=400, data=Df.reset_index())

ax.set_xlabel('Total samples classified as \"worth to run\" (CLASS 1)')
ax.set_ylabel('Total 20 best samples classified correctly')

# FuncFormatter can be used as a decorator
@ticker.FuncFormatter
def major_formatter(x, pos):
    return "{:.0f}%".format(x)

ax.xaxis.set_major_locator(ticker.LinearLocator(8))
ax.yaxis.set_major_locator(ticker.LinearLocator(8))
ax.xaxis.set_major_formatter(major_formatter)
ax.yaxis.set_major_formatter(major_formatter)

title  = ''
title += 'Tradeoff between simulations runs (x-axis) and classifier accuracy (y-axis) according\n'
title += 'the $\it{Number\ of\ CLASS\ 1\ in\ training\ (NC1T)}$\n'
title += 'and the $\it{Enough\ probability\ to\ a\ sample\ be\ of\ CLASS\ 1\ in\ the\ classification\ (EC1C)}$'

fig.suptitle(title, fontsize=20, ha='center', va='top')

text  = ''
text += 'OPTIMIZATION WITH IDLHC (REFERENCE):\n'
text += '100 samples per iteration and 20 best samples for pdf updating\n'.format(key[12:14])
text += 'Total of 2000 simulations run and 400 total 20 best samples'.format(key[-2:])
ax.text(0, 1.15, text,
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes,
        size = 16)

ax.grid()

plt.legend(bbox_to_anchor=(1.02, 1.02), loc=2, borderaxespad=0.)

fig.savefig("./FIGS/SUMMARY_PER.png".format(key))

#ax.plot('CLASS0', 'B20SAMPLES', data=Df.loc[I['10', :] , :])
#ax.plot('CLASS0', 'B20SAMPLES', data=Df.loc[I['15', :] , :])
#ax.plot('CLASS0', 'B20SAMPLES', data=Df.loc[I['20', :] , :])
