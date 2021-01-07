"""
:author: Rafael
:date: 09/12/2019
"""
from enum import Enum


class EnumLogStatus(Enum):
    """
    Classe com os enuns para os tipo de logs
    """

    INFO = 1
    """
    Mensagem de Informacao
    """

    WARN = 2
    """
    Mensagem de aviso de algo com possível problemas
    """

    ERRO = 3
    """
    Algo que deu errado, mas o processamento pode continuar
    """

    ERRO_FATAL = 4
    """
    Erro que proíbe a continuação do processamento
    """