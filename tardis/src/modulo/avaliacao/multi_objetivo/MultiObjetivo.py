from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes


class MultiObjetivo(AvaliadorPadrao):
    def __init__(self):

        super(MultiObjetivo, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = super(MultiObjetivo, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._solucoes = None

    def run(self):
        """
        Metodo responsavel por utilizar avaliadores em arquivos externos python.
        O arquivo deve possuir o metodo getResult(dict_variaveis)
        """
        if self._nome_of_mono is None:
            return
        super(MultiObjetivo, self).run()

        if EnumValues.MULTIOBJETIVO.name in self._nome_of_mono:
            iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
            self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao(iteracoes)
            for it in self._solucoes:
                for id in self._solucoes[it]:
                    try:
                        for of_nome in self._nomes_direcoes_of:
                            if EnumValues.MULTIOBJETIVO.name not in of_nome:
                                exec(f'{of_nome} = {self._solucoes[it][id].of[of_nome].valor}')

                        funcao_of = self._nome_of_mono.replace(EnumValues.MULTIOBJETIVO.name, "").replace('[', '').replace(']', '').replace(EnumValues.MAX.name, "").replace(EnumValues.MIN.name, "").replace("_", "")
                        valor_funcao_of = eval(f'{funcao_of}')
                        self._solucoes[it][id].of[self._nome_of_mono].valor = valor_funcao_of
                    except Exception as ex:
                        self.log(f"Erro ao calcular função.")
                        self._solucoes[it][id].of[self._nome_of_mono].valor = Solucao.of_padrao(self._solucoes[it][id].of[self._nome_of_mono].direcao)

    def before(self):
        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO):
            self._nome_of_mono = self._contexto.get_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, valor_unico_list=True)[0]
        super(MultiObjetivo, self).before()

    def after(self):
        if self._nome_of_mono is None:
            return
        super(MultiObjetivo, self).after()

