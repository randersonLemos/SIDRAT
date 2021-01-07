"""
:author: Rafael
:data: 06/12/2019
"""


from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.inicializacao.InicializadorPadrao import InicializadorPadrao
from src.modulo.inicializacao.default.Default import Default
from src.modulo.inicializacao.resume.Resume import Resume
from src.loggin.Enum import EnumLogStatus
from src.modulo.ModuloPadrao import ModuloPadrao


class Inicializador(ModuloPadrao):
    """
    Classe destinada para a inicializacao das informações setadas na configuração
    """


    def __init__(self):
        super().__init__()

        self._name = __name__
        self._necessidade = self._necessidade + [EnumAtributo.INICIALIZACAO_TYPE]
        self._inicializador = InicializadorPadrao()


    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        #super().carrega(contexto)

        self.log(texto=f'Carregando o {self._name}')
        self._contexto = contexto

        if self._contexto.tem_atributo(EnumAtributo.INICIALIZACAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.INICIALIZACAO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.DEFAULT.name) or (tipo == EnumValues.DEFAULT):
                self.log(texto=f"O modulo de inicialização [{EnumValues.DEFAULT.name}] foi definido.")
                self._inicializador = Default()

            elif (tipo == EnumValues.RESUME.name) or (tipo == EnumValues.RESUME):
                self.log(texto=f"O modulo de inicialização [{EnumValues.RESUME.name}] foi definido.")
                self._inicializador = Resume()

            else:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"O método de inicialização definido [{tipo}] não existe. Somente existe os métodos {EnumValues.DEFAULT.name} e {EnumValues.RESUME.name}")

            self._necessidade += self._inicializador.necessidade


    def run(self, contexto) -> Contexto:
        """
        Executa o inicializador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._inicializador.name
        self._contexto = super(Inicializador, self).run(contexto)

        self._inicializador.run(self._contexto)
        return self._inicializador.contexto
