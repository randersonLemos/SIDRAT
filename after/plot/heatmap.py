import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap

plt.close()


df = pd.read_csv('/media/beldroega/DATA/SHARED/SIDRAT/DATA/mean_compact.csv')

df['mt_'] = '('
for col in ['nsi', 'nsp', 'nct', 'tcc']:
    df['mt_'] += df[col].apply(lambda x: '{:03d}'.format(x))
    if col != 'tcc':
        df['mt_'] += ', '
df['mt_'] += ')'

df['n_sample_'] = -1
df = df.set_index('mt')
for index in df.index:
    df.loc[index, 'n_sample_'] = sum(df.loc[index, 'n_sample'])
df = df.reset_index()


aux = df.copy()
aux = aux[aux['nsi'] == 50]
aux = aux[(aux['nct'] == 10) | (aux['nct'] == 0)]
#aux = aux[aux['nct'] == 0]

fig, ax = plt.subplots(figsize=(10, 8))

sb.heatmap(  aux.pivot(index='mt_', columns='it', values='n_sample').T
           , annot=True
           , fmt="d"
           , annot_kws={'fontsize':8, 'color' : 'white'}
           , cmap=ListedColormap(['white'])
           , cbar=False
           #, square=True
           , ax=ax
          )

sb.heatmap(  aux.pivot(index='mt_', columns='it', values='n_sample_').T
           , linewidth=0.0
           , cmap=sb.color_palette("viridis", n_colors=15)
           #, cmap=sb.color_palette("viridis", as_cmap=True)
           #, vmin='-100'
           , ax=ax
          )

# Get the colorbar object from the Seaborn heatmap
colorbar = ax.collections[1].colorbar
n=10
# The list comprehension calculates the positions to place the labels to be evenly distributed across the colorbar
r = colorbar.vmax - colorbar.vmin
colorbar.set_ticks([colorbar.vmin + 0.5 * r / (n) + r * i / (n) for i in range(n)])
#colorbar.set_ticklabels(list(vmap.values()))
plt.tight_layout()

plt.show()
