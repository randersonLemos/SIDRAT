"""
:author: Rafael
:data: 10/12/2019
"""
import copy

import pandas as pd

from src.contexto.EnumAtributo import EnumValues
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.problema.Solucao import Solucao


class Solucoes(Loggin):
    def __init__(self):
        """
        Classe coleção de soluções
        """
        super().__init__()

        self._name = __name__

        self._solucoes = {}  # Dicionário para coleção de soluções

        self._melhor_solucao = Solucao(0, 0)

        self._solucoes_serializado = {}


    @property
    def solucoes(self) -> dict:

        """
        Retorna o dicionario com todas as solucoes
        :return: Retorna as solucoes
        """
        return self._solucoes

    def add_in_solucoes(self, solucao: Solucao, sobrescreve: bool = False) -> bool:

        """
        Método que adiciona solucao a lista, e verifica se já existe igual

        :param Solucao solucao: É a solucao para ser adcionada
        :param bool sobrescreve: Se quando encontrar uma solucao igual, deve sobrescrever. Padrão é não
        :return: Retorna True ou False, para verificar se a adição ocorreu corretamente.
        """

        if solucao is None:
            self.log(texto='Não pode add uma solucao None.')
            return False

        identificador = copy.deepcopy(solucao.id)
        iteracao = copy.deepcopy(solucao.iteracao)

        if iteracao in self._solucoes:
            if len(self._solucoes[iteracao]) > 0:
                if identificador in self._solucoes[iteracao]:
                    if sobrescreve:
                        self._solucoes[iteracao][identificador] = copy.deepcopy(solucao)
                        self._add_serializado(solucao)
                        self.log(texto=f'A solucao com iteração [{iteracao}] e id [{identificador}] foi sobrescrita.')
                        return True
                    else:
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'A Coleção já contem a solucao com iteração [{iteracao}] e id [{identificador}]. Não foi adicionada')
                        return False
                else:
                    self._solucoes[iteracao][identificador] = solucao
                    self._add_serializado(solucao)
            else:
                self._solucoes[iteracao][identificador] = solucao
                self._add_serializado(solucao)
        else:
            self._solucoes[iteracao] = {identificador: solucao}
            self._add_serializado(solucao)
        return True

    def _add_serializado(self, solucao):
        try:
            if solucao.serializacao() not in self._solucoes_serializado:
                self._solucoes_serializado[solucao.serializacao()] = {'iteracao': solucao.iteracao, 'id': solucao.id}
        except Exception as ex:
            if str(type(self._solucoes_serializado)) is not str(type({})):
                self._solucoes_serializado = {}
            for iteracao in self._solucoes:
                for id in self._solucoes[iteracao]:
                    self._solucoes_serializado[self._solucoes[iteracao][id].serializacao()] = {'iteracao': iteracao, 'id': id}

    def get_solucoes_by_iteracao_para_avaliar(self, iteracao: [int]) -> dict:

        """
        Método para obter as solucoes, para avaliar, são as soluções que não tem erro e não foram avaliadas ainda.

        :param [int] iteracao: Número que identifica a iteração
        :return: Retorna as solucoes que não tem erro e não foram avaliadas
        :rtype: dict
        """

        try:
            retorno = {}
            if iteracao is not None:
                if type(1) == type(iteracao):
                    iteracao = [iteracao]

                for it in iteracao:
                    if it in self._solucoes:
                        solucoes = self._solucoes[it]

                        for solucao in solucoes.values():
                            deve_add = False
                            if solucao.has_erro == "" or solucao.has_erro is None:
                                deve_add = True
                            if deve_add is True and solucao.avaliada is False:
                                if solucao.iteracao not in retorno:
                                    retorno[solucao.iteracao] = {solucao.id: solucao}
                                else:
                                    retorno[solucao.iteracao][solucao.id] = solucao

            if len(retorno) <= 0:
                self.log(tipo=EnumLogStatus.WARN, texto=f'Nenhuma estratégia com iteracao {iteracao} foi encontrada.')

            return retorno

        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro para obter solucao', info_ex=str(ex))
            return {}

    def get_solucoes_by_iteracao(self, iteracao: [int]) -> dict:

        """
        Método para obter as solucoes, atravez da iteracao. Detalhe todas as soluções mesmo as com erro são devolvidas.

        :param [int] iteracao: Número que identifica a iteração
        :return: Retorna as solucoes que atendem ao critério de busca
        :rtype: dict
        """

        try:
            retorno = {}
            if iteracao is not None:
                if type(1) == type(iteracao):
                    iteracao = [iteracao]
                for it in iteracao:
                    if it in self._solucoes:
                        retorno[it] = self._solucoes[it]

            if len(retorno) <= 0:
                self.log(tipo=EnumLogStatus.WARN, texto=f'Nenhuma estratégia com iteracao {iteracao} foi encontrada.')

            return retorno

        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro para obter solucao', info_ex=str(ex))
            return {}

    def get_solucao_by_iteracao_id(self, iteracao: int, id: int) -> Solucao:
        """
        Método para obter as solucao com iteracao e id.

        :param int iteracao: Número que identifica a iteração
        :param int id: Número do identificador
        :return: Retorna a solucao que atendem ao critério de busca
        :rtype: Solucao
        """

        if iteracao in self._solucoes:
            if id in self._solucoes[iteracao]:
                return self._solucoes[iteracao][id]
        self.log(tipo=EnumLogStatus.ERRO, texto=f'Nenhuma estratégia com iteracao {iteracao} e id {id} foi encontrada.')
        return None


    def data_frame(self, iteracao: [int] = None, identificador: int = None, com_erro: bool = False) -> pd.DataFrame:
        """
        Converte as solucoes em um dataFrame. Seguindo a regra: Se identificar = None, retorna todas as estratégias da iteracao definida, Se iteração nao definida retorna todas as estratégias.

        TODO :param [int] iteracao: Número que identifica a iteração
        :param int identificador: Número do identificador
        TODO :param bool com_erro: Se igual a True retorna todas com erro, Se igual False retorna todas sem erro. Se igual None retorna tudo.
        :return: Retorna o data frame da opção selecionada
        :rtype: pd.DataFrame
        """

        # TODO fazer busca por lista de iteracao
        df = pd.DataFrame()
        if iteracao is not None:

            if iteracao in self._solucoes:
                if identificador is None:
                    for kEst, vEst in self._solucoes[iteracao].items():
                        df = pd.concat([df, vEst.data_frame()], axis=0)
                    return df
                else:
                    if identificador in self._solucoes[iteracao]:
                        return self._solucoes[iteracao][identificador].data_frame()
        else:
            for kIte, vIte in self._solucoes.items():
                for kEst, vEst in vIte.items():
                    df = pd.concat([df, vEst.data_frame()], axis=0)
            return df

        self.log(tipo=EnumLogStatus.WARN,
                 texto=f'Nenhuma estratégia com iteracao {iteracao} e id {identificador} foi encontrada.')
        return df


    def to_save(self) -> list:
        """
        Retorna um lista de dicionarios com a ordenação para salvar, e no dicionario com o nome da coluna e valor.
        :return: uma lista de dicionarios.
        """
        estats = []
        for iteracao in self._solucoes:
            for id in self._solucoes[iteracao]:
                estats.append(self._solucoes[iteracao][id].to_save())
        return estats


    def existe_solucao(self, solucao: Solucao, retorna_solucao=False):
        try:
            tamanho = len(self._solucoes_serializado)
        except Exception:
            if str(type(self._solucoes_serializado)) is not str(type({})):
                self._solucoes_serializado = {}
            self._add_serializado(solucao)

        if solucao.serializacao() in self._solucoes_serializado:
            # A solucao encontrada é a mesma da solução busca
            if solucao.id == self._solucoes_serializado[solucao.serializacao()]['id'] and solucao.iteracao == self._solucoes_serializado[solucao.serializacao()]['iteracao']:
                pass
            else:
                if retorna_solucao:
                    iteracao = self._solucoes_serializado[solucao.serializacao()]['iteracao']
                    id = self._solucoes_serializado[solucao.serializacao()]['id']
                    return True, self._solucoes[iteracao][id]
                else:
                    return True
        if retorna_solucao:
            return False, None
        else:
            return False

    # TODO dominio para falar se usa ou nao iteracoes negativas
    def melhor_solucao(self, nome_of_mono=None):
        if len(self._solucoes) < 1:
            return None
        if self._melhor_solucao.id == 0 and self._melhor_solucao.iteracao == 0:
            self._melhor_solucao = copy.deepcopy(self._solucoes[0][0])

        for it in self._solucoes:
            for id in self._solucoes[it]:
                if (self._solucoes[it][id].has_erro is None) and (self._solucoes[it][id].iteracao >= 0):
                    eh_maior = True
                    if len(self._melhor_solucao.of) > 0:
                        if nome_of_mono is None:
                            for nome_of in self._solucoes[it][id].of:
                                direcao = 1
                                if self._melhor_solucao.of[nome_of].direcao in EnumValues.MIN.name:
                                    direcao = -1
                                if nome_of in self._melhor_solucao.of and (direcao * self._melhor_solucao.of[nome_of].valor) >= (direcao * self._solucoes[it][id].of[nome_of].valor):
                                    eh_maior = False
                        else:
                            nome_of = nome_of_mono
                            direcao = 1
                            if self._melhor_solucao.of[nome_of].direcao in EnumValues.MIN.name:
                                direcao = -1
                            if nome_of in self._melhor_solucao.of and (direcao * self._melhor_solucao.of[nome_of].valor) >= (direcao * self._solucoes[it][id].of[nome_of].valor):
                                eh_maior = False
                    if eh_maior:
                        self._melhor_solucao = copy.deepcopy(self._solucoes[it][id])
        return self._melhor_solucao


    def serializacao(self):
        lista_serialiazado = []
        for solucoes_in in self._solucoes.values():
            for solucao_in in solucoes_in.values():
                lista_serialiazado.append(solucao_in.serializacao())
        return lista_serialiazado


    def conjunto_melhores_solucoes(self, quantidade=10, nome_of_mono=None, iteracao=None):
        """
        método responsavel por retornar o conjunto das n melhores estratégias. Elas nao estão ordenadas.

        :param contexto: Contexto
        :param resgatar: int
        :return solucoes: Solucoes
        """
        solucoes_of = []
        ordenacao = "("
        lista_interacao = list(map(int, self.solucoes))
        if iteracao is not None:
            lista_interacao = [iteracao]
        for it in lista_interacao:
            for id in list(map(int, self.solucoes[it])):
                if it >= 0:
                    aux = {'it': it, 'id': id}
                    if nome_of_mono is None:
                        for nome_of in self.solucoes[it][id].of:
                            if nome_of not in ordenacao:
                                ordenacao += f"x['{nome_of}'],"
                            aux[nome_of] = self.solucoes[it][id].of[nome_of].valor
                    else:
                        nome_of = nome_of_mono
                        if nome_of not in ordenacao:
                            ordenacao += f"x['{nome_of}'],"
                        aux[nome_of] = self.solucoes[it][id].of[nome_of].valor
                    solucoes_of.append(aux)

        ordenacao = ordenacao[:-1] + ")"
        ordenacao = f"lambda x: {ordenacao}"
        reverse = True
        if self.solucoes[it][id].of[nome_of].direcao in EnumValues.MIN.name:
            reverse = False
        solucoes_of.sort(key=eval(ordenacao), reverse=reverse)

        n_solucoes = len(solucoes_of)
        if n_solucoes < quantidade:
            quantidade = n_solucoes

        melhores_solucoes = Solucoes()
        for solucao in solucoes_of[0:quantidade]:
            melhores_solucoes.add_in_solucoes(self.solucoes[solucao['it']][solucao['id']])

        return melhores_solucoes


    def remove_iteracao(self, it):
        if self.solucoes[it]:
            for id in self._solucoes[it]:
                del self._solucoes_serializado[self._solucoes[it][id].serializacao()]
            del self._solucoes[it]
        else:
            self.log(EnumLogStatus.WARN, texto=f'Iteracao nao removida. Iteracap {it} não existente')


    def remove_iteracao_id(self, it, id):
        if self.solucoes[it]:
            if self.solucao[it][id]:
                del self._solucoes_serializado[self._solucoes[it][id].serializacao()]
                del self._solucoes[it][id]
        else:
            self.log(EnumLogStatus.WARN, texto=f'Iteracao nao removida. Iteracap {it} e id {id} não existente')


    def solucoes_it_para_menos1(self, it):
        solucoes = self.get_solucoes_by_iteracao(it)
        if solucoes:
            if self.get_solucoes_by_iteracao(-1):
                self.remove_iteracao(-1)
            for id, solucao in solucoes[it].items():
                new_solucao = Solucao(solucao=solucao, iteracao=-1, id=id)
                new_solucao.of = solucao.of
                new_solucao.economico = solucao.economico
                self.add_in_solucoes(new_solucao)
            self.remove_iteracao(it)

    #def __repr__(self):
    #    stg = ''
    #    for ite in self._solucoes:
    #        stg += '{}\n'.format(ite)
    #        for idd in self._solucoes[ite]:
    #            stg += '{} : {}\n'.format(idd, self._solucoes[ite][idd])
    #    return stg
