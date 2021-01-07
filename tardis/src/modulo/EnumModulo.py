"""
:author: Rafael
:data: 17/01/2020
"""
from enum import Enum


class EnumModulo(Enum):
    """
    Classe de enum para os módulos existentes.
    """

    REDUCAO = 1
    """
    Enum referente ao modulo de reducao
    """

    OTIMIZACAO = 2
    """
    Enum referente ao modulo de otimização
    """

    AVALIACAO = 3
    """
    Enum referente ao modulo de avaliacao
    """

    EXPORTACAO = 4
    """
    Enum referente ao modulo de exportacao
    """

    INICIALIZACAO = 5
    """
    Enum resposavel por definir qual o tipo de inicialização das variaveis fazermos
    """

    CRITERIOPARADA = 6
    """
    Enum responsavael por devolver os criterios de parada
    """

    SORTEIO = 7
    """
    Enum responsavael por devolver sorteio utilizado
    """

    PROBLEMA_FECHADO = 8
    """
    Modulo responsavel por armazenar todos os problemas fechado
    """

    VISUALIZACAO = 9
    """
    Modulo responsavael por armazenar a visualizacao selecionada
    """