import pathlib
from zbarplot import barplotsamplediff
from zbarplot import barplotsamplediffneural
from zbarplot import barplotstacksampleratio
from zbarplot import barplotstacksamplerationeural
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




    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V4')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')




    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_V5')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT010_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_4')

    experiments = []
    experiments.append('IDLHC_NSI100_NSP020_NNBC_NCT020_TCC010')
    barplotstacksamplecategorize.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_5')
    barplotstacksampleratio.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_5')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e3_', suffix='_5')


def experiment_04():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE_SBA')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE_SBA/bar')


    experiments = []
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA016')
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA032')
    for experiment in experiments:
        barplotstacksamplecategorize.run(experiment, dfRootpath, pngRootpath, prefix='e4_', suffix='_1')
        barplotstacksamplerationeural.run(experiment, dfRootpath, pngRootpath, prefix='e4_', suffix='_1')
        barplotsamplediffneural.run(experiment, dfRootpath, pngRootpath, prefix='e4_', suffix='_1')
    barplotsamplediffneural.run(experiments, dfRootpath, pngRootpath, prefix='e4a_', suffix='_2')


    #experiments = []
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA004')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA008')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA016')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE024_SBA032')
    #barplotsamplediffneural.run(experiments, dfRootpath, pngRootpath, prefix='e4a_', suffix='_2')


    #experiments = []
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA008')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA016')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE064_SBA032')
    #barplotsamplediffneural.run(experiments, dfRootpath, pngRootpath, prefix='e4a_', suffix='_2')


    #experiments = []
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA008')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA016')
    #experiments.append('NSI100_NSP020_NCT010_TCC010_NNE128_SBA032')
    #barplotsamplediffneural.run(experiments, dfRootpath, pngRootpath, prefix='e4a_', suffix='_2')


def experiment_05():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA008')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE032_SBA008/bar')


    experiments = []
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA008')
    #experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA008')
    for experiment in experiments:
        barplotstacksamplecategorize.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
        barplotstacksampleratio.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
        barplotsamplediff.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_2')


    experiments = []
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA008')
    #experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA008')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA008')
    for experiment in experiments:
        barplotstacksamplecategorize.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
        barplotstacksampleratio.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
        barplotsamplediff.run(experiment, dfRootpath, pngRootpath, prefix='e5_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e5_', suffix='_2')


def experiment_07():
    dfRootpath  = pathlib.Path('/media/beldroega/DATA/SHARED/csv/RASTRIGIN_NNE032_SBA004')
    pngRootpath = pathlib.Path('/media/beldroega/DATA/SHARED/png/RASTRIGIN_NNE032_SBA004/bar')


    experiments = []
    experiments.append('NSI050_NSP020_NCT010_TCC010_NNE032_SBA004')
    #experiments.append('NSI050_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI050_NSP020_NCT020_TCC010_NNE032_SBA004')
    for experiment in experiments:
        barplotstacksamplecategorize.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
        barplotstacksampleratio.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
        barplotsamplediff.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e7_', suffix='_2')


    experiments = []
    experiments.append('NSI100_NSP020_NCT010_TCC010_NNE032_SBA004')
    #experiments.append('NSI100_NSP020_NCT015_TCC010_NNE032_SBA004')
    experiments.append('NSI100_NSP020_NCT020_TCC010_NNE032_SBA004')
    for experiment in experiments:
        barplotstacksamplecategorize.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
        barplotstacksampleratio.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
        barplotsamplediff.run(experiment, dfRootpath, pngRootpath, prefix='e7_', suffix='_1')
    barplotsamplediff.run(experiments, dfRootpath, pngRootpath, prefix='e7_', suffix='_2')
 


if __name__ == '__main__':
    #experiment_02()
    #experiment_04()
    experiment_05()
    experiment_07()
