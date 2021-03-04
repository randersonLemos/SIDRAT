"""
:author: Rafael
:data: 10/12/2019
"""

import pandas as pd

from copy import deepcopy

from src.contexto.EnumAtributo import EnumValues
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Variaveis import Variaveis
from src.problema.Variavel import Variavel


class Of:
    def __init__(self, nome, valor=None, direcao=EnumValues.MAX.name):
        if valor is None:
            self._valor = Solucao.of_padrao(direcao)

        else:
            self._valor = valor

        self._nome = nome

        self._direcao = direcao


    @property
    def nome(self):
        return self._nome


    @property
    def direcao(self):
        return self._direcao


    @property
    def valor(self):
        return self._valor


    @valor.setter
    def valor(self, valor):
        self._valor = valor


class Solucao(Loggin):
    @staticmethod
    def of_padrao(direcao=EnumValues.MAX.name):
        """
        Determina qual o valor padrão para a of.

        :return: retorna o valor padrão para of.
        """
        if direcao in EnumValues.MIN.name:
            return float("inf")
        return float('-inf')


    @staticmethod
    def validar_of(of) -> bool:
        """
        Faz a checagem correta para verificar se a of tem um valor válido

        :return: True se for valida, e False se for inválida
        """
        if str(of) != str(float('-inf')) and str(of) != str(float('inf')) and of is not None:
            return True
        return False


    def __init__(self, id, iteracao, solucao=None):
        """
        Construtor de objectos solucao.

        :param int id: número único que identifica a estratégia, frente todas as estratégias
        :param int iteracao: qual o passo do otimizador
        """
        super().__init__()

        self._name = __name__  # Nome do arquivo

        self._has_erro = None  # Informa a ocorrencia de erros

        self._economico = None  # Armazena os dados economicos (vem de ferramentas externas)

        self._id = id  # identifica solução

        self._avaliada = False  # Verifica se solução foi avaliada

        self._iteracao = iteracao  # Iteração é um conjunto de estratégias (uma passo da otimização)

        self._geral = ""

        self._variaveis = Variaveis()

        self._of = {}  # Destinado a armazenas varias ofs

        if solucao:
            self._variaveis = deepcopy(solucao.variaveis)
            for nome_of in solucao.of:
                self.of = Of(nome_of, direcao=solucao.of[nome_of].direcao)

    @property
    def geral(self) -> str:
        """
        Campo destinado a colocar qualquer informação de interece

        :return: Retorna o que estiver gravado em geral, preferencialmente str
        """
        return self._geral


    @property
    def id(self) -> int:
        """
        Retorna o id da solucao

        :return: Retorna o id
        """
        return self._id


    @property
    def iteracao(self) -> int:
        """
        Retorna a intereacao da solucao

        :return: Retorna a solucao
        """
        return self._iteracao


    @property
    def has_erro(self) -> str:
        """
        Informa o erro da solucao

        :return: Retorna o erro na solucao
        """
        return self._has_erro


    @has_erro.setter
    def has_erro(self, erro: str = None):
        """
        Seta o erro da solucao. Se ja existir um erro o novo erro é adcionado.
        :param str erro: Erro encontrado na solucao
        """
        if (erro is None) or (str(erro) == ""):
            self._has_erro = None
        else:
            if self._has_erro is None:
                self._has_erro = erro
            else:
                self._has_erro = f'{self._has_erro}>[{erro}]'


    @property
    def economico(self) -> pd.DataFrame:
        """
        Retorna os dados economicos obtidos.

        :return: dados economico
        """
        return self._economico


    @property
    def variaveis(self) -> Variaveis:
        """
        Retorna o objeto com todas as variaveis
        :return: retorna todas as variaveis
        :rtype: Variaveis
        """
        return self._variaveis


    @property
    def avaliada(self) -> bool:
        """
        Retorna um bool informando se a solução é repetida

        :return: retorna True se é repetida, False se é unica
        :rtype: bool
        """
        return self._avaliada


    @property
    def of(self) -> dict:
        """
        Retorna o dicionario de ofs
        :return: Retorna um dicionario de of
        """
        if self._of is None:
            self._of = {}
        return self._of


    @of.setter
    def of(self, of) -> None:
        """
        Inclui a of no dicionario de ofs.
        :param of: Objeto da classe of
        """
        try:
            self._check_tudo()
            if of is not None and str(type(of)) == str(type(Of(None))):
                if of.nome in self._of:
                    if Solucao.validar_of(self._of[of.nome].valor) and Solucao.validar_of(of.valor):
                        self.log(tipo=EnumLogStatus.WARN, texto=f'A of [{of.nome}] tera seu valor substituido de [{self._of[of.nome].valor}] para [{of.valor}]')

                self._of[of.nome] = deepcopy(of)
                if Solucao.validar_of(of.valor):
                    self._avaliada = True

            elif str(type(of)) == str(type({})):
                self._avaliada = True
                for of_nome in of:
                    if of_nome in self._of:
                        if Solucao.validar_of(self._of[of_nome].valor) and Solucao.validar_of(of[of_nome].valor):
                            self.log(tipo=EnumLogStatus.WARN, texto=f'A of [{of[of_nome].nome}] tera seu valor substituido de [{self._of[of.nome].valor}] para [{of[of_nome].valor}]')

                    self._of[of_nome] = Of(of_nome, valor=of[of_nome].valor, direcao=of[of_nome].direcao)

                    if not Solucao.validar_of(self._of[of_nome].valor):
                        self._avaliada = False
            else:
                self.log(tipo=EnumLogStatus.ERRO, texto="Of envida não é do tipo especificado.")
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto="Erro ao setar of", info_ex=str(ex))


    @geral.setter
    def geral(self, geral):
        try:
            self._geral = f'{geral}'
        except Exception as ex:
            self.log(texto='Não é possivel gravar o tipo [{type(geral}] no campo geral, será atribuido vazio ao campo.', info_ex=str(ex), tipo=EnumLogStatus.ERRO)


    @economico.setter
    def economico(self, economico: pd.DataFrame):
        """
        Seta os dados economicos obtidos.

        :param pd.DataFrame economico: Dados economicos
        """
        self._economico = economico


    def set_avaliada(self):
        """
        Seta se a solução foi avaliada. Para ser TRUE todas as ofs tem de ser TRUE.

        :param avaliada: True se for repetida, e False se for unica
        """
        avaliada = []
        for of_nome in self._of:
            if not Solucao.validar_of(self._of[of_nome].valor):
                avaliada.append(1)

        if sum(avaliada) > 0:
            self._avaliada = False
        else:
            self._avaliada = True


    def add_in_variaveis(self, variaveis):
        """
        Adicionar uma variavel um lista de variaveis em variaveis

        :param list variaveis: Uma ou uma lista de variaveis
        """
        if not isinstance(variaveis, list):
            variaveis = [variaveis]

        for variavel in variaveis:
            self._variaveis.add_in_variaveis(variavel)


    def get_variavies_by_tipo(self, tipo=EnumTipoVariaveis.VARIAVEL) -> dict:
        """
        Retorna as variaveis

        :param EnumTipoDominio.VARIAVEL tipo: qual o tipo de variavel que deseja buscar.
        :return: As variaveis do tipo selecionado
        :rtype: Variaveis
        """
        return self._variaveis.get_variaveis_by_tipo(tipo)


    def get_variaveis_nome_valor(self):
        """
        Retorna um dicionario de chave = nome, valor = valor real da variavel
        :return: dicionario
        """

        variaveis = {}

        for key, variavel in self._variaveis.get_variaveis_by_tipo(EnumTipoVariaveis.VARIAVEL).items():
            variaveis[variavel.nome] = variavel.valor

        for key, variavel in self._variaveis.get_variaveis_by_tipo(EnumTipoVariaveis.CONSTANTE).items():
            variaveis[variavel.nome] = variavel.valor

        for key, variavel in self._variaveis.get_variaveis_by_tipo(EnumTipoVariaveis.CONDICIONAL).items():
            equacao = None
            equacao_aux = None
            try:
                equacao = variavel.dominio.equacao
                equacao_aux = variavel.dominio.equacao
                equacao_aux = equacao_aux.replace('(', '')
                equacao_aux = equacao_aux.replace(')', '')
                condicoes = equacao_aux.split()
                for condicao in condicoes:
                    if condicao in variaveis:
                        valor = variaveis[condicao]
                        equacao = equacao.replace(condicao, f"({str(valor)})")

                valor = eval(equacao)
                variaveis[variavel.nome] = valor
            except Exception as ex:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Erro para escrever equacao [{equacao_aux}] => [{equacao}].", info_ex=str(ex))

        return variaveis


    def data_frame(self):
        df = pd.DataFrame({'id': [self._id],
                           'iteracao': [self._iteracao],
                           'has_erro': [self._has_erro],
                           'OF': [self.of],
                           'serializado': self.serializacao()
                           },
                          index=[self._id])

        dfv = self._variaveis.data_frame()
        dfv.index = [self.id]
        df = pd.concat([df, dfv], axis=1)

        return df


    def to_string(self) -> str:
        """
        Converte o objeto em string

        :return: o objeto convertido em string
        :rtype: str
        """
        has_erro = "" if self._has_erro is None else self._has_erro
        est = f"'iteracao': {self._iteracao}, 'id': {self._id}, 'has_erro': {has_erro}"
        for of_nome in self._of:
            est = est + f"of[{self._of[of_nome].direcao}_{of_nome}]: {self._of[of_nome].valor}, "
        est = est + f"'geral': {self._geral},"
        est = est + self._variaveis.to_string()
        return str(est)


    def serializacao(self) -> str:
        """
        Serializa o objecto

        :return: objeto serializado
        """

        string = f"{self._variaveis.serializacao()}"
        return string


    def to_save(self) -> list:
        """
        Retorna um lista de dicionarios com a ordenação para salvar, e no dicionario com o nome da coluna e valor.
        As colunas são id, iteracao, has_erro_of + as variaveis

        :return: uma lista de dicionarios.
        """
        has_erro = self._has_erro
        if self._has_erro is None:
            has_erro = ''

        est = [{'iteracao': self._iteracao}, {'id': self._id}, {'has_erro': has_erro}]
        for of_nome in self._of:
            est = est + [{f'of[{self._of[of_nome].direcao}_{of_nome}]': self._of[of_nome].valor}]
        est = est + [{'geral': self._geral}]

        est = est + self._variaveis.to_save()
        return est


    def copy(self, iteracao, id):
        solucao = deepcopy(self)
        solucao._id = id
        solucao._iteracao = iteracao
        return deepcopy(solucao)


    def of_valida(self):
        """
        Valida as ofs da solucao
        :return: T F
        :rtype: bool
        """
        if len(self._of) > 0:
            for of_nome in self._of:
                if not Solucao.validar_of(self._of[of_nome].valor):
                    return False
            return True
        else:
            return False


    def _check_tudo(self):
        if self._of is None:
            self._of = {}
