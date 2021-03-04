"""
:author: Randerson Lemos
:data: 01/01/2021
"""


from src.loggin.Enum import EnumLogStatus
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumValues
from src.contexto.EnumAtributo import EnumAtributo
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.fofe.FofePadrao import FofePadrao
from src.modulo.fofe.binary_classifier.BinaryClassifier import BinaryClassifier


class Fofe(ModuloPadrao):
    """
    Classe que gerencia as FOFEs
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._fofe = FofePadrao()


    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f'Carregando o {self._name}')

        self._contexto = contexto

        if self._contexto.tem_atributo(EnumAtributo.FOFE):
            tipo = self._contexto.get_atributo(EnumAtributo.FOFE)

            if isinstance(tipo, str):
                tipo = tipo.upper()

            if (tipo == EnumValues.NN_BINARY_CLASSIFIER.name) or (tipo == EnumValues.NN_BINARY_CLASSIFIER):
                self.log(texto=f"O modulo de fofe [{EnumValues.NN_BINARY_CLASSIFIER.name}] foi definido.")
                self._fofe = BinaryClassifier()

            else:
                self.log(tipo=EnumLogStatus.ERRO_FATAL,
                         texto=f"O método de fofe definido [{tipo}] não existe." +
                               f"Somente existe os métodos {EnumValues.NN_BINARY_CLASSIFIER.name}"
                        )

            for necessidade in self._fofe._necessidade:
                if necessidade not in self._necessidade:
                    self._necessidade.append(necessidade)


    def run(self):
        """
        Executa a Fofe escolhida

        :return Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f'Executando {self._name}')

        self._fofe.run(self._contexto)

        return self._fofe._contexto


    def update_contexto(self, contexto):
        self._contexto = contexto
