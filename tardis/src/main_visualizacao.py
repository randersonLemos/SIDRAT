import sys

from src.carregamento.Carregamento import Carregamento
from src.modulo.EnumModulo import EnumModulo

# sys.path.insert(0, ".")
# sys.path.insert(0, "..")

path_relativo_config = ""
modules = ['VISUALIZACAO']

###TODO  escrever o caminho do projeto
path_projeto = r'D:\\Users\\rafae\\CEPETRO\\Tardis\\execucao\\caixa_preta\\SPHERE_2\\'

paths = []
###TODO escrever caminho do .config
paths.append(r'base\configuracao_visualizacao.config')

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

tamanho_maximo = len(paths)
erros = 0
erros_maximo = 1
ii = 0
while ii < tamanho_maximo:

    try:
        path_relativo_config = paths[ii]

        print('******************************************************')
        print('******************************************************')
        print(f'** EXECUTANDO {path_relativo_config}')
        print('******************************************************')
        print('******************************************************')

        carregamento = Carregamento(path_projeto, path_relativo_config, modules)
        contexto = carregamento.run()

        visualizacao = contexto.get_modulo(EnumModulo.VISUALIZACAO)
        contexto = visualizacao.run(contexto)

        print('******************************************************')
        print('******************************************************')
        print('************** PROGRAMA FINALIZADO *******************')
        print('******************************************************')
        print('******************************************************')
        ii = ii + 1
    except Exception as ex:
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        erros += 1
        if erros >= erros_maximo:
            ii = ii + 1
            erros = 0
        print(str(ex))
        print('************** PROGRAMA FINALIZADO *******************')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')
        print('ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ERRO ')

    carregamento = None
    contexto = None

print('******************************************************')
print('******************************************************')
print('************** TUDO CHEGOU AO FIM ********************')
print('******************************************************')
print('******************************************************')
