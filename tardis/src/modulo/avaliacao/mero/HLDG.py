"""
:author: Luis
:data: 21/01/2020
"""

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Terminal import Terminal
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Solucao import Solucao


class HLDG(Loggin):
    """
    Classe para construção do arquivo HLDG.mero e sua execucao
    """

    def __init__(self):

        super().__init__()

        self._name = __name__

        self._contexto = None

        self._solucao_pdf_atualizada = None

        self._solucoes = None

        self._iteracao_nova_amostragem = 1

        self._path_hldg = ''

        self._n_amostragem = None

        self._ultimo_id = 0

    def run(self, contexto: Contexto, solucao_pdf_atualizada: Solucao, n_amostragem):
        """
        Executa a amostragem com o IDLHCn

        :param Contexto contexto: contexto com todas as informações necessárias
        :param Solucao solucao_pdf_atualizada: Solucao com pdf atualizada para utilizacao na amostragem
        """

        self._n_amostragem = n_amostragem

        self._contexto = contexto
        self._solucao_pdf_atualizada = solucao_pdf_atualizada

        path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)

        self._solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        ultima_iteracao = max(map(int, self._solucoes.solucoes))
        self._ultimo_id = max(map(int, self._solucoes.solucoes[ultima_iteracao]))

        self._iteracao_nova_amostragem = ultima_iteracao + 1

        self._path_hldg = InOut.ajuste_path('\\'.join([path_projeto, self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO), f'HLDG_{self._iteracao_nova_amostragem}.mero']))
        self._gera_entrada_hldg()
        self._execucao_hldg()
        self._criar_solucoes_em_contexto()

        return self._contexto

    def _gera_conteudo_hldg(self):
        return "\n".join([self._gera_cabecalho(), self._gera_conteudo_variavel_peso(), self._gera_qtd_amostras()])

    def _gera_cabecalho(self):
        return '\n'.join(['*MODEL_NAMING {}_', '*ATTRIBUTE_LIST']).format(self._iteracao_nova_amostragem)

    def _gera_conteudo_variavel_peso(self):

        conteudo = ""

        solucao = self._solucao_pdf_atualizada
        nome_variaveis = solucao.variaveis.get_variaveis_by_tipo(EnumTipoVariaveis.VARIAVEL)

        for nome_variavel in nome_variaveis:
            probabilidade = solucao.variaveis.get_variavel_by_nome(nome_variavel).dominio.probabilidade
            niveis = solucao.variaveis.get_variavel_by_nome(nome_variavel).dominio.niveis

            tipo_str = self._checa_tipo_variavel(niveis)

            conteudo += f'{nome_variavel}\t{tipo_str}'
            for dom, prob in zip(niveis, probabilidade):
                conteudo += f'\t{dom}\t({prob})'
            conteudo += '\n'

        return conteudo

    def _gera_qtd_amostras(self):
        return f'*SAMPLE_COUNT\t{str(self._n_amostragem)}'

    def _checa_tipo_variavel(self, niveis):
        tipo_str = "CAT"

        for dom in niveis:
            if type(dom) is str:
                return tipo_str
            elif type(dom) is float:
                tipo_str = 'REAL'
            elif (type(dom) is int) and tipo_str is not 'REAL':
                tipo_str = 'INT'

        return tipo_str

    def _gera_entrada_hldg(self):
        conteudo = self._gera_conteudo_hldg()

        if TXT().salvar(self._path_hldg, conteudo):
            self.log(texto='Arquivo de entrada do HLDG gerado com sucesso')
        else:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro na geracao do arquivo do HLDG')

    def _execucao_hldg(self):
        executavel = InOut().ajuste_path(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_EXECUTAVEL))
        comando = f'{executavel} hldg -i {self._path_hldg}'

        if Terminal().run(comando):
            self.log(texto='execucao HLDG feita com sucesso')
        else:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro execucao HLDG')

    def _carregar_saida_HLDG(self):
        path_out_hldg = self._path_hldg.replace('.mero', '-models.txt')
        conteudo_sorteio_txt = TXT().ler(path_out_hldg)
        return conteudo_sorteio_txt

    def _criar_solucoes_em_contexto(self):
        conteudo_sorteio_txt = self._carregar_saida_HLDG()

        nomes_variaveis = conteudo_sorteio_txt[0].split('\t')[1:-1]

        lista_serializado = self._solucoes.serializacao()

        for solucao_txt in conteudo_sorteio_txt[1:]:
            nome_solucao_val_vars = solucao_txt.split('\t')
            [iteracao_solucao, id_solucao] = nome_solucao_val_vars[0].split('_')

            solucao = Solucao(id=int(id_solucao)+self._ultimo_id, iteracao=int(iteracao_solucao), solucao=self._solucao_pdf_atualizada)

            val_vars = [InOut().ajusta_entrada(val_var) for val_var in nome_solucao_val_vars[1:-1]]
            for variavel, valor in zip(nomes_variaveis, val_vars):
                solucao.variaveis.get_variavel_by_nome(variavel).valor = valor

            if solucao.variaveis.serializacao() not in lista_serializado:
                self._solucoes.add_in_solucoes(solucao)

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, self._solucoes, True)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [int(iteracao_solucao)], True)
