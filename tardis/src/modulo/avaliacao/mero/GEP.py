"""
:author: Rafael
:data: 19/12/2019
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Terminal import Terminal
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes


class GEP(Loggin):
    """
    Classe que executa a GEP
    """

    def __init__(self):
        """
        Classe para construção do arquivo gevt.mero
        """
        super().__init__()

        self._name = __name__
        self._contexto = None
        self._qualificador = None
        self._gevts_templates = None

    def run(self, contexto: Contexto) -> Contexto:
        """
        Executa a classe
        :param Contexto contexto: Variavel de contexto que conte todas as informações
        :return: A variavel de contexto
        :rtype: Contexto
        """

        self.log(texto=f'Executando o {self._name}')
        self._contexto = contexto
        self._gevts_templates = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)

        mero_executavel = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_EXECUTAVEL)

        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        iteracoes_str = ""
        for ss in iteracoes:
            iteracoes_str = f'{iteracoes_str}_{ss}'
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)
        prefixo_quali_itera = f'{self._qualificador}{iteracoes_str}'

        path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        path_simulacao = self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)
        path_unimap = InOut.ajuste_path(f'{path_projeto}/{self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIMAP_PATH)}')

        solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        list_solucoes = solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
        if len(list_solucoes) < 1:
            return self._contexto

        for gevt_template in self._gevts_templates:
            path_completo_destino = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{prefixo_quali_itera}_{gevt_template}_gep.mero')

            cont = f"*SIMULATOR {self._contexto.get_atributo(EnumAtributo.SIMULADOR_NOME)} {self._contexto.get_atributo(EnumAtributo.SIMULADOR_VERSAO)}\n"
            cont += '*MODEL_LIST\nID'

            sol: Solucao = list(list(list_solucoes.values())[0].values())[0]
            for nome, valor in sol.get_variaveis_nome_valor().items():
                cont += ' {}'.format(nome)
            cont += '\n'

            for k_iteracao, v_est in list_solucoes.items():
                for k_id, vv_est in v_est.items():
                    aux_path_simula   = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{prefixo_quali_itera}_{vv_est.id}_{gevt_template}.unievent')
                    aux_path_template = InOut.ajuste_path(f'{path_projeto}/{self._gevts_templates[gevt_template]["template_path"]}')
                    valor_variavel = ""
                    for nome, valor in vv_est.get_variaveis_nome_valor().items():
                        valor_variavel += f' {valor}'
                    cont += f'{prefixo_quali_itera}_{vv_est.id}_{gevt_template} {valor_variavel} {aux_path_template} {aux_path_simula} {path_unimap}\n'
            try:
                if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_GEP_INCLUDE_PATH):
                    include_gep = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEP_INCLUDE_PATH)
                    cont_gep = TXT().ler(path_arquivo=InOut.ajuste_path(f'{path_projeto}/{include_gep}'))
                    for linha in cont_gep:
                        cont+=linha

                if not TXT().salvar(path_arquivo=path_completo_destino, conteudo=cont):
                    solucoes = self._set_erro(list_solucoes, solucoes)

                self.log(texto="CHAMANDO O MERO")
                comando = f'{InOut.ajuste_path(str(mero_executavel))} gep -i {path_completo_destino} -l INFO'
                if Terminal().run(comando) is False:
                    solucoes = self._set_erro(list_solucoes, solucoes)
            except Exception as ex:
                self.log(texto="Erro ao executar GEP", tipo=EnumLogStatus.WARN, info_ex=str(ex))
                solucoes = self._set_erro(list_solucoes, solucoes)

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, [solucoes], True)
        return self._contexto

    def _set_erro(self, list_solucoes: dict, solucoes: Solucoes) -> Solucoes:
        for k_iteracao, v_est in list_solucoes.items():
            for k_id, vv_est in v_est.items():
                self.log(texto=f'Erro ao executar a GEP para  a solucao interacao {vv_est.iteracao}, id {vv_est.id}', tipo=EnumLogStatus.WARN)
                solucoes.get_solucao_by_iteracao_id(vv_est.iteracao, vv_est.id).has_erro = "GEVT"
        return solucoes
