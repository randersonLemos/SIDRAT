"""
:author: Luis
:data: 20/01/2020
"""

import glob
import os

from src.contexto.Contexto import Contexto
from src.contexto.Contexto import EnumAtributo
from src.inout.InOut import InOut
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin


class Remocao(Loggin):
    """
    Classe destinada para a efetuar a exportacao dos resultados
    """

    def __init__(self):
        super().__init__()

        self._contexto = None
        """
        Variavel de armazenagem do contexto.
        """

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def run(self, contexto: Contexto):
        """
        Inicia o processo de remocao de arquivos de saida de simulaao

        :param Contexto contexto:
        """

        path_simulacao = InOut().ajuste_path('\\'.join([contexto.get_atributo(EnumAtributo.PATH_PROJETO), contexto.get_atributo(EnumAtributo.PATH_SIMULACAO), '\\']))
        try:
            import shutil
            shutil.rmtree(path_simulacao)
            self.log(texto=f'Removendo conteúdo da pasta {path_simulacao}')
        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f"Falha para remover pasta {path_simulacao}", info_ex=str(ex))

        try:
            from pathlib import Path
            path_simulacao_Path = Path(path_simulacao)
            path_simulacao_Path.mkdir()
            self.log(texto=f'Pasta {path_simulacao} criada com sucesso')
        except Exception as ex:
            import time
            time.sleep(10)
            try:
                os.mkdir(path_simulacao)
                self.log(texto=f'Pasta {path_simulacao} criada com sucesso')
            except Exception as ex:
                self.log(tipo=EnumLogStatus.WARN, texto=f"Falha para criar pasta {path_simulacao}", info_ex=str(ex))

        # extensoes_remover = ['irf', 'mrf', 'sr3', 'unitub', 'fcs.csv', 'fcp.csv',
        #                      'fci.csv', 'fc.csv', 'weofcs.csv', 'cs.csv', 'eofcs.csv', '.unipro']
        #
        # for extensao in extensoes_remover:
        #     arquivos_remover = glob.glob(f'{path_simulacao}*.{extensao}')
        #     for arquivo_remover in arquivos_remover:
        #         self.log(texto=f'Removendo o arquivo {arquivo_remover}')
        #         try:
        #             os.remove(arquivo_remover)
        #             self.log(texto=f'Removido o arquivo {arquivo_remover}')
        #         except Exception as ex:
        #             self.log(tipo=EnumLogStatus.WARN, texto=f'Falha remocao {arquivo_remover}', info_ex=str(ex))


