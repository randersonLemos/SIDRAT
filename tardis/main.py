import sys

from src.carregamento.Carregamento import Carregamento
from src.inout.LogarMemoria import LiberarMemoria
#from src.modulo.EnumModulo import EnumModulo

modules = [  'OTIMIZACAO'
           , 'INICIALIZACAO'
           , 'REDUCAO'
           , 'AVALIACAO'
           , 'CRITERIOPARADA'
           , 'SORTEIO'
           , 'PROBLEMA_FECHADO'
          ]

path_projeto = ''
Path_config = []

if sys.stdin.isatty():
    for idx, argumento in enumerate(sys.argv):
        if idx == 1:
            path_projeto = argumento
        if idx >= 2:
            Path_config.append(argumento)

# Caminho para a raiz do projeto (DEFAULT)
if not path_projeto:
    path_projeto = '/media/beldroega/DATA/SIDRAT/TARDIS'

# Caminho relativo para o arquivo *.config (DEFAULT)
if not Path_config:
    Path_config.append('base/configuracao.config')


print(f'projeto {path_projeto}')
print(f'paths   {Path_config}')


for path_config in Path_config:
    try:
        print('******************************************************')
        print('******************************************************')
        print(f'** EXECUTANDO {path_config}')
        print('******************************************************')
        print('******************************************************')

        carregamento = Carregamento(path_projeto, path_config, modules)
        contexto = carregamento.run()

        #problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
        #contexto = problema_fechado.run(contexto)

        #inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
        #contexto = inicializacao.run(contexto)

        #otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
        #contexto = otimizador.run(contexto)

        print('******************************************************')
        print('******************************************************')
        print('************** PROGRAMA FINALIZADO *******************')
        print('******************************************************')
        print('******************************************************')

    except Exception as ex:
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print(str(ex))
        print('************** PROGRAMA FINALIZADO *******************')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        sys.exit(-1)

    finally:
        carregamento = None
        problema_fechado = None
        inicializacao = None
        otimizador = None
        contexto = None
        LiberarMemoria()

print('******************************************************')
print('******************************************************')
print('************** TUDO CHEGOU AO FIM ********************')
print('******************************************************')
print('******************************************************')
