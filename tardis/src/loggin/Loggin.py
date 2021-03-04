"""
:author: Rafael
:date: 09/12/2019
"""
from datetime import datetime
import sys
from src.loggin.Enum import EnumLogStatus
import time


def _horario():
    agora = datetime.now()
    return "{}/{}/{}:{}h{}m".format(agora.year, agora.month, agora.day, agora.hour, agora.minute)


class Loggin(object):
    def __init__(self):

        global g_arquivo_log
        """
        Variavel global para definir o caminho para o arquivo de loggin.
        """

        if 'g_arquivo_log' in globals():
            self._arquivo_log = g_arquivo_log
        else:
            self._arquivo_log = None

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    @staticmethod
    def set_arquivo_log(path_arquivo_log: str) -> None:
        """
        Seta o caminho do arquivo de log

        :param str path_arquivo_log: caminho do arquivo de log
        """
        global g_arquivo_log
        g_arquivo_log = path_arquivo_log

    @property
    def arquivo_log(self) -> str:
        """
        Obtem o caminho do arquivo de log

        :return: caminho de log
        :rtype: str
        """

        global g_arquivo_log
        if 'g_arquivo_log' in globals():
            self._arquivo_log = g_arquivo_log
        else:
            self._arquivo_log = None
        return self._arquivo_log

    def log(self, arquivo: object = None, tipo: object = EnumLogStatus.INFO, texto: object = None, info_ex: object = None):
        """
        Log as informações vindas

        :param str arquivo: nome do arquivo que aconteceu a msg
        :param EnumLogStatus tipo: tipo do log se o enum LogStatus
        :param str texto: texto da mensagem
        :param st info_ex: texto caso a mensagem venha de uma exceção
        """

        if arquivo is None:
            arquivo = self._name

        if not sys.exc_info() == (None, None, None):
            if tipo.value <= EnumLogStatus.INFO.value:
                tipo = EnumLogStatus.WARN

            exc_type, exc_value, exc_traceback = sys.exc_info()
            if info_ex is None:
                info_ex = f"{exc_traceback.tb_frame.f_code.co_name}:{exc_traceback.tb_lineno}"
            else:
                info_ex = f"{exc_traceback.tb_frame.f_code.co_name}:{exc_traceback.tb_lineno}:{info_ex}"

        if info_ex is None:
            msg = f'[{_horario()}][{tipo.name}][{arquivo}] - {texto}'
        else:
            msg = f'[{_horario()}][{tipo.name}][{arquivo}] - {texto}\n\t\t\t[{info_ex}]'

        self._log_terminal(msg)
        self._log_arquivo(msg)

        if EnumLogStatus.ERRO_FATAL == tipo:
            self._log_terminal("FIM DA EXECUÇÃO, ERRO")
            self._log_arquivo("FIM DA EXECUÇÃO, ERRO")
            sys.exit(-1)


    def _log_arquivo(self, msg):
        tentar = True
        arquivo = self.arquivo_log
        arq = None

        if arquivo is None:
            sys.exit(-1)

        while tentar:
            try:
                arq = open(arquivo, 'a+')
                arq.write(f'{msg}\n')
                tentar = False

            except FileNotFoundError:
                self._log_terminal(
                    f'[{_horario()}][{EnumLogStatus.ERRO_FATAL.name}][{self._name}] - Arquivo [{self._arquivo_log}] não encontrado, tentaremos daqui 10 minutos.')
                time.sleep(10 * 60)

            except PermissionError:
                self._log_terminal(
                    f'[{_horario()}][{EnumLogStatus.ERRO_FATAL.name}][{self._name}] - Não tem permissão para abrir o arquivo [{self._arquivo_log}]')
                sys.exit(-1)

            except TypeError:
                self._log_terminal(
                    f'[{_horario()}][{EnumLogStatus.ERRO_FATA.nameL}][{self._name}] - Erro ao abrir arquivo {self._arquivo_log}')
                sys.exit(-1)

            except IOError:
                self._log_terminal(
                    f'[{_horario()}][{EnumLogStatus.ERRO_FATAL.name}][{self._name}] - Erro ao abrir arquivo {self._arquivo_log}')
                sys.exit(-1)

            finally:
                if arq is not None:
                    arq.close()
                sys.stdout.flush()


    @staticmethod
    def _log_terminal(msg):
        print(msg)
        sys.stdout.flush()


    @property
    def name(self):
        return self._name
