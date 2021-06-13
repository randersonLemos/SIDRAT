import pathlib
from zscatterplot import scatterPlot

dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

experiments = []
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')

scatterPlot.run(experiments, dfRootpath, pngRootpath, suffix='_1')

