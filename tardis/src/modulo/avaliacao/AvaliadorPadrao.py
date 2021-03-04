"""
:author: Luis Otavio
:data: 28/04/2020
"""

from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.modulo.avaliacao.Resgate import Resgate
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes


class AvaliadorPadrao(Loggin):
    """
    Classe destinada a fazer pre e pos processos da avaliacao.
    """
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._necessidade = [EnumAtributo.AVALIACAO_TYPE]

        self._contexto = None

        self._nome_of_mono = None

        self._nomes_direcoes_of = None


    def before(self):
        self.log(texto=f"Before {self._name}")

        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)
        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO):
            self._nome_of_mono = self._contexto.get_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, valor_unico_list=True)[0]

        self._retira_solucoes_repetida_avaliacao()


    def run(self):
        """
        Executa o avaliador desejado.

        """
        self.log(texto=f"Executando {self._name}")


    def after(self):
        self.log(texto=f"After {self._name}")

        self._atualiza_solucao_para_avaliada_e_qtd_avaliacoes()


    def update_contexto(self, contexto):
        self._contexto = contexto


    @property
    def contexto(self):
        """
        contexto com todas as informações necessárias
        :return:
        """
        return self._contexto


    @property
    def necessidade(self):
        """
        Defini quais os atributos necessarios para executar o modulo desejado
        """
        return self._necessidade


    def _atualiza_solucao_para_avaliada_e_qtd_avaliacoes(self):
        qtd_avaliacao = 0
        if self._contexto.tem_atributo(EnumAtributo.QTD_SOLUCES_AVALIADAS):
            qtd_avaliacao = self._contexto.get_atributo(EnumAtributo.QTD_SOLUCES_AVALIADAS)

        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

        list_solucoes = solucoes.get_solucoes_by_iteracao(iteracoes)
        if len(list_solucoes) <= 0:
            return

        for k_iteracao, v_solucoes in list_solucoes.items():
            qtd_avaliacao += len(v_solucoes)
            for id in list_solucoes[k_iteracao]:
                solucoes.solucoes[k_iteracao][id].set_avaliada()
        self._contexto.set_atributo(EnumAtributo.QTD_SOLUCES_AVALIADAS, [qtd_avaliacao], True)


    def _retira_solucoes_repetida_avaliacao(self):
        try:
            iteracao_avaliar = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR)
            solucoes_historico: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
            solucoes_avaliar = solucoes_historico.get_solucoes_by_iteracao_para_avaliar(iteracao_avaliar)
            qtd_solucoes_novas = 0
            for iteracao in solucoes_avaliar:
                for id in solucoes_avaliar[iteracao]:
                    qtd_solucoes_novas += 1
                    solucao: Solucao = solucoes_avaliar[iteracao][id]
                    existe, solucao_repetida = solucoes_historico.existe_solucao(solucao, retorna_solucao=True)
                    if existe is True:
                        if solucao_repetida.of_valida():
                            try:
                                solucao.of = solucao_repetida.of
                                solucao.set_avaliada()
                                qtd_solucoes_novas -= 1
                                if "REPETIDA" not in solucao.geral:
                                    solucao.geral += f'[REPETIDA|it:{solucao_repetida.iteracao}|id:{solucao_repetida.id}]'
                            except Exception as ex:
                                self.log(tipo=EnumLogStatus.ERRO, texto=f"Erro ao recurar solucao [it:{solucao_repetida.iteracao}|id:{solucao_repetida.id}].", info_ex=str(ex))
            self._contexto.set_atributo(EnumAtributo.INTERNO_CRITERIO_PARADA_QTD_SOLUCAO_NOVA, [qtd_solucoes_novas], sobrescreve=True)
        except Exception as ex:
            self.log(texto="Erro ao recuperar solução repetida.", tipo=EnumLogStatus.ERRO, info_ex=str(ex))


    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto
