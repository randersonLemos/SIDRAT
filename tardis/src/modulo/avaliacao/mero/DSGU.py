"""
:author: Rafael
:data: 03/01/2020
"""
import os
import threading
import time

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Terminal import Terminal
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.problema.Solucoes import Solucoes


def thread_function(name):
    print(f"Thread {name}: starting")
    time.sleep(20)
    print(f"Thread {name}: finishing")


class DSGU(Loggin):
    """
    Classe que executa a DSGU
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
        self._gevts_templates = None
        self._thread = None

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
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)
        self._solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)

        mero_executavel = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_EXECUTAVEL)

        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        iteracoes_str = ""
        for ss in iteracoes:
            iteracoes_str = f'{iteracoes_str}_{ss}'

        prefixo = f'{self._qualificador}{iteracoes_str}'

        path_projeto = InOut.ajuste_path(str(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)))
        path_simulacao = InOut.ajuste_path(str(self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)))
        path_dsgu = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{prefixo}_dsgu.mero')

        if not self._escrever(iteracoes, path_dsgu):
            self._contexto.set_atributo(EnumAtributo.SOLUCOES, [self._solucoes], True)
            return self._contexto

        try:
            params = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_DS_PARAMS)
            comando = f'{mero_executavel} dsgu -i {path_dsgu} {params}'
            self.log(texto=f'Executando comando {comando}.')
            self.log(texto=f'Abrindo as threads, aguarde ...')
            terminal = Terminal()
            self._thread = threading.Thread(target=terminal.run, args=(comando, ))
            self._thread.start()
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro executar o comando {comando}', info_ex=str(ex))
            list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
            for k_iteracao, v_est in list_solucoes.items():
                for k_id, vv_est in v_est.items():
                    vv_est.has_erro = 'DSGU'
                    self._solucoes.add_in_solucoes(vv_est, True)
            self._thread.join()
            self._thread = None

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, [self._solucoes], True)
        return self._contexto

    def _escrever(self, iteracoes, path_dsgu):

        try:
            path_projeto = InOut.ajuste_path(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO))
            path_simulacao = InOut.ajuste_path(self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO))

            cont = f'*SIMULATOR {self._contexto.get_atributo(EnumAtributo.SIMULADOR_NOME)} {self._contexto.get_atributo(EnumAtributo.SIMULADOR_VERSAO)}\n' \
                '*MODEL_LIST\n' \
                'ID\n'

            ids = ""

            list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
            for gevt_template in self._gevts_templates:
                for k_iteracao, v_est in list_solucoes.items():
                    for k_id, vv_est in v_est.items():
                        id = f'{self._qualificador}_{vv_est.iteracao}_{vv_est.id}_{gevt_template}'
                        path_file_id = InOut.ajuste_path(f'{path_projeto}/{path_simulacao}/{id}')

                        if os.path.isfile(f'{path_file_id}.dat'):
                            ids += f'{id}\n'
                            try:
                                if os.path.isfile(f'{path_file_id}.out'):
                                    os.remove(f'{path_file_id}.out')
                                if os.path.isfile(f'{path_file_id}.mrf'):
                                    os.remove(f'{path_file_id}.mrf')
                                if os.path.isfile(f'{path_file_id}.irf'):
                                    os.remove(f'{path_file_id}.irf')
                                if os.path.isfile(f'{path_file_id}.rstr.irf'):
                                    os.remove(f'{path_file_id}.rstr.irf')
                                if os.path.isfile(f'{path_file_id}.rstr.mrf'):
                                    os.remove(f'{path_file_id}.rstr.mrf')
                                if os.path.isfile(f'{path_file_id}.rstr.sr3'):
                                    os.remove(f'{path_file_id}.rstr.sr3')
                                if os.path.isfile(f'{path_file_id}.sr3'):
                                    os.remove(f'{path_file_id}.sr3')
                                if os.path.isfile(f'{path_file_id}.log'):
                                    os.remove(f'{path_file_id}.log')
                                if os.path.isfile(f'{path_file_id}.unipro'):
                                    os.remove(f'{path_file_id}.unipro')
                            except Exception as ex:
                                self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao remover arquivos.', info_ex=str(ex))
                        else:
                            self.log(tipo=EnumLogStatus.WARN, texto=f'O arquivo {path_file_id} não existe.')
                            vv_est.has_erro = 'DSGU'
                            self._solucoes.add_in_solucoes(vv_est, True)

            if ids == "":
                self.log(tipo=EnumLogStatus.ERRO, texto='Não há estudo para simular.')
                return False

            cont += ids
            if not TXT().salvar(path_arquivo=path_dsgu, conteudo=cont):
                self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever aquivo {path_dsgu}.')
                for k_iteracao, v_est in list_solucoes.items():
                    for k_id, vv_est in v_est.items():
                        vv_est.has_erro = 'DSGU'
                        self._solucoes.add_in_solucoes(vv_est, True)
                return False

        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro para escrever arquivo dsgu.mero', info_ex=str(ex))
            list_solucoes = self._solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
            for k_iteracao, v_est in list_solucoes.items():
                for k_id, vv_est in v_est.items():
                    vv_est.has_erro = 'DSGU'
                    self._solucoes.add_in_solucoes(vv_est, True)
            return False

        return True

    def finalizar_thread(self):
        try:
            if self._thread is not None:
                self._thread.join()
        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao finalizar thread')
        finally:
            self._thread = None
