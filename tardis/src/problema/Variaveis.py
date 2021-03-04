"""
:author: Rafael
:data: 11/12/2019
"""
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Variavel import Variavel
import pandas as pd


class Variaveis(Loggin):
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._variaveis = {}

        self._set_variaveis()


    def _set_variaveis(self):
        for tipo in EnumTipoVariaveis:
            self._variaveis[tipo.name] = {}


    def add_in_variaveis(self, variavel: Variavel):
        """
        Adicionar uma nova variavel a lista de variaveis

        :param Variavel variavel: variavel
        """
        for tipo in EnumTipoVariaveis:
            if variavel.nome in self._variaveis[tipo.name]:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Variavel {variavel.nome} já definida.")

        self._variaveis[variavel.dominio.tipo.name][variavel.nome] = variavel


    def get_variavel_by_nome(self, nome: str) -> Variavel:
        """
        Obtem a variavel com o nome informado

        :param str nome: Nome da variavel informado
        :return: variavel encontrada
        :rtype: Variavel
        """
        for tipo in EnumTipoVariaveis:
            if nome in self._variaveis[tipo.name]:
                return self._variaveis[tipo.name][nome]
        return None


    def set_variavel_posicao_by_nome(self, nome: str, posicao: int):

        """
        Seta o novo valor da variavel cujo novo foi informado
        :param str nome: Nome da variavel
        :param int posicao: Posicao no vetor da variavel
        """
        for tipo in EnumTipoVariaveis:
            if nome in self._variaveis[tipo.name]:
                self._variaveis[tipo.name][nome].posicao = posicao
                return

    def get_variaveis_by_tipo(self, tipo: EnumTipoVariaveis = EnumTipoVariaveis.VARIAVEL) -> dict:

        """
        Retorna as variaveis do tipo infomado
        :param EnumTipoVariaveis tipo: tipo desejado.
        :return: Variaveis encontradas
        :rtype: dict
        """
        return self._variaveis[tipo.name]

    def data_frame(self):
        df = pd.DataFrame()
        for k, v in self._variaveis.items():
            var = {}
            for kk, vv in v.items():
                var[kk] = vv.data_frame()

            df = pd.concat([df, pd.DataFrame(data={k: [var]}, index=[0], columns=[k])], axis=1)
        return df

    def to_string(self):
        string = ""
        for tipo in EnumTipoVariaveis:
            for variavel in self._variaveis[tipo.name].values():
                if string == "":
                    string = f"\n\t\t\t{variavel.to_string()}"
                else:
                    string = f"{string}\n\t\t\t{variavel.to_string()}"
        return string

    def serializacao(self):
        string = ""
        for tipo in EnumTipoVariaveis:
            for variavel in self._variaveis[tipo.name].values():
                string = f"{string}{variavel.serializacao()}"
        return string

    def to_save(self) -> list:
        """
        Retorna um lista de dicionarios com a ordenação para salvar, e no dicionario com o nome da coluna e valor.
        :return: uma lista de dicionarios.
        :rtype: list
        """
        vars = []
        for k_tipo, v_tipo in self._variaveis.items():
            for k_variavel, v_variavel in v_tipo.items():
                vars.append(v_variavel.to_save())

        return vars
