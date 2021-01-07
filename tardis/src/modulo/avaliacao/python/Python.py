from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.loggin.Loggin import EnumLogStatus
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.modulo.avaliacao.python.interface import load_method
from src.problema.Solucao import Of


class Python(AvaliadorPadrao):
    def __init__(self):

        super(Python, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_PYTHON_PATH] + super(Python, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._solucoes = None

    def run(self):
        """
        Metodo responsavel por utilizar avaliadores em arquivos externos python.
        O arquivo deve possuir o metodo getResult(dict_variaveis)
        """

        super(Python, self).run()

        path_python = InOut.ajuste_path('/'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
                                                  self._contexto.get_atributo(EnumAtributo.AVALIACAO_PYTHON_PATH)]))

        try:
            getResult = load_method(path_python)
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao carregar o metodo getResult em {path_python}: [{ex}]')

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
                try:
                    of = getResult(dict_variaveis)
                except Exception as ex:
                    self.log(tipo=EnumLogStatus.ERRO,
                         texto=f'Erro ao calcular of com o metodo getResult em {path_python}: [{ex}]')

                self._solucoes.get_solucao_by_iteracao_id(iteracao=it, id=id).of[self._nome_of_mono].valor = of
                self._solucoes.get_solucao_by_iteracao_id(iteracao=it, id=id).set_avaliada()
