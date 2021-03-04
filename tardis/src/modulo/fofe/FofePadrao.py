"""
:author: Randerson Lemos
:data: 010/01/2021
"""

from src.loggin.Loggin import Loggin
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo


class FofePadrao(Loggin):
    """
    Classe pai de todas as FOFES
    """


    def __init__(self):
        super().__init__()

        self._name = __name__

        self._solucao = None

        self._contexto = None

        self._necessidade = []


    def update_contexto(self, contexto):
        self._contexto = contexto
