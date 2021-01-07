import sys
from src.inout.InOut import InOut
import os
from enum import Enum


def root():
    root_path = sys.path[0]
    is_src_tests_root = os.path.basename(root_path) == 'src' or os.path.basename(root_path) == 'tests'
    if is_src_tests_root:
        return '\\'.join([root_path,'..'])
    return root_path


class PathsFiles(Enum):
    name_folder_mocks = 'mocks'
    folder_src = os.path.join(root(),'src')
    folder_tests = os.path.join(root(), 'tests')
    folder_area_test_mero = os.path.join('H:\\','UNITTEST')
    folder_projeto_mero = os.path.join(folder_area_test_mero,'otimizacao')

    file_config_src = os.path.join(folder_src,'configuracao.config')
    folder_mocks = os.path.join(folder_tests, name_folder_mocks)

    folder_projeto_teste = os.path.join(folder_tests, 'area_teste')
    folder_base = os.path.join(folder_projeto_teste, 'base')

    folder_base_mocks = os.path.join(folder_mocks, 'otimizadores', 'base')
    folder_base_mero = os.path.join(folder_projeto_mero, '..', 'base')
    file_relativo_config_mero = os.path.join(folder_base_mero, 'configuracao.config')

    file_config_test = os.path.join(folder_base, 'configuracao.config')
    file_relativo_config_test = os.path.join('..','base', 'configuracao.config')
    file_relativo_config_funcoes_test = os.path.join('base', 'configuracao.config')

    file_relativo_funcoes_teste = os.path.join('..', name_folder_mocks,'funcoes_teste')
    file_relativo_rastrigin = os.path.join(file_relativo_funcoes_teste, 'rastrigin.py')
    file_relativo_rosenbrock = os.path.join(file_relativo_funcoes_teste, 'rosenbrock.py')
    file_relativo_sphere = os.path.join(file_relativo_funcoes_teste, 'sphere.py')
    file_relativo_dominio = os.path.join(file_relativo_funcoes_teste, 'dominio_sintetico50_rest5.txt')


def src():
    return os.path.join(root(),'src')


def configuracao_base():
    return os.path.join(src(),'configuracao.config')


def path_relativo_mocks():
    return InOut().ajuste_path('tests\\mocks')


def path_mocks():
    return InOut().ajuste_path('\\'.join([root(), path_relativo_mocks()]))


def path_projeto():
    return InOut().ajuste_path('\\'.join([path_mocks(), 'projeto']))


def path_otimizadores():
    return InOut().ajuste_path('\\'.join([path_mocks(), 'otimizadores']))


def path_idlhc():
    return InOut().ajuste_path('\\'.join([path_otimizadores(), 'idlhc']))


def path_idlhc_rastringin():
    return InOut().ajuste_path('\\'.join([path_otimizadores(), 'idlhc_rastringin']))


def path_mcc():
    return InOut().ajuste_path('\\'.join([path_otimizadores(), 'mcc']))


def path_mcc_rastringin():
    return InOut().ajuste_path('\\'.join([path_otimizadores(), 'mcc_rastringin']))


def path_base():
    return InOut().ajuste_path('\\'.join([path_otimizadores(), 'base']))


def path_relativo_config():
    return 'configuracao.config'


def nome_arquivo_configuracao_reest():
    return 'configuracao_resume.config'


def nome_arquivo_configuracao():
    return 'configuracao.config'


def path_arquivo_configuracao():
    return InOut().ajuste_path('\\'.join([path_projeto() , nome_arquivo_configuracao()]))


def nome_arquivo_exemplo():
    return 'arquivo_com_cabecalho_2_linhas_3_colunas.csv'


def path_arquivo_exemplo():
    return InOut().ajuste_path('\\'.join([path_mocks(), nome_arquivo_exemplo()]))


def path_arquivo_log():
    return InOut().ajuste_path('\\'.join([path_projeto(), 'log_test.out']))
