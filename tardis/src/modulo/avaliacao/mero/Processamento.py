"""
:author: Rafael
:data: 07/01/2020
"""
import os
import time
from copy import deepcopy

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.problema.Solucoes import Solucoes
from src.modulo.avaliacao.mero.CalculaOfEconomico import CalculaOfEconomico
from src.modulo.avaliacao.mero.CalculaOfProducao import CalculaOfProducao


class Processamento(Loggin):
    """
    Classe que executa a Calcula_OF
    """

    def __init__(self):
        """
        Classe para construção do arquivo gevt.mero
        """
        super().__init__()

        self._name = __name__
        self._contexto = None
        self._qualificador = None
        self._solucoes = None
        self._path_projeto = None
        self._path_simulacao = None
        self._gevts_templates = None
        self._uniecos = None
        self._buffer = {'simular': {}, 'simulando': {}, 'simulado': {}, 'erro': {}, 'unipro': {}, 'finalizado': {}}

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
        self._uniecos = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR)
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)
        self._solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        self._path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        self._path_simulacao = self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)

        if not self._existe_solucoes():
            return self._contexto

        self._check_simular()
        while True:
            time.sleep(3)
            self._check_simulando()
            self._check_simulado()
            self._check_unipro()
            self._pos_processamento()

            soma = len(self._buffer['simular']) + len(self._buffer['simulando']) + len(self._buffer['simulado']) + len(self._buffer['unipro'])
            if soma <= 0:
                break

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, [self._solucoes], True)
        return self._contexto

    def _existe_solucoes(self):
        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
        if len(list_solucoes) <= 0:
            self.log(tipo=EnumLogStatus.INFO, texto=f'Não há estudo sem erro para avaliar')
            return False
        return True

    def _check_simular(self):
        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        iteracoes_str = ""
        for ss in iteracoes:
            iteracoes_str = f'{iteracoes_str}_{ss}'

        self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)

        prefix_simular = {}
        for gevt_templante in self._gevts_templates:
            for k_iteracao, v_est in list_solucoes.items():
                for k_id, vv_est in v_est.items():
                    prefixo = f'{self._qualificador}_{vv_est.iteracao}_{vv_est.id}_{gevt_templante}'
                    prefix_simular[prefixo] = {'iteracao': vv_est.iteracao,
                                               'id': vv_est.id,
                                               'time': time.time(),
                                               'path': f'{self._path_projeto}/{self._path_simulacao}/{prefixo}'}
        self._buffer['simular'] = prefix_simular

    def _check_simulando(self):

        simular = self._buffer['simular']
        keys = deepcopy(list(simular.keys()))
        for ii in range(len(keys)):
            prefixo = keys[ii]
            iteracao = simular[prefixo]["iteracao"]
            id = simular[prefixo]["id"]
            path = simular[prefixo]["path"]
            file = InOut.ajuste_path(f'{path}.out')
            if os.path.isfile(file):
                self.log(texto=f'Solucao ({prefixo}) iteracao [{iteracao}] e id [{id}] simulando.')
                self._buffer['simulando'][prefixo] = simular[prefixo]
                del self._buffer['simular'][prefixo]
            else:
                horas_sim_max = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_TEMPO_MAX_SIM)
                if simular[prefixo]["time"] + horas_sim_max * 60 * 60 < time.time():
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'A simulação da solucao  {prefixo}) iteracao [{iteracao}] e id [{id}] excedeu tempo de {horas_sim_max} hora.')
                    self._buffer['erro'][prefixo] = simular[prefixo]
                    self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f"Excedeu {horas_sim_max}h"
                    del self._buffer['simular'][prefixo]

    def _check_simulado(self):
        simulando = self._buffer['simulando']
        keys = deepcopy(list(simulando.keys()))
        for ii in range(len(keys)):
            prefixo = keys[ii]
            iteracao = simulando[prefixo]['iteracao']
            id = simulando[prefixo]['id']
            path = simulando[prefixo]['path']
            file = InOut.ajuste_path(f'{path}.out')

            if os.path.isfile(file):
                with open(file, 'r') as out_file:
                    file_read = out_file.read()
                    if 'Normal Termination' in file_read:
                        self.log(texto=f'Solucao ({prefixo}) iteracao [{iteracao}] e id [{id}] foi simulada com sucesso, será calculado o unipro. ')
                        self._buffer['simulado'][prefixo] = simulando[prefixo]
                        del self._buffer['simulando'][prefixo]
                        continue

                    if 'End of Simulation:' in file_read:
                        time.sleep(1)
                        with open(file, 'r') as out_file2:
                            file_read_2 = out_file2.read()
                            if 'Normal Termination' in file_read_2:
                                self.log(texto=f'Solucao ({prefixo}) iteracao [{iteracao}] e id [{id}] foi simulada com sucesso, será calculado o unipro. ')
                                self._buffer['simulado'][prefixo] = simulando[prefixo]
                                del self._buffer['simulando'][prefixo]
                                continue
                            else:
                                self.log(texto=f'Erro ao simular solucao ({prefixo}) iteracao [{iteracao}] e id [{id}]',tipo=EnumLogStatus.ERRO)
                                self._buffer['erro'][prefixo] = simulando[prefixo]
                                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Calcula_OF"
                                del self._buffer['simulando'][prefixo]
                                continue

                    horas_sim_max = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_TEMPO_MAX_SIM)
                    if simulando[prefixo]["time"] + horas_sim_max * 60 * 60 < time.time():
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'A simulação da solucao  {prefixo}) iteracao [{iteracao}] e id [{id}] excedeu tempo de {horas_sim_max} hora.')
                        self._buffer['erro'][prefixo] = simulando[prefixo]
                        self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f"Excedeu {horas_sim_max}h"
                        del self._buffer['simulando'][prefixo]

            else:
                self.log(texto=f'Erro ao simular solucao  {prefixo}) iteracao [{iteracao}] e id [{id}]', tipo=EnumLogStatus.ERRO)
                self._buffer['erro'][prefixo] = simulando[prefixo]
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Calcula_OF"
                del self._buffer['simulando'][prefixo]
        return

    def _check_unipro(self):
        simulado = self._buffer['simulado']
        keys = deepcopy(list(simulado.keys()))
        for ii in range(len(keys)):
            prefixo = keys[ii]
            iteracao = simulado[prefixo]['iteracao']
            id = simulado[prefixo]['id']
            path = simulado[prefixo]['path']
            path_file = InOut.ajuste_path(f'{path}.unipro')

            if os.path.isfile(path_file):
                # se arquivo unipro esta escrito
                tamanho_unipro = 0
                try:
                    tamanho_unipro = os.path.getsize(path_file)
                except Exception as ex:
                    pass

                if tamanho_unipro > 300:
                    self._buffer['unipro'][prefixo] = simulado[prefixo]
                    del self._buffer['simulado'][prefixo]
                    self.log(texto=f'Solucao ({prefixo}) iteracao [{iteracao}] e id [{id}] foi calculado o unipro, com sucesso. ')
                    continue

            horas_sim_max = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_TEMPO_MAX_SIM)
            if simulado[prefixo]["time"] + horas_sim_max * 60 * 60 < time.time():
                self.log(tipo=EnumLogStatus.ERRO, texto=f'A simulação da solucao  {prefixo}) iteracao [{iteracao}] e id [{id}] excedeu tempo de {horas_sim_max} hora.')
                self._buffer['erro'][prefixo] = simulado[prefixo]
                self._solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f"Excedeu {horas_sim_max}h"
                del self._buffer['simulado'][prefixo]

    def _pos_processamento(self):

        self._solucoes = CalculaOfProducao(self._contexto).run(buffer=self._buffer, solucoes=self._solucoes)

        self._solucoes = CalculaOfEconomico(self._contexto).run(buffer=self._buffer, solucoes=self._solucoes)

        keys = deepcopy(list(self._buffer['unipro']))
        for ii in range(len(keys)):
            prefixo = keys[ii]
            del self._buffer['unipro'][prefixo]
