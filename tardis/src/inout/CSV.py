"""
:author Rafael:
:date 07/01/2020
"""
from src.inout.InOut import InOut
from src.loggin.Loggin import Loggin, EnumLogStatus
import pandas as pd


class CSV(InOut, Loggin):
    """
    Classe destinada para manipulacao de arquivos do tipo texto, csv.
    """

    def __init__(self):
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def ler(self, path_arquivo: str, headers: bool = True, index_col: bool = True, lines_ignore: int = -1, sep: str = ';') -> pd.DataFrame:
        """
        Método responsavel por ler arquivos csv e transformar em dataframe
        :param str path_arquivo: caminho onde localiza o arquivo
        :param bool headers: se deve considerar que o arquivo tem cabeçalho ou não.
        :param bool index_col: se deve considerar que o arquivo tem index ou não.
        :param int lines_ignore: Quantidade de linhas que deve ser ignoradas antes de estar ler o cvs
        :param str sep: tipo do separador usado.
        :return: Retorna o pd.DataFrame do arquivo csv
        :rtype: pd.DataFrame
        """

        path_arquivo = self.ajuste_path(path_arquivo)

        if sep == '\t':
            sep = ','
            delim_whitespace = True
        else:
            delim_whitespace = False

        try:
            if headers:
                header = 'infer'
                skiprows = [i for i, line in enumerate(open(path_arquivo)) if i <= lines_ignore]
                if index_col:
                    df = pd.read_csv(path_arquivo, sep=sep, index_col=0, header=header, skiprows=skiprows, delim_whitespace=delim_whitespace)
                else:
                    df = pd.read_csv(path_arquivo, sep=sep, header=header, skiprows=skiprows, delim_whitespace=delim_whitespace)
            else:
                if index_col:
                    df = pd.read_csv(path_arquivo, sep=sep, index_col=0, header=None, delim_whitespace=delim_whitespace)
                else:
                    df = pd.read_csv(path_arquivo, sep=sep, header=None, delim_whitespace=delim_whitespace)
                df.index.name = None
                df.columns = range(len(df.columns))
            return df

        except FileNotFoundError as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao abrir arquivo [{path_arquivo}]', info_ex=str(ex))
        except PermissionError as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao abrir arquivo [{path_arquivo}]', info_ex=str(ex))
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao abrir arquivo [{path_arquivo}]', info_ex=str(ex))
        return pd.DataFrame()

    def salvar(self, path_arquivo: str, conteudo: str, metodo_gravacao:str = "w") -> bool:
        if type(conteudo) is pd.Series:
            conteudo.to_csv(path_arquivo,header=True)
        pass
