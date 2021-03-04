"""
:author Rafael:
:date 02/05/2019
"""
from src.inout.InOut import InOut
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.inout.Copy import Copy


class TXT(InOut, Loggin):
    """
    Classe destinada para manipulacao de arquivos do tipo texto, txt.
    """

    def __init__(self):
        #super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def ler(self, path_arquivo: str) -> list:
        """
        Método responsavel por leitura dos arquivos

        :param str path_arquivo: caminho do arquivo
        :return: Um array com todas as linhas do arquivo
        :rtype: list
        """

        path_arquivo = TXT().ajuste_path(path_arquivo)
        if not TXT().arquivo_existe(path_arquivo):
            self.log(tipo=EnumLogStatus.ERRO, texto=f"Arquivo {path_arquivo} nao existe.")
            return [None]

        retorno = []
        arquivo = None
        try:
            arquivo = open(path_arquivo, 'r')
            for linha in arquivo:
                retorno.append(linha)
        except FileNotFoundError as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto="Erro ao abrir arquivo", info_ex=f'{ex}')
        except PermissionError as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto="Erro ao abrir arquivo", info_ex=f'{ex}')
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto="Erro ao abrir arquivo", info_ex=f'{ex}')
        finally:
            arquivo.close()

        return retorno

    def salvar(self, path_arquivo: str, conteudo: str, metodo_gravacao:str = "w") -> bool:
        """
        Método para salvar conteudo de arquivos

        :param str path_arquivo: Caminho do arquivo
        :param str conteudo: Conteudo a ser salvo
        :param str metodo_gravacao: Método de gravação, padrão w
        :return: Se deu erro ou não
        :rtype: bool
        """
        path_arquivo = InOut.ajuste_path(path_arquivo)

        try:
            if not Copy.criar_arquivos(path_arquivo):
                return False
            arq = open(path_arquivo, metodo_gravacao)
            arq.write(conteudo)
            arq.close()
        except FileNotFoundError as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao salvar arquivo.', info_ex=str(ex))
            return False
        except PermissionError as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao salvar arquivo.', info_ex=str(ex))
            return False
        except TypeError as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao salvar arquivo.', info_ex=str(ex))
            return False
        except NameError as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao salvar arquivo.', info_ex=str(ex))
            return False
        except IOError as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao salvar arquivo.', info_ex=str(ex))
            return False
        return True
