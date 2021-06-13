import pathlib
from zlineplot import lineplotoptimization


def experiment_01():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')

    linePlotOptimizationEvolution.run(experiments, dfRootpath, pngRootpath, suffix='_1')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC020')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC030')

    linePlotOptimizationEvolution.run(experiments, dfRootpath, pngRootpath, suffix='_2')


def experiment_02():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')
    linePlotOptimizationEvolution.run(experiments, dfRootpath, pngRootpath, suffix='_1')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC020')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC030')
    linePlotOptimizationEvolution.run(experiments, dfRootpath, pngRootpath, suffix='_2')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    linePlotOptimizationEvolution.run(experiments, dfRootpath, pngRootpath, suffix='_3')


def experiment_03():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')


    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V2')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')

    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V3')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')





if __name__ == '__main__':
    #experiment_01()
    #experiment_02()
    experiment_03()
