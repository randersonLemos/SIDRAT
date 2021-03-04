"""
:author: Rafael
:data: 10/12/2019
"""
from enum import Enum


class EnumTipoVariaveis(Enum):
    """
    Descreve os tipos de variavies
    """
    #
    # TODAS = 1
    # """
    # Retornar todas as variaveis de todos os tipos
    # """

    VARIAVEL = 2
    """
    Reflete em uma variavel padrão
    """

    CONSTANTE = 3
    """
    É um paramentro constante, que o valor sera sempre o valor default
    """

    CONDICIONAL = 4
    """
    Quando uma variavel depende de outra
    """