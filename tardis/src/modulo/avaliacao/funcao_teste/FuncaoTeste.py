"""
:author: Luis Otavio
:data: 28/04/2020
"""
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.loggin.Loggin import EnumLogStatus
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.modulo.problemas_fechados.funcoes_teste.base.clustering import clustering
from src.modulo.problemas_fechados.funcoes_teste.base.knapsack import knapsack
from src.modulo.problemas_fechados.funcoes_teste.base.rastrigin import rastrigin
from src.modulo.problemas_fechados.funcoes_teste.base.rosenbrock import rosenbrock
from src.modulo.problemas_fechados.funcoes_teste.base.sphere import sphere
from src.problema.Solucoes import Solucoes


class FuncaoTeste(AvaliadorPadrao):
    def __init__(self, tipo_funcao_teste: EnumValues):

        super(FuncaoTeste, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_TYPE] + super(FuncaoTeste, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._tipo_funcao_teste = tipo_funcao_teste

        self._funcao = None

        self._solucoes = Solucoes()

    def _get_funcao_teste(self):
        if EnumValues.RASTRIGIN == self._tipo_funcao_teste:
            return rastrigin.getResult
        elif EnumValues.ROSENBROCK == self._tipo_funcao_teste:
            return rosenbrock.getResult
        elif EnumValues.SPHERE == self._tipo_funcao_teste:
           return sphere.getResult
        elif EnumValues.KNAPSACK == self._tipo_funcao_teste:
           return knapsack.getResult
        elif EnumValues.CLUSTERING == self._tipo_funcao_teste:
           return clustering.getResult

    def run(self):
        """
        Metodo responsavel por utilizar avaliadores em arquivos externos python.
        O arquivo deve possuir o metodo getResult(dict_variaveis)
        """
        super(FuncaoTeste, self).run()
        try:
            if self._funcao is None:
                self._funcao = self._get_funcao_teste()

            iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
            self._solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

            list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)

            for it in list_solucoes:
                for id in list_solucoes[it]:
                    dict_variaveis = {}
                    solucao = self._solucoes.get_solucao_by_iteracao_id(iteracao=it, id=id)

                    for nome, valor in solucao.get_variaveis_nome_valor().items():
                        valor_var = valor
                        if valor_var.__class__ is str:
                            valor_var = 0
                        dict_variaveis.update({nome: valor_var})
                    of = -1 * float('inf')
                    avaliada = True
                    try:
                        of = self._funcao(dict_variaveis)
                    except Exception as ex:
                        avaliada = False
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao calcular of com o metodo getResult em {self._tipo_funcao_teste.name}: [{ex}]')
                    self._solucoes.get_solucao_by_iteracao_id(iteracao=it, id=id).of[self._nome_of_mono].valor = of
                    self._solucoes.get_solucao_by_iteracao_id(iteracao=it, id=id).set_avaliada()
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto="Erro ao recuperar valor da funca.", info_ex=str(ex))