"""
:author: Luis
:data: 03/03/2020
"""
import glob
import os

from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.Copy import Copy
from src.inout.InOut import InOut
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin


class Resgate(Loggin):
    """
    Classe destinada para a efetuar o salvamento dos dados de simulação por algum critério
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

        self._qualificador = None
        """
        Variavel com o nome do qualificador
        """

        self._resgatar = 10

    def melhores(self, contexto: Contexto):
        """
        Metodo responsavel por salvar as melhores simulacoes dentro de uma pasta definida na configuracao.
        Caso melhores simulacoes ocorram, as piores dentro da pasta são apagadas

        :param contexto:
        :return bool: True caso o metodo tenha funcionado corretamente
        """
        self._contexto: Contexto = contexto
        self._resgatar = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MELHORES_QTD_SALVAR)
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)
        nome_of = None
        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO):
            nome_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, valor_unico_list=True)[0]

        solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        melhores_solucoes = solucoes.conjunto_melhores_solucoes(quantidade=self._resgatar, nome_of_mono=nome_of)

        try:
            dados_copiar_origem, dados_copiar_destino, paths_dados_manter = self._gera_paths_origem_e_destino(melhores_solucoes)

            paths_melhores_resultados = self._gera_paths_melhores_resultados()

            self._salvar(dados_copiar_origem, dados_copiar_destino)

            self._remover(dados_copiar_destino, paths_melhores_resultados, paths_dados_manter)
            return self._contexto
        except Exception as ex:
            self.log(tipo=Warning, texto=f'Houve erro ao salvar melhores solucoes [{ex}]')

    def _gera_paths_melhores_resultados(self):

        path_melhores_resultados = InOut().ajuste_path('\\'.join(
            [self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
             self._contexto.get_atributo(EnumAtributo.AVALIACAO_PATH_MELHORES), '\\']))

        paths = glob.glob('\\'.join([path_melhores_resultados, '*']))

        paths = [InOut().ajuste_path(path) for path in paths]

        return paths

    def _salvar(self, dados_copiar_origem, dados_copiar_destino):
        for dado_copiar_origem, dado_copiar_destino in zip(dados_copiar_origem, dados_copiar_destino):
            self.log(texto=f'copiando dados {os.path.basename(dado_copiar_origem)}')
            if not Copy.copy_file(dado_copiar_origem, dado_copiar_destino, replace=False):
                self.log(
                    texto=f'Arquivo {dado_copiar_origem} nao foi salvo na pasta de melhores estratégias. Arquivo ja existente.')

    def _remover(self, dados_copiar_destino, paths_melhores_resultados, paths_dados_manter):
        arquivos_apagar = list((set(paths_melhores_resultados) - set(dados_copiar_destino))-set(paths_dados_manter))
        for arquivo_apagar in arquivos_apagar:
            try:
                self.log(texto=f'apagando dos melhores resultados {os.path.basename(arquivo_apagar)}')
                os.remove(arquivo_apagar)
            except Exception as ex:
                self.log(tipo=EnumLogStatus.WARN, texto=f'Problema de remocao de {arquivo_apagar}. Erro=[{ex}]')

    def _gera_paths_origem_e_destino(self, solucoes):
        solucoes = solucoes.solucoes

        path_melhores_resultados = InOut().ajuste_path('\\'.join(
            [self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
             self._contexto.get_atributo(EnumAtributo.AVALIACAO_PATH_MELHORES), '\\']))
        path_simulacao = InOut().ajuste_path('\\'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
                                                        self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)]))

        dados_copiar_origem = list()
        dados_copiar_destino = list()
        dados_manter = list()

        paths_dados_manter = list()
        nome_melhores_solucoes = list()
        for it in list(map(int, solucoes)):
            for id in list(map(int, solucoes[it])):
                if solucoes[it][id].of_valida():
                    nome_melhores_solucoes.append(f'_{it}_{id}_')

        for nome_melhor_solucao in nome_melhores_solucoes:
            str_pesquisa_melhor_solucao = InOut.ajuste_path(
                '\\'.join([path_simulacao, '*' + nome_melhor_solucao + '*']))

            str_pesquisa_solucao_existentes = InOut.ajuste_path(
                '\\'.join([path_melhores_resultados, '*' + nome_melhor_solucao + '*']))

            dados_copiar_origem += (glob.glob(str_pesquisa_melhor_solucao))
            dados_manter += (glob.glob(str_pesquisa_solucao_existentes))

        dados_copiar_destino += \
            [InOut.ajuste_path('\\'.join([path_melhores_resultados, os.path.basename(dado_copiar_origem)])) for
             dado_copiar_origem in dados_copiar_origem]

        paths_dados_manter += \
            [InOut.ajuste_path('\\'.join([path_melhores_resultados, os.path.basename(dado_copiar_origem)])) for
             dado_copiar_origem in dados_manter]

        return dados_copiar_origem, dados_copiar_destino, paths_dados_manter
