PATH_PRJ = '/media/beldroega/DATA/SIDRAT/tardis'

PATH_CFG = '/base/configuracao.config'

PATH_CFG_TEM = '/base/configuracao_template.config'

MODULES = [ 'OTIMIZACAO'
          , 'INICIALIZACAO'
          , 'AVALIACAO'
          , 'CRITERIOPARADA'
          , 'SORTEIO'
          , 'PROBLEMA_FECHADO'
          , 'FOFE'
         ]


with open(PATH_PRJ + PATH_CFG_TEM, 'r') as fh:
    lines = []
    for line in fh:
        line = line.strip()
        if '__AVALIACAO_TYPE__' in line:
            line = line.replace('__AVALIACAO_TYPE__', 'RASTRIGIN')
            print(line)
        if '__AVALIACAO_DIRECAO_OF__' in line:
            line = line.replace('__AVALIACAO_DIRECAO_OF__', 'MAX RASTRIGIN')
            print(line)
        lines.append(line)


with open(PATH_PRJ + PATH_CFG, 'w') as fh:
    txt = '\n'.join(lines)
    fh.write(txt)


from src.carregamento.Carregamento import Carregamento
from src.inout.LogarMemoria import LiberarMemoria
from src.modulo.EnumModulo import EnumModulo
from src.contexto.EnumAtributo import EnumAtributo


class Context_Variables:
    def __init__(self):
        self.dict = {}
        self.EA = EnumAtributo

    def path_result(self, value):
        self.dict[self.EA.PATH_RESULTADO] = value

    def idlhc_number_samples_iteration(self, value):
        self.dict[self.EA.OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO] = value

    def idlhc_number_samples_pdf(self, value):
        self.dict[self.EA.OTIMIZACAO_IDLHC_AMOSTRAS_PDF] = value

    def stop_critiria(self, value):
        self.dict[self.EA.CRITERIO_PARADA] = value

    def stop_critiria_iterations(self, value):
        self.dict[self.EA.CRITERIO_PARADA_ITERACOES] = value

    def fofe(self, value):
        self.dict[self.EA.FOFE] = value

    def fofe_nnbc_num_models(self, value):
        self.dict[self.EA.NN_BINARY_CLASSIFIER_NMODELS] = value

    def fofe_nnbc_num_class1(self, value):
        self.dict[self.EA.NN_BINARY_CLASSIFIER_NCLASS1] = value

    def fofe_nnbc_threshold(self, value):
        self.dict[self.EA.NN_BINARY_CLASSIFIER_THRESHOLD] = value


def configure_context(context, context_variables):
    cv = context_variables
    csa = context.set_atributo

    for key in cv.dict:
        csa(key, cv.dict[key], True)

    return context


IDLHC_NUMBER_SAMPLES_ITERATION = [50, 100, 150]
IDLHC_NUMBER_SAMPLES_PDF = [10, 20, 30]
FOFE_NNBC_NUM_CLASS1 = [10, 20, 30]
FOFE_NNBC_NUM_THRESHOLD = [0.1, 0.2, 0.3]
TIMES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


import os
import itertools


for a, b, c, d, e in itertools.product( IDLHC_NUMBER_SAMPLES_ITERATION
                                      , IDLHC_NUMBER_SAMPLES_PDF
                                      , FOFE_NNBC_NUM_CLASS1
                                      , FOFE_NNBC_NUM_THRESHOLD
                                      , TIMES
                                      ):

    cv = Context_Variables()

    dirr = '_RES_RST/IDLHC_NSI{:03d}_NSP{:03d}_NNBC_NCT{:03d}_TCC{:03d}_{:02d}'.format(a, b, c, int(100 * d), e)

    if os.path.isdir(dirr):
        print('Experiment {} alread done'.format(dirr))

    elif os.path.isdir(dirr + '_ERROR'):
        print('Experiment {} alread done'.format(dirr + '_ERROR'))

    else:
        try:
            cv.path_result(dirr + '/it_{}')
            cv.idlhc_number_samples_iteration(a)
            cv.idlhc_number_samples_pdf(b)
            cv.stop_critiria('ITERACOES_MAX')
            cv.stop_critiria_iterations(30)
            cv.fofe('NN_BINARY_CLASSIFIER')
            cv.fofe_nnbc_num_models(10)
            cv.fofe_nnbc_num_class1(c)
            cv.fofe_nnbc_threshold(d)

            carregamento = Carregamento(PATH_PRJ, PATH_CFG, MODULES)
            context = carregamento.get_context()
            context = configure_context(context, cv)
            carregamento.set_context(context)
            carregamento.run()
            
            problema_fechado = context.get_modulo(EnumModulo.PROBLEMA_FECHADO)
            context = problema_fechado.run(context)
            
            inicializacao = context.get_modulo(EnumModulo.INICIALIZACAO)
            context = inicializacao.run(context)
            
            otimizador = context.get_modulo(EnumModulo.OTIMIZACAO)
            context = otimizador.run(context)
            
            carregamento = None
            problema_fechado = None
            inicializacao = None
            otimizador = None
            context = None
            LiberarMemoria()

        except KeyError:
            os.rename(dirr, dirr + '_ERROR')
