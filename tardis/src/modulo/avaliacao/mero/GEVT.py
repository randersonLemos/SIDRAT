"""
:author: Nome_do_autor
:data: dd/mm/aaaa
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Terminal import Terminal
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.modulo.avaliacao.mero.gerenciamento.Gerenciamento import Gerenciamento
from src.problema.Solucao import Solucao
from src.problema.Solucoes import Solucoes


class GEVT(Loggin):
    """
    Isto é um comentário da classe MyClass
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

        # TODO alterar o qualificador para redutor
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)

        solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        list_solucoes = solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
        if len(list_solucoes) <= 0:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Não há estudo sem erro para avaliar')
            return self._contexto

        path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        path_simulacao = self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)
        prefixo_quali_iteracoes = f'{self._qualificador}{iteracoes_str}'

        for prefixo in self._gevts_templates.keys():
            path_completo_destino = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{self._gevts_templates[prefixo]["gevt_file_name"]}.mero')

            if not self._qualificador in EnumValues.TOTAL.name:
                if not self._resecreve_time_list(path_completo_destino):
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever arquivo [{path_completo_destino}].')
                    for iteracao in iteracoes:
                        for idd in solucoes.solucoes[iteracao]:
                            solucoes.solucoes[iteracao][idd].has_erro = "GEVT"
                    continue

            for k_iteracao, v_est in list_solucoes.items():
                for k_id, vv_est in v_est.items():
                    try:
                        _path_params = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{prefixo_quali_iteracoes}_{vv_est.id}_params.txt')

                        if self._escreve_params(vv_est, _path_params, prefixo) is False:
                            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever arquivo [{_path_params}].')
                            solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "GEVT"
                            continue

                        gerenciamento = Gerenciamento()
                        gerenciamento.run(_path_params, self._contexto)

                        self.log(texto="CHAMANDO O MERO")
                        comando = f'{mero_executavel} gevt -i {path_completo_destino} --params {_path_params}'
                        if Terminal().run(comando, erro_customizado="Unlicensed product.") is False:
                            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executar comando [{comando}].')
                            solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "GEVT"
                            continue

                    except Exception as ex:
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executar GEVT.', info_ex=str(ex))
                        solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "GEVT"
                        continue

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, [solucoes], True)
        return self._contexto

    def _escreve_params(self, solucao: Solucao, _path_params, prefixo):
        try:
            unievet_file_name = f'{self._qualificador}_{solucao.iteracao}_{solucao.id}_{prefixo}.unievent'
            cont = 'name_unievent {}\n'.format(unievet_file_name)

            if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_DATA_FINAL):
                cont += f'{EnumValues.DATA_FINAL.name} {self._contexto.get_atributo(EnumAtributo.REDUCAO_GEVT_DATA_FINAL)}\n'

            if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_DIA_FINAL):
                cont += f'{EnumValues.DIA_FINAL.name} {self._contexto.get_atributo(EnumAtributo.REDUCAO_GEVT_DIA_FINAL)}\n'

            # cont += f'***{EnumTipoVariaveis.VARIAVEL.name}***\n'
            # for key, variavel in solucao.get_variavies_by_tipo().items():
            #     cont += '{} {}\n'.format(key, variavel.valor)
            #
            # cont += f'***{EnumTipoVariaveis.CONSTANTE.name}***\n'
            # for key, variavel in solucao.get_variavies_by_tipo(EnumTipoVariaveis.CONSTANTE).items():
            #     cont += '{} {}\n'.format(key, variavel.valor)
            cont += f'***VARIAVEIS***\n'
            for nome, valor in solucao.get_variaveis_nome_valor().items():
                cont += '{} {}\n'.format(nome, valor)

            if TXT().salvar(_path_params, cont):
                return True

        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao escrever arquivo de dominio.', info_ex=str(ex))
            return False
        return False

    def _resecreve_time_list(self, gevt_path):
        if self._contexto.tem_atributo(EnumAtributo.REDUCAO_GEVT_TIME_LIST):
            linhas_gevt = TXT().ler(gevt_path)
            for i in range(len(linhas_gevt)-1, 0, -1):
                if (linhas_gevt[i] != '') and (not '**' in linhas_gevt[i][0:2]):
                    if not linhas_gevt[i].strip()[-9:] in EnumValues.TIME_LIST.name:
                        self.log(tipo=EnumLogStatus.WARN, texto='Ultima linha não contem TIME LIST')
                        return False
                    else:
                        conteudo = "\n"
                        conteudo += '\n'.join([str(x) for x in self._contexto.get_atributo(EnumAtributo.REDUCAO_GEVT_TIME_LIST)])
                        self.log(texto=f'Reescrevendo arquivo {gevt_path}')
                        return TXT().salvar(gevt_path, metodo_gravacao='a+', conteudo=conteudo)
        return True
