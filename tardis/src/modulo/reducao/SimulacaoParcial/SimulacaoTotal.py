"""
:author: Luis
:data: 03/03/2020
"""
from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.Exportacao import Exportacao
from src.modulo.EnumModulo import EnumModulo
from src.problema.Solucao import Solucao
from src.modulo.reducao.RedutorPadrao import RedutorPadrao


class SimulacaoTotal(RedutorPadrao):
    """
    Classe destinada para a efetuar a simulacao total para os melhores modelos que foram simulados de forma parcial
    """

    def __init__(self):
        super().__init__()

        self._necessidade = [] + super(SimulacaoTotal, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def run(self, contexto: Contexto):
        """
        Metodo responsavel por simular de forma total as melhores simulacoes ao ser utilizado
        redutor com simulacao parcial

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        super(SimulacaoTotal, self).run(contexto)

        n_melhores = 10

        solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

        iteracao_sim_total = max(map(int, solucoes.solucoes)) + 1

        melhores_solucoes = solucoes.conjunto_melhores_solucoes(n_melhores).solucoes

        for it in melhores_solucoes:
            for id in melhores_solucoes[it]:
                solucao_sim_total = melhores_solucoes[it][id]

                solucao = Solucao(id=id,
                                        iteracao=iteracao_sim_total,
                                        solucao=solucao_sim_total)

                self.log(arquivo=__name__, texto=f'Solucao de it={it}, id={id} sera simulado de forma total')
                solucao.geral = f'SIMULACAO TOTAL do it = {it} id = {id}'
                solucoes.add_in_solucoes(solucao)

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, solucoes, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [iteracao_sim_total], True)

        gevts_templates = self._contexto.get_gevts_templates(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE))
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR, gevts_templates, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR, EnumValues.TOTAL.name, True)

        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)

        self._contexto = avaliacao.run(self._contexto)

        Exportacao().csv(self._contexto)
        Exportacao().obejto(self._contexto)
