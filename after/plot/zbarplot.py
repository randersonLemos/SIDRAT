import pathlib
from zbarplot import barplotsamplediff
from zbarplot import barplotstacksampleratio
from zbarplot import barplotstacksamplecategorize


def experiment_01():
    ###
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V2')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_V2')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')

    barPlotStackSampleCategorize.run(experiments, dfRootpath, pngRootpath, suffix='_1')
    barPlotStackSampleRatio.run(experiments, dfRootpath, pngRootpath, suffix='_1')
    barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)


    ####
    #dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/ROSENBROCK')
    #pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/ROSENBROCK')
    #
    #experiments = []
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')
    #
    ##barPlotStackSampleCategorize.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
    ##barPlotStackSampleRatio.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
    #barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)
    #
    #
    ####
    #dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/SPHERE')
    #pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/SPHERE')
    #
    #experiments = []
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC020')
    #experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC030')
    #
    ##barPlotStackSampleCategorize.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
    ##barPlotStackSampleRatio.run(experiments[0], dfRootpath, pngRootpath, suffix='_1')
    #barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath)

def experiment_02():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')

    #barPlotStackSampleCategorize.run(experiments, dfRootpath, pngRootpath, suffix='_1')
    #barPlotStackSampleRatio.run(experiments, dfRootpath, pngRootpath, suffix='_1')
    barPlotSampleDiff.run(experiments, dfRootpath, pngRootpath, suffix='_1')


def experiment_03():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_1')




    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V2')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_2')




    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V3')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_3')


if __name__ == '__main__':
    #experiment_02()
    experiment_03()
