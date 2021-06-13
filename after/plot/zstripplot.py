import pathlib
from zstripplot import stripplotoptimization


def experiment_01():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')

    stripPlotDefault.run(experiments, dfRootpath, pngRootpath, suffix='_1')


def experiment_03():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')



    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V2')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')




    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V3')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    stripplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')


if __name__ == '__main__':
    #experiment_01()
    experiment_03()
