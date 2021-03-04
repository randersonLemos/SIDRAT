PATH_PRJ = '/tmp/SIDRAT/tardis'

PATH_CFG = '/base/configuracao.config'

MODULES = [ 'OTIMIZACAO'
          , 'INICIALIZACAO'
          , 'AVALIACAO'
          , 'CRITERIOPARADA'
          , 'SORTEIO'
          , 'PROBLEMA_FECHADO'
          , 'FOFE'
         ]


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


cv = Context_Variables()
cv.path_result('RES/it_{}')
cv.idlhc_number_samples_pdf(20)
cv.idlhc_number_samples_iteration(100)
cv.stop_critiria('ITERACOES_MAX')
cv.stop_critiria_iterations(20)
cv.fofe('NN_BINARY_CLASSIFIER')
cv.fofe_nnbc_num_models(10)
cv.fofe_nnbc_num_class1(10)
cv.fofe_nnbc_threshold(0.1)


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
