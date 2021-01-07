import os
import pytest
import shutil

from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Copy import Copy
import tests.utilitarios.PathsFiles as paths_files

copy = Copy()
copy.set_arquivo_log(paths_files.path_arquivo_log())


def test_de_criação_de_folder():
    nome_diretorio_auxiliar1 = 'mocks2'
    nome_diretorio_auxiliar2 = 'mocks3\\'

    path_criacao_folder = '\\'.join([paths_files.path_mocks(), nome_diretorio_auxiliar1, nome_diretorio_auxiliar2])
    path_remocao_folder = '\\'.join([paths_files.path_mocks(), nome_diretorio_auxiliar1])

    path_criacao_folder = InOut().ajuste_path(path_criacao_folder)
    path_remocao_folder = InOut().ajuste_path(path_remocao_folder)

    if not copy.criar_arquivos(path_criacao_folder):
        pytest.fail('Criacao de folder falhou')
    if not os.path.isdir(path_criacao_folder):
        pytest.fail('Folder nao foi criado')

    try:
        shutil.rmtree(path_remocao_folder)
    except Exception as ex:
        pytest.fail(f'Nao foi possivel remover folder criado. Erro :[{ex}]')


def test_de_copia_de_arquivo_quando_folder_destino_eh_existente():
    path_arquivo_para_copia = paths_files.path_arquivo_exemplo()
    path_arquivo_copiado = '\\'.join([paths_files.path_mocks(), 'arquivo_copiado.txt'])

    path_arquivo_copiado = InOut().ajuste_path(path_arquivo_copiado)

    if not copy.copy_file(path_arquivo_para_copia, path_arquivo_copiado):
        pytest.fail('erro ao copiar arquivo')
    if not InOut().arquivo_existe(path_arquivo_copiado):
        pytest.fail('arquivo copiado nao foi gerado')
    if not TXT().ler(path_arquivo_copiado) == TXT().ler(path_arquivo_para_copia):
        pytest.fail('conteudo arquivo copiado nao eh igual ao original')

    try:
        os.remove(path_arquivo_copiado)
    except Exception as ex:
        pytest.fail(f'Nao foi possivel remover arquivo gerado. Erro :[{ex}]')


def test_de_copia_de_arquivo_quando_folder_destino_nao_eh_existente():
    nome_diretorio_auxiliar1 = 'mocks2'
    nome_diretorio_auxiliar2 = 'mocks3\\'

    path_arquivo_para_copia = paths_files.path_arquivo_exemplo()

    path_arquivo_copiado = '\\'.join([paths_files.path_mocks(), nome_diretorio_auxiliar1,
                                      nome_diretorio_auxiliar2, 'arquivo_copiado.txt'])
    path_arquivo_copiado = InOut().ajuste_path(path_arquivo_copiado)

    path_remocao_folder = '\\'.join([paths_files.path_mocks(), nome_diretorio_auxiliar1])
    path_remocao_folder = InOut().ajuste_path(path_remocao_folder)

    if not copy.copy_file(path_arquivo_para_copia, path_arquivo_copiado):
        pytest.fail('Criacao de arquivo copiado falhou')
    if not os.path.isfile(path_arquivo_copiado):
        pytest.fail('Arquivo nao foi copiado')
    if not TXT().ler(path_arquivo_copiado) == TXT().ler(path_arquivo_para_copia):
        pytest.fail('conteudo arquivo copiado nao eh igual ao original')

    try:
        shutil.rmtree(path_remocao_folder)
    except Exception as ex:
        pytest.fail(f'Nao foi possivel remover folder criado. Erro :[{ex}]')
