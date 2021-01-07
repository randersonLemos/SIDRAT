"""
:author: Rafael
:date: 09/12/2019
"""
from src.loggin.Loggin import Loggin, EnumLogStatus
import platform
import os.path


class InOut(object):
    """
    Classe com metodos staticos para ajustes
    """
    @staticmethod
    def barra() -> str:
        barra = '/'
        if platform.system().upper() == "WINDOWS":
            barra = '\\'
        return barra

    @staticmethod
    def ajuste_path(caminho: str) -> str:
        """
        Método estatico para ajustar as barras

        :param str caminho:
        :return: Devolve o caminho com o ajuste de barra por sistema operacional
        :rtype: str
        """

        barra = '/'
        if platform.system().upper() == "WINDOWS":
            barra = '\\'
            caminho = caminho.replace("/", "\\")
            caminho = caminho.replace("\\\\", "\\")
        else:
            caminho = caminho.replace("\\", "/")
            caminho = caminho.replace("//", "/")

        caminho = caminho.replace(f'{barra}{barra}', barra)
        caminho = caminho.replace("'", "")
        caminho = caminho.replace(", ", "_")
        caminho = caminho.replace(",", "_")
        caminho = caminho.replace(" ", "_")

        return str(caminho)

    @staticmethod
    def arquivo_existe(path_file: str) -> bool:
        """
        Verificar se o arquivo existe
        :param str path_file: Verifica se o arquivo existe
        :return: Devolve bool informando se o arquivo existe
        :rtype: bool
        """

        if not os.path.isfile(path_file):
            Loggin().log(tipo=EnumLogStatus.ERRO, texto=f"{path_file} arquivo nao existe.")
            return False
        return True

    @staticmethod
    def diretorio_existe(path_: str) -> bool:
        """
        Verificar se o arquivo existe
        :param str path_: Verifica se o arquivo existe
        :return: Devolve bool informando se o arquivo existe
        :rtype: bool
        """

        if not os.path.isdir(path_):
            Loggin().log(tipo=EnumLogStatus.ERRO, texto=f"{path_} diretorio nao existe.")
            return False
        return True

    @staticmethod
    def ajusta_entrada(entrada: str) -> object:
        """
        Converte do tipo str para o tipo correto da variavel.

        :param str entrada: Tipo de entrada
        :return: O valor no tipo correto
        :rtype: object
        """

        try:
            entrada = entrada.replace("\n", "")
            if 'float' in str(type(entrada)):
                return float(entrada)
            if 'int' in str(type(entrada)):
                return int(entrada)

            if str(float(entrada)) == str(entrada):
                return float(entrada)
            if str(int(entrada)) == str(entrada):
                return int(entrada)
            if entrada[0] == '+':
                if str(int(entrada[1:])) == str(entrada[1:]):
                    return int(entrada)

        except ValueError:
            try:
                return float(entrada)
            except ValueError:
                if entrada.upper() == "TRUE":
                    return True
                elif entrada.upper() == 'FALSE':
                    return False
                entrada = entrada.replace("'", "")
                return entrada

    @staticmethod
    def ajusta_id_iteracao(valor: int) -> str:
        """
        Converte o id e iteração para um formato str melhor para salvar.
        :param int valor: Valor do id e ou iteracao.
        :return: Devolve o valor no formato str com zeros antes do número
        :rtype: str
        """

        _format_id_prefix = '{:0>5}'
        return _format_id_prefix.format(valor)

    @staticmethod
    def path_to_array(path: str) -> str:
        barra = '/'
        if platform.system().upper() == "WINDOWS":
            barra = '\\'

        return path.split(barra)[1:]
