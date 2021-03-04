"""
:author: Rafael
:data: 06/12/2019
"""
from src.contexto.Contexto import Contexto, EnumAtributo
from src.loggin.Loggin import Loggin, EnumLogStatus


class ModuloPadrao(Loggin):
    """
    Classe destinada para a ser o pai de todos os modulos
    """

    def __init__(self):
        super().__init__()

        self._name = __name__

        self._contexto = None

        self._necessidade = [EnumAtributo.PATH_PROJETO]


    @property
    def necessidade(self):
        """
        Defini quais os atributos necessarios para executar o modulo desejado
        """
        return self._necessidade


    @property
    def name(self):
        """
        Nome da classe em execução.
        """
        return self._name.split(".")[-1]


    def check_necessidades(self):
        """
        Verificar se a lista em self._list esta presente no contexto
        """
        tem_tudo = True
        msg = ""
        for necessidade in self._necessidade:
            if self._contexto.tem_atributo(necessidade):
                self.log(texto=f"Atritubo [{necessidade}] está definido como [{self._contexto.get_atributo(necessidade)}] (OK)")
            else:
                tem_tudo = False
                msg = f'Atributo [{necessidade}] não está definido\n{msg}'

        if not tem_tudo:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=msg)


    def run(self, contexto: Contexto) -> Contexto:
        """
        Executa o modulo desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f'Executando o {self._name}')
        self._contexto = contexto
        return self._contexto


    def carrega(self, contexto: Contexto):
        """
        Carregando módulo desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f'Carregando o {self._name}')
        self._contexto = contexto


    def after(self, contexto: Contexto) -> Contexto:
        """
        Executa o after do Redutor desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self.log(texto=f'After o {self._name}')
        self._contexto = contexto
        return self._contexto
