import tests.utilitarios.PathsFiles as paths_files
from src.loggin.Loggin import Loggin
from src.inout.InOut import InOut
import platform

inout = InOut()
Loggin().set_arquivo_log(paths_files.path_arquivo_log())

def test_ajuste_barras():
    path_desajustado = '..\\\\mocks/exemplo.txt'
    path_win = '..\\mocks\\exemplo.txt'
    path_lin = '../mocks/exemplo.txt'

    if platform.system().upper() == "WINDOWS":
        assert inout.ajuste_path(path_desajustado) == path_win
    else:
        assert inout.ajuste_path(path_desajustado) == path_lin


def test_de_existencia_de_arquivo():

    assert inout.arquivo_existe(paths_files.path_arquivo_exemplo()) == True


def test_de_nao_existencia_de_arquivo():

    path_mocks = paths_files.path_mocks()
    path_arquivo_inexistente = inout.ajuste_path('\\'.join([path_mocks,'arquivo_inexistente.txt']))

    assert inout.arquivo_existe(path_arquivo_inexistente) is False


def test_de_ajuste_de_informacoes_em_strings():

    errors = []

    if not 1.1 == inout.ajusta_entrada('1.1'):
        errors.append('erro transformacao para float')
    if not 1 == inout.ajusta_entrada('1') or (int is not type(inout.ajusta_entrada('1'))):
        errors.append('erro transformacao para int')
    if not inout.ajusta_entrada('tRUE'):
        errors.append('erro transformacao para bool True')
    if inout.ajusta_entrada('fALSE'):
        errors.append('erro transformacao para bool False')
    if not '123x456y' == inout.ajusta_entrada('123x456y'):
        errors.append('erro manter str com mesmo valor do str')
    if not '2015.10' == inout.ajusta_entrada("'2015.10'"):
        errors.append('erro ')

    assert not errors, "ocorrencia de erros:\n{}".format("\n".join(errors))


def test_de_ajuste_de_ids_e_iteracoes():

    assert inout.ajusta_id_iteracao(400) == '00400'


