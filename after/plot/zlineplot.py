import pathlib
from zlineplot import lineplotoptimization
from zlineplot import lineplotoptimizationneural


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

    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V4')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')

    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V5')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT000_TCC000')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_5')

def experiment_04():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE_SBA')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE_SBA/line')

    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')

    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA016')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA032')

    lineplotoptimizationneural.run(experiments, dfRootpath, pngRootpath, prefix='e4_', suffix='_1')

    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')

    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA016')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA032')

    lineplotoptimizationneural.run(experiments, dfRootpath, pngRootpath, prefix='e4_', suffix='_2')

    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')

    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA016')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA032')

    lineplotoptimizationneural.run(experiments, dfRootpath, pngRootpath, prefix='e4_', suffix='_3')

    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')

    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA016')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA032')

    lineplotoptimizationneural.run(experiments, dfRootpath, pngRootpath, prefix='e4_', suffix='_4')


def experiment_05():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA008')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE032_SBA008/line')

    experiments = []
    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA008')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')

    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA008')

    experiments.append('NSI050_NSP010_NCT000_TCC000')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_2')


def experiment_06():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/ROSEMBROCK_NNE032_SBA008')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/ROSEMBROCK_NNE032_SBA008/line')

    experiments = []
    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA008')
    #experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA008')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA008')
    #experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA008')
    #experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')

    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA008')
    #experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA008')

    experiments.append('NSI050_NSP010_NCT000_TCC000')
    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_2')


def experiment_07():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA004')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE032_SBA004/line')

    experiments = []
    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA004')
    experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA004')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA004')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')


    experiments = []
    experiments.append('NSI100_NSP020_NCT000_TCC000')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA004')

    experiments.append('NSI050_NSP020_NCT000_TCC000')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA004')
    experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA004')

    experiments.append('NSI050_NSP010_NCT000_TCC000')

    lineplotoptimization.run(experiments, dfRootpath, pngRootpath, prefix='e7_', suffix='_2')




if __name__ == '__main__':
    #experiment_01()
    #experiment_02()
    #experiment_03()
    #experiment_04()
    experiment_05()
    #experiment_06()
    experiment_07()
