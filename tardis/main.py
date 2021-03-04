from src.carregamento.Carregamento import Carregamento
from src.inout.LogarMemoria import LiberarMemoria
from src.modulo.EnumModulo import EnumModulo
from src.contexto.EnumAtributo import EnumAtributo


def run_idlhc_standard(time):
    path_project = 'U:/SIDRAT/tardis'

    path_config  = '/base/configuracao.config'

    modules      = [  'OTIMIZACAO'
                    , 'INICIALIZACAO'
                    , 'AVALIACAO'
                    , 'CRITERIOPARADA'
                    , 'SORTEIO'
                    , 'PROBLEMA_FECHADO'
                   ]        
    
    carregamento = Carregamento(path_project, path_config, modules)
    contexto = carregamento.run()    
   
    problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
    
    contexto = problema_fechado.run(contexto)
    
    EA = EnumAtributo
    csa = contexto.set_atributo
    csa(EA.PATH_RESULTADO, "RES/IDLHC_STANDARD_{}/it_{{}}".format(time), True)
    
    inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
    
    contexto = inicializacao.run(contexto)
    
    otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
    contexto = otimizador.run(contexto)
    
    carregamento = None
    problema_fechado = None
    inicializacao = None
    otimizador = None
    contexto = None
    LiberarMemoria()


def run_idlhc_ml(time):    
    path_project = 'U:/SIDRAT/tardis'

    path_config  = '/base/configuracao_fofe.config'

    modules      = [  'OTIMIZACAO'
                    , 'INICIALIZACAO'
                    , 'AVALIACAO'
                    , 'CRITERIOPARADA'
                    , 'SORTEIO'
                    , 'PROBLEMA_FECHADO'
                    , 'FOFE'
                   ]
    
    NCLASS1 = [10, 15, 20]
    THRESHOLD = [10, 20, 30, 40, 50]
    
    
    import itertools
    for nclass1, threshold in itertools.product(NCLASS1, THRESHOLD):
        carregamento = Carregamento(path_project, path_config, modules)
        contexto = carregamento.run()
    
        EA = EnumAtributo
        csa = contexto.set_atributo
        csa(EA.NN_BINARY_CLASSIFIER_NCLASS1, nclass1, True)
        csa(EA.NN_BINARY_CLASSIFIER_THRESHOLD, threshold/100, True)
        csa(EA.PATH_RESULTADO, "RES/IDLHC_ML_C{}T{}_{}/it_{{}}".format(nclass1, threshold, time), True)
    
        problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
        contexto = problema_fechado.run(contexto)
    
        inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
        contexto = inicializacao.run(contexto)
    
        otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
        contexto = otimizador.run(contexto)
    
        carregamento = None
        problema_fechado = None
        inicializacao = None
        otimizador = None
        contexto = None
        LiberarMemoria()
  
times = [1, 2, 3, 4, 5]   
  
for time in times:        
    run_idlhc_standard(time)
    
for time in times:
    run_idlhc_ml(time)  