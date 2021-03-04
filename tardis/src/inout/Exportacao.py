"""
:author: Rafael
:data: 06/12/2019
"""
import os
import pickle

from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin


class Exportacao(Loggin):
    """
    Classe destinada para a efetuar a exportacao dos resultados
    """

    def __init__(self):
        super().__init__()

        self._name = __name__

        self._contexto = None


    def csv(self, contexto, nome=None):
        """
        Método interno para salvar CSV com dados da otimização
        """

        self._contexto = contexto

        conteudo_solucao_csv = self._gerar_conteudo_solucoes_csv()

        try:

            iteracao_max = max(self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes)

            path_csv = InOut().ajuste_path('/'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), f'/{self._contexto.get_atributo(EnumAtributo.PATH_RESULTADO)}.csv'])).format(str(iteracao_max))
            if nome is not None:
                path_csv = InOut().ajuste_path('/'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), f'/{self._contexto.get_atributo(EnumAtributo.PATH_RESULTADO)}.csv'])).format(str(nome))

            if not TXT().salvar(path_csv, conteudo_solucao_csv):
                self.log(tipo=EnumLogStatus.WARN, texto='Erro ao salvar CSV da otimização.')

        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto='Erro ao salvar CSV da otimização.', info_ex=str(ex))


    def _gerar_conteudo_solucoes_csv(self) -> str:
        """
        Método interno geracao do conteudo do CSV com os dados de otimizacao
        """
        try:
            solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes

            if not solucoes:
                return ""

            conteudo = ""

            iteracao = list(solucoes)[0]
            _id = list(solucoes[iteracao])[0]
            lista_cabecalho = [list(a)[0] for a in solucoes[iteracao][_id].to_save()]

            conteudo += ';'.join(lista_cabecalho) + '\n'

            for iteracao in solucoes:
                for _id in solucoes[iteracao]:
                    dados_solucao = solucoes[iteracao][_id].to_save()
                    for item_cabecalho in lista_cabecalho:
                        aux_conteudo = ""
                        for _id_item, item_solucao in enumerate(dados_solucao):
                            if item_cabecalho == list(item_solucao)[0]:
                                aux_conteudo = f'{item_solucao[item_cabecalho]}'
                                del dados_solucao[_id_item]
                                break
                        conteudo += aux_conteudo + ';'
                    conteudo = conteudo[:-1] + '\n'

            return conteudo[:-1]

        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto='Erro ao gerar conteudo de exportacao do csv.', info_ex=str(ex))
            return ""

    def objeto(self, contexto: Contexto, nome=None):
        """
        Método interno para salvar contexto com os dados da otimização
        """

        try:
            self._contexto = contexto
            iteracao_max = max(self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes)
            path_objeto = InOut().ajuste_path('/'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), f'/{self._contexto.get_atributo(EnumAtributo.PATH_RESULTADO)}.rst'])).format(str(iteracao_max))
            if nome is not None:
                path_objeto = InOut().ajuste_path('/'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), f'/{self._contexto.get_atributo(EnumAtributo.PATH_RESULTADO)}.rst'])).format(str(nome))
            with open(path_objeto, 'wb') as file:
                pickle.dump(self._contexto, file)
        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao exportar objeto.', info_ex=str(ex))
