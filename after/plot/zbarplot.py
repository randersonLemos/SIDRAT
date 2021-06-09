import pathlib
from zbarplot import barPlotSampleDiff
from zbarplot import barPlotSampleRatio
from zbarplot import barPlotStackSampleRatio
from zbarplot import barPlotStackSampleCategorize


###
dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

experiments = []
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')

barPlotStackSampleCategorize.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
barPlotStackSampleRatio.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)


###
dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/ROSENBROCK')
pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/ROSENBROCK')

experiments = []
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')

#barPlotStackSampleCategorize.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
#barPlotStackSampleRatio.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)


###
dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/SPHERE')
pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/SPHERE')

experiments = []
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')

#barPlotStackSampleCategorize.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
#barPlotStackSampleRatio.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)
