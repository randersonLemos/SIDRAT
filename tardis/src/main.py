import sys

from src.carregamento.Carregamento import Carregamento
from src.inout.LogarMemoria import LiberarMemoria
from src.modulo.EnumModulo import EnumModulo

# sys.path.insert(0, ".")
# sys.path.insert(0, "..")

path_relativo_config = ""
modules = ['OTIMIZACAO', 'INICIALIZACAO', 'REDUCAO', 'AVALIACAO', 'CRITERIOPARADA', 'SORTEIO', 'PROBLEMA_FECHADO']

###TODO  escrever o caminho do projeto
path_projeto = r'C:\Users\rafael\Desktop\randerson\tardis\idlhc'

paths = []
###TODO escrever caminho do .config
paths.append(r'..\base\configuracao.config')

if sys.stdin.isatty():
    lista_argumentos = list(sys.argv)
    if len(lista_argumentos) >= 2:
        path_projeto = lista_argumentos[1]
        if len(lista_argumentos) >= 3:
            paths = []
            for ii in range(2, len(lista_argumentos)):
                paths.append(lista_argumentos[ii])


    print(f'lista {lista_argumentos}')
print(f'projeto {path_projeto}')
print(f'paths {paths}')

ii = 0
while ii < len(paths):
    try:
        path_relativo_config = paths[ii]
        print('******************************************************')
        print('******************************************************')
        print(f'** EXECUTANDO {path_relativo_config}')
        print('******************************************************')
        print('******************************************************')

        carregamento = Carregamento(path_projeto, path_relativo_config, modules)
        contexto = carregamento.run()

        problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
        contexto = problema_fechado.run(contexto)

        inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
        contexto = inicializacao.run(contexto)

        otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
        contexto = otimizador.run(contexto)

        print('******************************************************')
        print('******************************************************')
        print('************** PROGRAMA FINALIZADO *******************')
        print('******************************************************')
        print('******************************************************')
        ii = ii + 1
    except Exception as ex:
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print(str(ex))
        print('************** PROGRAMA FINALIZADO *******************')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        exit(-1)
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
