"""
:author: Rafael
:data: 06/12/2019
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.modulo.avaliacao.funcao_teste.FuncaoTeste import FuncaoTeste
from src.modulo.avaliacao.mero.Mero import Mero
from src.modulo.avaliacao.python.Python import Python
from src.modulo.avaliacao.wahoo.Wahoo import Wahoo


class Avaliador(ModuloPadrao):
    """
    Classe destinada para carregar o modulo de avaliação setados na configuração
    """

    def __init__(self):
        super(Avaliador, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_TYPE] + super(Avaliador, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._avaliador = AvaliadorPadrao()

    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(Avaliador, self).carrega(contexto)

        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)
            if type("") == type(tipo):
                tipo = tipo.upper()

            if (tipo == EnumValues.MERO.name) or (tipo == EnumValues.MERO):
                self.log(texto=f'O modulo de inicialização [{EnumValues.MERO.name}] foi definido.')
                self._avaliador = Mero()
            if (tipo == EnumValues.CAMPO_NAMORADO_POSICIONAMENTO.name) or (tipo == EnumValues.CAMPO_NAMORADO_POSICIONAMENTO):
                self.log(texto=f'O modulo de inicialização [{EnumValues.MERO.name}] foi definido.')
                self._avaliador = Mero()
            elif (tipo == EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name) or (tipo == EnumValues.CAMPO_NAMORADO_NUMERO_POCOS):
                self.log(texto=f'O modulo de inicialização [{EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name}] foi definido.')
                self._avaliador = Mero()
            elif (tipo == EnumValues.WAHOO.name) or (tipo == EnumValues.WAHOO):
                self.log(texto=f'O modulo de inicialização [{EnumValues.WAHOO.name}] foi definido.')
                self._avaliador = Wahoo()
            elif (tipo == EnumValues.PYTHON.name) or (tipo == EnumValues.PYTHON):
                self.log(texto=f'O modulo de inicialização [{EnumValues.PYTHON.name}] foi definido.')
                self._avaliador = Python()
            elif (tipo == EnumValues.RASTRIGIN.name) or (tipo == EnumValues.RASTRIGIN):
                self.log(texto=f'O modulo de inicialização [{EnumValues.RASTRIGIN.name}] foi definido.')
                self._avaliador = FuncaoTeste(EnumValues.RASTRIGIN)
            elif (tipo == EnumValues.ROSENBROCK.name) or (tipo == EnumValues.ROSENBROCK):
                self.log(texto=f'O modulo de inicialização [{EnumValues.ROSENBROCK.name}] foi definido.')
                self._avaliador = FuncaoTeste(EnumValues.ROSENBROCK)
            elif (tipo == EnumValues.SPHERE.name) or (tipo == EnumValues.SPHERE):
                self.log(texto=f'O modulo de inicialização [{EnumValues.SPHERE.name}] foi definido.')
                self._avaliador = FuncaoTeste(EnumValues.SPHERE)
            elif (tipo == EnumValues.KNAPSACK.name) or (tipo == EnumValues.KNAPSACK):
                self.log(texto=f'O modulo de inicialização [{EnumValues.KNAPSACK.name}] foi definido.')
                self._avaliador = FuncaoTeste(EnumValues.KNAPSACK)
            elif (tipo == EnumValues.CLUSTERING.name) or (tipo == EnumValues.CLUSTERING):
                self.log(texto=f'O modulo de inicialização [{EnumValues.CLUSTERING.name}] foi definido.')
                self._avaliador = FuncaoTeste(EnumValues.CLUSTERING)

            self._necessidade += self._avaliador.necessidade

    def run(self, contexto) -> Contexto:
        """
        Executa o avaliador desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        :rtype Contexto
        """
        self._name = self._avaliador.name
        self._contexto = super(Avaliador, self).run(contexto)

        self._avaliador.contexto = self._contexto
        self._avaliador.before()
        self._avaliador.run()
        self._avaliador.after()

        return self._avaliador.contexto
