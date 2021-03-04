"""
:author: Rafael
:data: 07/09/2020
"""
from src.loggin.Loggin import Loggin
from src.modulo.ModuloPadrao import ModuloPadrao


class Modulo(Loggin):
    """
    Classe destinada para carrego os modulos
    """


    def __init__(self, obj_modulo):
        super().__init__()
        self._name = __name__
        self._modulo = obj_modulo

    def run(self, contexto):
        """
        Carrega o modulo desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self._modulo.carrega(contexto)
        self._modulo.check_necessidades()
        return self._modulo
