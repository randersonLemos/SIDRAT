import os
import shutil

import tests.utilitarios.PathsFiles as paths_files
from src.inout.InOut import InOut
from src.inout.TXT import TXT

txt = TXT()
txt.set_arquivo_log(paths_files.path_arquivo_log())


def test_de_verificacao_de_leitura_de_arquivo():
    assert txt.ler(paths_files.path_arquivo_exemplo()) == ['id;cab1;cab2\n', '1;val11;val12\n', '2;val21;val22']


def test_de_retorno_vazio_na_leitura_de_arquivo_inexistente():

    path_arquivo_inexistente = InOut().ajuste_path('\\'.join([paths_files.path_mocks(), 'arquivo_inexistente.txt']))
    assert txt.ler(path_arquivo_inexistente) == [None]


def test_para_salvar_arquivos():

    errors = []

    file_name = 'arquivo_teste.txt'
    path_arquivo_salvar = InOut().ajuste_path('\\'.join([paths_files.path_mocks(), file_name]))
    conteudo = 'teste_conteudo_linha_1\nteste_conteudo_linha_2'

    if not txt.salvar(path_arquivo_salvar, conteudo) == True:
        errors.append('erro ao salvar em caminho de pasta existente')
    if not txt.ler(path_arquivo_salvar) == ['teste_conteudo_linha_1\n', 'teste_conteudo_linha_2']:
        errors.append('erro ao comparar conteudo salvo com o lido no arquivo salvo')

    try:
        os.remove(path_arquivo_salvar)
    except Exception as ex:
        errors.append(f'erro ao apagar arquivo gerado [{ex}]')

    assert not errors, 'ocorrencia de erros:\n{}'.format('\n'.join(errors))


def test_para_salvar_arquivos_em_folders_inexistentes():

    errors = []

    folder_auxiliar = 'mocks2'
    file_name = 'arquivo_teste.txt'
    path_folder_salvar = InOut().ajuste_path('\\'.join([paths_files.path_mocks(),folder_auxiliar]))
    path_arquivo_salvar = InOut().ajuste_path('\\'.join([paths_files.path_mocks(),folder_auxiliar,file_name]))
    conteudo = 'teste_conteudo_linha_1\nteste_conteudo_linha_2'
    if not txt.salvar(path_arquivo_salvar, conteudo):
        errors.append('erro ao salvar em caminho de pasta inexistente')
    if not txt.ler(path_arquivo_salvar) == ['teste_conteudo_linha_1\n', 'teste_conteudo_linha_2']:
        errors.append('erro ao comparar conteudo salvo com o lido no arquivo salvo')

    try:
        shutil.rmtree(path_folder_salvar)
    except Exception as ex:
        errors.append(f'erro ao remover arquivo gerado [{ex}]')

    assert not errors, 'ocorrencia de erros:\n{}'.format('\n'.join(errors))