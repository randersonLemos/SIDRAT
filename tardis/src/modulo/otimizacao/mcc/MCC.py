"""
:author: Rafael
:data: 16/01/2020
"""
import copy
import random

from src.contexto.Contexto import EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.inout.Exportacao import Exportacao
from src.inout.LogarMemoria import LogarMemoria
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.otimizacao.OtimizadorPadrao import OtimizadorPadrao
from src.problema.Solucao import Solucao
from src.problema.Variavel import Variavel


class MCC(OtimizadorPadrao):
    """
    Implementação do algoritmo de otimização MCC - metodo das coordenadas ciclicas
    """

    def __init__(self):
        super(MCC, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.OTIMIZACAO_MCC_VARIAVEIS_ITERACAO] + super(MCC, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._variaveis_por_iteracao = 0
        self._nome_variaveis_ordem = []
        self._nome_variaveis = []
        self._solucoes_usadas = {}
        self._solucao_melhor = None

    def inicializacao(self):
        super(MCC, self).inicializacao()

        self._solucao_melhor = self._solucoes.melhor_solucao(nome_of_mono=self._nome_of_mono)

        if self._contexto.tem_atributo(EnumAtributo.OTIMIZACAO_MCC_SOLUCOES_USADAS):
            self._solucoes_usadas = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_MCC_SOLUCOES_USADAS)

        self._variaveis_por_iteracao = self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_MCC_VARIAVEIS_ITERACAO)

        for nome in self._solucao_melhor.get_variavies_by_tipo():
            self._nome_variaveis.append(nome)

    def run(self):
        """
        Executa a otimizacao usando o método MCC.
        """
        super(MCC, self).run()

        avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
        criterio = self._contexto.get_modulo(EnumModulo.CRITERIOPARADA)

        while not criterio.run(self._contexto):
            self.log(texto=f"Nova iteracao do método")
            self._iteracao += 1

            if self._proximo_conjuto():
                self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [self._iteracao], True)

                self._contexto = avaliacao.run(self._contexto)

                self._selecionar_melhor()

                self._para_resume()
                Exportacao().csv(self._contexto)
                Exportacao().obejto(self._contexto)
                LogarMemoria(self._contexto)
            else:
                self.log(texto=f'Fim da execução do {self._name}')
                return
        self.log(texto=f'Fim da execução do {self._name}')

    def _proximo_conjuto(self) -> bool:
        variaveis_avaliadas = 1
        self.log(texto=f'Buscar solucoes para iteracao {self._iteracao}.')
        variaveis = copy.deepcopy(self._solucao_melhor.variaveis)
        qtd_variaveis = len(variaveis.get_variaveis_by_tipo())
        if qtd_variaveis == 0:
            self.log(texto=f'Não existe variaveis.', tipo=EnumLogStatus.ERRO)
            return False

        qtd_tentiva_achar_variavel = 0
        qtd_variaveis_descartadas = 0

        while self._variaveis_por_iteracao >= variaveis_avaliadas:
            qtd_tentiva_achar_variavel += 1

            while len(self._nome_variaveis_ordem) < self._variaveis_por_iteracao:
                lista_variaveis = copy.deepcopy(self._nome_variaveis)

                if self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_MCC_ORDEM_VARIAVEL_ALEATORIA):
                    random.shuffle(lista_variaveis)

                self._nome_variaveis_ordem = list(self._nome_variaveis_ordem) + list(lista_variaveis)

            variavel_nome = self._nome_variaveis_ordem[0]
            #definindo o passo sempre ocmo 1 ou -1 pr dentro do metodo ele percorrer os passos.
            solucao_mais_um:  Solucao = self._evoluindo_variavel(+1, variaveis.get_variavel_by_nome(variavel_nome))
            solucao_menos_um: Solucao = self._evoluindo_variavel(-1, variaveis.get_variavel_by_nome(variavel_nome))

            if (solucao_mais_um is not None) or (solucao_menos_um is not None):
                self._solucoes.add_in_solucoes(solucao_mais_um)
                self._solucoes.add_in_solucoes(solucao_menos_um)
                variaveis_avaliadas += 1
                qtd_tentiva_achar_variavel = 0
            else:
                qtd_variaveis_descartadas += 1

            del self._nome_variaveis_ordem[0]

            if qtd_tentiva_achar_variavel > qtd_variaveis:
                if variaveis_avaliadas > 0:
                    return True
                else:
                    self.log(texto=f'Convergiu, em um caminho tentando encontrar outro.')
                    self._selecionar_melhor()

                    self.log(texto=f'Voltando para outro ponto de inicio, nova estratégia de inicio {self._solucao_melhor.to_string()}')
                    variaveis = copy.deepcopy(self._solucao_melhor.variaveis)
                    qtd_variaveis = len(variaveis.get_variaveis_by_tipo())
                    qtd_tentiva_achar_variavel = 0
                    qtd_variaveis_descartadas = 0

        del variaveis
        variaveis = None
        return True

    def _evoluindo_variavel(self, passo: int, variavel_in: Variavel) -> Solucao:
        solucao_aux = None
        variavel = None
        while True:
            variavel = copy.deepcopy(variavel_in)

            if abs(passo) > len(variavel.dominio.niveis):
                solucao_aux = None
                self.log(texto=f'Não existe niveis para mais um na variavel [{variavel.nome}], com posicao [{abs(passo)}].')
                break
            elif variavel.posicao + passo < 0:
                solucao_aux = None
                self.log(texto=f'Não existe niveis para mais um na variavel [{variavel.nome}], com posicao [{variavel.posicao + passo}].')
                break
            elif variavel.posicao + passo >= len(variavel.dominio.niveis):
                solucao_aux = None
                self.log(texto=f'Não existe niveis para mais um na variavel [{variavel.nome}], com posicao [{variavel.posicao + passo}].')
                break

            valor_antigo = variavel.valor
            try:
                variavel.posicao += passo
            except ValueError as ex:
                self.log(texto="Valor for do limite", info_ex=str(ex))
                return None

            #self.log(texto=f'Passo igual [{passo}] para evolução da variavel [{variavel.nome}], valor antigo [{valor_antigo}], valor novo [{variavel.valor}]')
            solucao_aux = Solucao(iteracao=self._iteracao, id=self._id + 1, solucao=self._solucao_melhor)
            solucao_aux.variaveis.set_variavel_posicao_by_nome(variavel.nome, variavel.posicao)
            solucao_aux.geral += f'[MCC][{variavel.nome}|{valor_antigo}>{variavel.valor}]'

            if self._solucoes.existe_solucao(solucao_aux):
                passo += int(passo / abs(passo))
                #self.log(texto=f'Já existe solucao com esses valores nas variaveis. Passo será [{passo}].')
            else:
                self._id += 1
                break

        del variavel
        variavel = None
        return solucao_aux

    def _selecionar_melhor(self):
        """
        Obtem a melhor solucao, de modo geral e se precisar de um novo caminho
        :param solucoes: Lista de todas as estratégias
        :type solucoes: Solucao
        :param nova: Informa se quer uma solucao para um novo caminho
        :type nova: bool
        :return:
        :rtype:
        """
        solucoes_aux = self._contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes
        #melhor_aux = self._solucao_base
        melhor_aux = None
        melhor_aux_of = float('-inf')
        quantidade_de_vezes_usar_solucao_com_melhor = 1
        for k_iteracao in solucoes_aux:
            for k_id in solucoes_aux[k_iteracao]:
                if Solucao.validar_of(solucoes_aux[k_iteracao][k_id].of[self._nome_of_mono].valor):
                    direcao_of_valor = 1
                    if self._nomes_direcoes_of[self._nome_of_mono][EnumValues.DIRECAO.name] in EnumValues.MIN.name:
                        direcao_of_valor = -1
                    #if (direcao_of_valor * solucoes_aux[k_iteracao][k_id].of[self._nome_of_mono].valor) > (direcao_of_valor * melhor_aux.of[self._nome_of_mono].valor):
                    if (direcao_of_valor * solucoes_aux[k_iteracao][k_id].of[self._nome_of_mono].valor) > (direcao_of_valor * melhor_aux_of):
                        eh_nova = True
                        if k_iteracao in self._solucoes_usadas:
                            if k_id in self._solucoes_usadas[k_iteracao]:
                                if self._solucoes_usadas[k_iteracao][k_id] > quantidade_de_vezes_usar_solucao_com_melhor:
                                    eh_nova = False
                        if eh_nova:
                            melhor_aux = solucoes_aux[k_iteracao][k_id]
                            melhor_aux_of = solucoes_aux[k_iteracao][k_id].of[self._nome_of_mono].valor

        if melhor_aux is None:
            melhor_aux = self._solucao_base

        self._solucao_melhor = melhor_aux
        if '[Melhor]' not in self._solucao_melhor.geral:
            self._solucao_melhor.geral += '[Melhor]'
        if melhor_aux.iteracao in self._solucoes_usadas:
            if melhor_aux.id in self._solucoes_usadas[melhor_aux.iteracao]:
                self._solucoes_usadas[melhor_aux.iteracao][melhor_aux.id] += 1
            else:
                self._solucoes_usadas[melhor_aux.iteracao][melhor_aux.id] = 1
        else:
            self._solucoes_usadas[melhor_aux.iteracao] = {melhor_aux.id: 1}

        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_MCC_SOLUCOES_USADAS, self._solucoes_usadas, True)

    def _para_resume(self):
        self.log(texto="Salvando atributos para resume.")
        self._contexto.set_atributo(EnumAtributo.OTIMIZACAO_MCC_SOLUCOES_USADAS, self._solucoes_usadas, True)

