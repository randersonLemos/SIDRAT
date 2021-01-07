import pytest
from src.inout.Terminal import Terminal
import tests.utilitarios.PathsFiles as paths_files

terminal = Terminal()
terminal.set_arquivo_log(paths_files.path_arquivo_log())


def test_de_execucao_terminal_com_valor_valido():
    assert terminal.run('dir') is True


def test_de_execucao_terminal_com_valor_nao_valido():
    assert terminal.run('comando nao inexiste') is False
