"""
:author: Rafael
:data: 10/12/2019
"""
from src.loggin.Loggin import Loggin
from src.loggin.Enum import EnumLogStatus
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.inout.InOut import InOut


class Dominio(Loggin):

    def __init__(self, nome, niveis=None, probabilidade=None, default=None, equacao=None, tipo=EnumTipoVariaveis.VARIAVEL):
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._nome = nome
        """
        Nome do dominio, é a chave para os dominios
        """

        self._tipo = tipo
        """
        Tipo do dominio, ver class EnumTipoDominio
        """

        self._niveis = niveis
        """
        Lista que discretiza os valores possível para o dominio
        """

        self._equacao = equacao
        """
        Equacao de condicional da variavel
        """

        self._probabilidade = probabilidade
        """
        Lista discretizada dos nível de probabilidade para cada valor possível
        """

        self._default = default
        """
        Valor default para o dominio
        """


    @property
    def nome(self):
        return self._nome


    @property
    def probabilidade(self):
        return self._probabilidade


    @property
    def niveis(self):
        return self._niveis


    @property
    def equacao(self):
        return self._equacao


    @property
    def default(self):
        return self._default


    @property
    def tipo(self):
        return self._tipo


    def get_valor(self, valor):
        """
        Verificar se o valor esta na lista de problema e retornar o valor assim como a posicao.
        :param valor: valor da lista
        :type valor: object
        :return: Valor e posicao
        :rtype: object, int(None)
        """
        if valor is None:
            valor = self._default

        if valor in self._niveis:
            return valor, self._niveis.index(valor)

        return None, None


    def get_posicao(self, posicao: int) -> tuple:
        """
        Verificar se a posicao esta dentro dos limites do problema, retorna a posicao assim com o valor.
        :param posicao: o valor da posicao no array
        :type posicao: int
        :return: Posicao, Valor
        :rtype: int, object
        """
        if posicao is None:
            posicao = self._niveis.index(self._default)
        if (posicao >= 0) and (posicao < len(self._niveis)):
            return posicao, self._niveis[posicao]
        return None, None


    @probabilidade.setter
    def probabilidade(self, probabilidade):
        """
        A atualização da probabilidade não altera o objeto original, mas criar uma copia de um novo objeto
        :param probabilidade: lista de probabilidade para inserir, ou número para colocar em todas as posições
        :type probabilidade: list ou float
        :return: O objeto dominio com a probabilide atualizada
        :rtype: Dominio
        """
        prob_equi = []
        for ii in range(len(self._niveis)):
            prob_equi.append(1 / len(self._niveis))

        if (type(0.1) == type(probabilidade)) or (type(1) == type(probabilidade)):
            aux_p = []
            for ii in range(len(self._niveis)):
                aux_p.append(probabilidade)
            probabilidade = aux_p

        if (probabilidade is None) or (len(probabilidade) == 0):
            self.log(tipo=EnumLogStatus.WARN,
                     texto=f"A probabilidade esta vazia. Assim a probabilidade ser equiprovável [{prob_equi}].")
#            probabilidade = prob_equi
        else:
            if not len(self._niveis) == len(probabilidade):
                self.log(tipo=EnumLogStatus.WARN,
                         texto=f"A quantidade de niveis da probabilidade [{len(probabilidade)}] é diferente do problema [{len(self._niveis)}]. Assim a probabilidade ser equiprovável [{prob_equi}].")
#                probabilidade = prob_equi
            else:
                if round(sum(probabilidade), 7) > 1:
                    self.log(tipo=EnumLogStatus.WARN,
                             texto=f"A somatória das probabilidade [{round(sum(probabilidade),7)}] é maior que 1. Assim a probabilidade ser equiprovável [{prob_equi}].")
#                    probabilidade = prob_equi
                if round(sum(probabilidade), 7) < 1:
                    self.log(tipo=EnumLogStatus.WARN,
                             texto=f"A somatória das probabilidade [{round(sum(probabilidade),7)}] é menor que 1.")

        self._probabilidade = probabilidade


    def to_string(self):
        #stg  = 'nome = {}; '.format(self.nome)
        #stg += 'valor default = {}; '.format(self._default)
        #stg += 'tipo = {}\n'.format(self.name)
        #stg += 'dominio       {' + ', '.join(['{:+.3f}'.format(el) for el in self._niveis]) + '}\n'
        #stg += 'probabilidade {' + ', '.join(['{:+.3f}'.format(el) for el in self._probabilidade]) + '}'
        #return stg

        return "Nome: {};\tDominio: {};\tProbabilidade: {};\tDefault: {};\tTipo: {}".format(self.nome
                                                                                            , self._niveis
                                                                                            , self._probabilidade
                                                                                            , self._default
                                                                                            , self._tipo.name
                                                                                           )
