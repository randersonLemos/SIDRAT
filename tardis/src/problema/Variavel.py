"""
:author: Rafael
:data: 11/12/2019
"""
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
import pandas as pd
from src.problema.Dominio import Dominio
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis


class Variavel(Loggin):
    def __init__(self, dominio: Dominio, valor=None, posicao=None):
        super().__init__()

        self._name = __name__

        self._dominio = dominio  # Domínio da variáveis

        self._valor = ""  # Valor da variável

        self._posicao = -1  # Posição da variável no vetor de domínio

        if self._dominio.tipo.name != EnumTipoVariaveis.CONDICIONAL.name:
            v_valor, v_posicao = self._dominio.get_valor(valor)
            p_posicao, p_valor = self._dominio.get_posicao(posicao)
            if (v_valor == p_valor) and (v_posicao == p_posicao):
                self._valor = v_valor
                self._posicao = int(v_posicao)
            else:
                self._valor = v_valor
                self._posicao = int(v_posicao)
                self.log(tipo=EnumLogStatus.WARN, texto=f'A relação entre valor[{valor}] e posição[{posicao}] no domínio[{self._dominio.niveis}] esta errada. Assim foi gravado valor[{self._valor}] e posicao[{self._posicao}].')


    @property
    def nome(self):
        return self._dominio.nome


    @property
    def valor(self):
        return self._valor


    @valor.setter
    def valor(self, valor):
        valor, posicao = self._dominio.get_valor(valor)
        self._valor = valor
        self._posicao = posicao
        # TODO print aumenta o tempo de processamento no idlhc
        #self.log(texto=f'Foi gravado valor[{self._valor}] e posicao[{self._posicao}].')


    @property
    def posicao(self):
        return int(self._posicao)


    @posicao.setter
    def posicao(self, posicao):
        if posicao < 0:
            self.log(texto='Não foi gravado nova posicao, pois é menor que zero.', tipo=EnumLogStatus.WARN)
            raise ValueError
        if posicao >= len(self._dominio.niveis):
            self.log(texto=f'Não foi gravado nova posicao da variavel [{self.nome}], pois é maior que niveis [{len(self._dominio.niveis)}].', tipo=EnumLogStatus.WARN)
            raise ValueError(f'Tamanho maximo {len(self._dominio.niveis)}')
        posicao, valor = self._dominio.get_posicao(posicao)
        self._valor = valor
        self._posicao = int(posicao)
        # TODO print aumenta o tempo de processamento no idlhc
        #self.log(texto=f'Foi gravado valor[{self._valor}] e posicao[{self.posicao}].')


    @property
    def dominio(self):
        return self._dominio


    def data_frame(self) -> pd.DataFrame():
        df = pd.DataFrame(data={'nome': self.nome, 'valor': self.valor, 'posicao': self.posicao}, index=[self.nome])
        return df


    def to_string(self):
        return f'Nome: {self._dominio.nome};\tValor: {self._valor};\tPosicao: {self.posicao};\tDominio: {self._dominio.to_string()}'


    def serializacao(self):
        return f'[{self.nome}>{self._valor}>{self.posicao}]'


    def to_save(self) -> dict:
        """
        Retorna um dicionários contendo nome : valor
        :return: um dicionario.
        :rtype: dict
        """
        return {self.nome: self.valor}
