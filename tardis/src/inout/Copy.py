"""
:author: Nome_do_autor
:data: dd/mm/aaaa
"""
import os
from src.loggin.Loggin import Loggin, EnumLogStatus
import platform
from src.inout.InOut import InOut
import shutil


class Copy(Loggin):
    """
    Isto é um comentário da classe MyClass
    """

    def __init__(self):
        """
        Comentário do construtor
        """
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    @staticmethod
    def criar_arquivos(path_file: str) -> bool:
        """
        Criar toda estrutura de arquivo para depois fazer a copia do arquivo.
        :param str path_file: Deve ser o caminho do arquivo, com o nome do arquivo junto.
        :return: Se tudo correu ok
        :rtype: bool
        """

        test_path = ""
        try:
            barra = '/'
            inicio = '/'
            if platform.system().upper() == "WINDOWS":
                barra = '\\'
                inicio = ''

            path_aux = path_file.split(barra)

            for pp in range(len(path_aux)-1):
                if path_aux[pp] == "":
                    continue
                if test_path == "":
                    test_path = InOut.ajuste_path(f'{inicio}{path_aux[pp]}')
                else:
                    test_path = InOut.ajuste_path(f'{test_path}{barra}{path_aux[pp]}')

                if not os.path.isdir(test_path):
                    Loggin().log(arquivo=__name__, tipo=EnumLogStatus.WARN, texto=f'Caminho {test_path} não existe.')
                    os.mkdir(test_path)
                    Loggin().log(arquivo=__name__, tipo=EnumLogStatus.WARN, texto=f'Caminho {test_path} foi criado com sucesso.')

            return True
        except Exception as ex:
            Loggin().log(arquivo=__name__, tipo=EnumLogStatus.ERRO_FATAL, texto=f'Não foi possível diretorios [{test_path}].', info_ex=str(ex))
            return False

    @staticmethod
    def copy_file(path_origem: str, path_destino: str, replace=True ) -> bool:
        """
        Faz a copia de um arquivo para outro lugar, fazendo a checagem se existe diretorio e criando se não existir

        :param str path_origem: Caminho onde o arquivo se encontra.
        :param str path_destino: Caminho para onde o arquivo sera comiado.
        :return: se o arquivo foi copiado com sucesso ou teve erro
        :rtype: bool
        """

        try:
            if not Copy.criar_arquivos(path_destino):
                return False

            try:
                if not replace:
                    if os.path.isfile(path_destino):
                        Loggin().log(arquivo=__name__,
                                     texto=f'Arquivo [{path_destino}] já existente. Arquivo não foi copiado.')
                        return False
                shutil.copy(path_origem, path_destino)
                Loggin().log(arquivo=__name__, texto=f'Arquivo [{path_origem}] copiado com sucesso para [{path_destino}].')
            except Exception as ex:
                Loggin().log(tipo=EnumLogStatus.ERRO, arquivo=__name__, texto=f'Arquivo [{path_origem}] NÃO copiado com sucesso para [{path_destino}].', info_ex=str(ex))
                return False

            return True
        except Exception as ex:
            Loggin().log(arquivo=__name__, tipo=EnumLogStatus.ERRO_FATAL, texto=f'Não foi possível copiar aquivo de [{path_origem}] para [{path_destino}].', info_ex=str(ex))
            return False

    @staticmethod
    def copy_folder(path_origem: str, path_destino: str, replace=True) -> bool:
        """
        Faz a copia de uma pasta e todas subpastas e arquivos

        :param str path_origem: Caminho onde o folder se encontra.
        :param str path_destino: Caminho para onde o folder sera copiado.
        :param bool replace: Flag para fazer substituicao da pasta e conteudo
        :return: se o arquivo foi copiado com sucesso ou teve erro
        :rtype: bool
        """

        if replace:
            if os.path.isdir(path_destino):
                Loggin().log(texto=f'Apagando pasta {path_destino} para substituicao')
                shutil.rmtree(path_destino)
        try:
            Loggin().log(texto=f'Copiando conteudo {path_origem} para {path_destino}')
            shutil.copytree(path_origem, path_destino)
            Loggin().log(texto=f'Pasta {path_destino} gerada com sucesso')
            return True
        except Exception as ex:
            Loggin().log(tipo=EnumLogStatus.ERRO_FATAL, arquivo=__name__, texto=f'Folder [{path_origem}] NÃO copiado com sucesso para [{path_destino}].', info_ex=str(ex))
            return False
