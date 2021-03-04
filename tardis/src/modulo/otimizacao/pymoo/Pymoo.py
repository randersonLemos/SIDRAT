"""
:author: Nome_do_autor
:data: dd/mm/aaaa
"""

from pymoo.algorithms.nsga3 import NSGA3
# from src.otimizacao.pymoo.Problema_Solucao import my_callback
# from src.otimizacao.pymoo.Problema_Solucao import MyRepair
from pymoo.algorithms.so_de import DE
from pymoo.configuration import Configuration
from pymoo.factory import get_algorithm
from pymoo.factory import get_reference_directions
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize

from src.contexto.Contexto import Contexto, EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.modulo.otimizacao.pymoo.ProblemaSolucao import ProblemaSolucao

Configuration.show_compile_hint = False


class Pymoo(OtimizadorPadrao):
    """
    Isto é um comentário da classe MyClass
    """

    def __init__(self):

        super(Pymoo, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.INICIALIZACAO_DOMINIO,
                             EnumAtributo.PATH_RESULTADO,
                             EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX,
                             EnumAtributo.OTIMIZACAO_PYMOO_POPULATON]
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._algoritmo_tipo = None
        self._tamanho_populacao = None
        self._variaveis = None
        self._simulacoes_max = None

    @property
    def otimizador(self):
        return self._algoritmo_tipo

    @otimizador.setter
    def otimizador(self, otimizador):
        self._algoritmo_tipo = otimizador

    def inicializacao(self):
        super(Pymoo, self).inicializacao()

        self._tamanho_populacao = int(self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_PYMOO_POPULATON))
        self._variaveis = self._solucao_base.get_variavies_by_tipo()
        self._simulacoes_max = self._contexto.get_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX)

    def run(self):
        """
        Executa a otimizacao usando o método MCC.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o contexto atualizado
        :rtype: Contexto
        """
        super(Pymoo, self).run()
        problema = self._problema()
        algorithm = self._algorithm()

        res = minimize(problema,
                       algorithm,
                       termination=('n_eval', self._simulacoes_max),
                       seed=int(self._contexto.get_atributo(EnumAtributo.RANDOM_SEED)),
                       save_history=True,
                       verbose=True
                       )

        return problema.contexto

    def _problema(self):
        xu = []
        n_var = len(self._variaveis)
        n_obj = 1
        if self._nome_of_mono is None:
            n_obj = len(self._nomes_direcoes_of)

        for variavel in self._variaveis:
            xu.append(len(self._variaveis[variavel].dominio.niveis) - 1)

        return ProblemaSolucao(n_var=n_var, n_obj=n_obj, xl=0, xu=xu, contexto=self._contexto, otimizador=self._algoritmo_tipo.name, nome_of_mono=self._nome_of_mono)

    def _algorithm(self):
        if self._algoritmo_tipo == EnumValues.PYMOO_DE:
            return self._de()

        if self._algoritmo_tipo == EnumValues.PYMOO_GA:
            return self._ga()

        if self._algoritmo_tipo == EnumValues.PYMOO_NSGA3:
            return self._nsga3()

    def _de(self) -> object:
        sampling = get_sampling("int_random")

        algorithm = DE(
            pop_size=self._tamanho_populacao,
            sampling=sampling,
            variant="DE/rand/1/bin",
            CR=0.5,
            F=0.3,
            dither="vector",
            jitter=False
        )
        return algorithm

    def _ga(self) -> object:
        sampling = get_sampling("int_random")
        crossover = get_crossover("int_sbx")
        mutation = get_mutation("int_pm")

        algorithm = get_algorithm("ga",
                                  pop_size=self._tamanho_populacao,
                                  sampling=sampling,
                                  crossover=crossover,
                                  mutation=mutation,
                                  eliminate_duplicates=True
                                  )

        return algorithm

    def _nsga3(self) -> object:
        sampling = get_sampling("int_random")
        crossover = get_crossover("int_sbx")
        mutation = get_mutation("int_pm")
        # create the reference directions to be used for the optimization
        if self._nome_of_mono is None:
            ref_dirs = get_reference_directions("das-dennis", len(self._nomes_direcoes_of), n_partitions=len(self._variaveis))
        else:
            ref_dirs = get_reference_directions("das-dennis", 1, n_partitions=len(self._variaveis))

        algorithm = NSGA3(pop_size=self._tamanho_populacao,
                          sampling=sampling,
                          crossover=crossover,
                          mutation=mutation,
                          ref_dirs=ref_dirs,
                          eliminate_duplicates=True)

        return algorithm




