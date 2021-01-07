"""
:author: Rafael
:data: 15/10/2020
"""
import os
from copy import deepcopy

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.CSV import CSV
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.inout.Terminal import Terminal
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.problema.Solucao import Of, Solucao


class CalculaOfEconomico(Loggin):
    """
    Classe destinada a ler os resultados
    """

    def __init__(self, contexto):
        """
        Comentário do construtor
        """
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._contexto = contexto
        self._path_projeto = self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)
        self._uniecos = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR)
        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)
        self._path_simulacao = self._contexto.get_atributo(EnumAtributo.PATH_SIMULACAO)
        self._gevts_templates = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR)
        self._nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)

    def run(self, buffer, solucoes):
        """
        """

        if EnumValues.VPL.name in self._nomes_direcoes_of:
            solucoes = self._executar_fop(buffer, solucoes)

        if EnumValues.VME.name in self._nomes_direcoes_of:
            solucoes = self._executar_vme(buffer, solucoes)

        return solucoes

    def _ler_dados_economicos(self, solucoes, path, ler_resultados, nome_of):
        keys = deepcopy(list(ler_resultados.keys()))
        direcao_of = self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name]
        if len(keys) == 0:
            return solucoes

        self.log(texto=f'Ler dados economicos de {path}')
        try:
            df_lido_correto = True
            df = CSV().ler(f'{path}', lines_ignore=3, sep=";", index_col=False)
            if df is None or df.shape[1] <= 1:
                df = CSV().ler(f'{path}', lines_ignore=3, sep=",", index_col=False)
                if df is None or df.shape[1] <= 1:
                    df_lido_correto = False

            if df_lido_correto:
                df.sort_values(by='MODEL', inplace=True)
                df.index = df.MODEL

                for ii in range(len(keys)):
                    prefixo = keys[ii]
                    iteracao = ler_resultados[prefixo]['iteracao']
                    id = ler_resultados[prefixo]['id']
                    df_aux = {'dataframe': df[df.index == prefixo]}
                    if len(df_aux) > 0:
                        try:
                            valor_of = Solucao.of_padrao(direcao_of)
                            if nome_of == EnumValues.VPL.name:
                                if 'OF' in list(df_aux['dataframe'].columns):
                                    df_npvf = df_aux['dataframe'][df_aux['dataframe'].OF == 'NPVF']
                                    valor_of = df_npvf.VALUE.iloc[0]
                            if nome_of == EnumValues.VME.name:
                                if 'EMV' in list(df_aux['dataframe'].columns):
                                    valor_of = df_aux["dataframe"].EMV.iloc[0]

                            self.log(texto=f'Solucao iteracao [{iteracao}], e id [{id}] tem OF no valor de [{valor_of}]')
                            solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = valor_of
                            solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).set_avaliada()
                        except Exception as ex:
                            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao ler dados economicos da solucao iteracao [{iteracao}], e id [{id}]', info_ex=str(ex))
                            solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'LER_CVS_{nome_of}'
                            solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = Solucao.of_padrao(direcao_of)
                    else:
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao ler dados economicos da solucao iteracao [{iteracao}], e id [{id}]')
                        solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'LER_CVS_{nome_of}'
                        solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = Solucao.of_padrao(direcao_of)
            else:
                for ii in range(len(keys)):
                    prefixo = keys[ii]
                    iteracao = ler_resultados[prefixo]['iteracao']
                    id = ler_resultados[prefixo]['id']
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao abrir dados economicos da solucao iteracao [{iteracao}], e id [{id}]')
                    solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'ABRIR_CVS_{nome_of}'
                    solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = Solucao.of_padrao(direcao_of)
        except Exception as ex:
            for ii in range(len(keys)):
                prefixo = keys[ii]
                iteracao = ler_resultados[prefixo]['iteracao']
                id = ler_resultados[prefixo]['id']
                self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao obter dados economicos da solucao iteracao [{iteracao}], e id [{id}]', info_ex=str(ex))
                solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = f'OBTER_{nome_of}'
                solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).of[nome_of].valor = Solucao.of_padrao(direcao_of)
        return solucoes

    def _executar_fop(self, buffer, solucoes):
        unipro = buffer['unipro']
        if len(unipro) == 0:
            return solucoes

        unieco_path = InOut.ajuste_path(f"{self._path_projeto}/{self._uniecos[list(self._uniecos.keys())[0]]['unieco_path']}")
        unieco_file = ((unieco_path.split(InOut.barra())[-1]).split("#")[0]).split(".")[0]
        cont = f'*PROJECT aux\n' \
               f'*SIMULATOR {self._contexto.get_atributo(EnumAtributo.SIMULADOR_NOME)} {self._contexto.get_atributo(EnumAtributo.SIMULADOR_VERSAO)}\n' \
               f'*UNIECO {unieco_path}\n' \
               f'*ECO_REFERENCE_DATE {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE)}\n' \
               f'*MODEL_LIST\n' \
               f'ID\n'

        iteracaoes = {}
        ids = {}
        for prefixo in unipro.keys():
            cont += f'{prefixo}\n'
            iteracaoes[unipro[prefixo]['iteracao']] = True
            ids[unipro[prefixo]['iteracao']] = True

        iteracaoes_str = ""
        ids_str = ""
        for iteracao in iteracaoes.keys():
            iteracaoes_str = f'{iteracaoes_str}_{iteracao}'
        for id in ids.keys():
            ids_str = f'{ids_str}_{id}'

        cont += self._adiciona_discretizacao_plat()

        path = InOut.ajuste_path(f'{self._path_projeto}/{self._path_simulacao}/{self._qualificador}_it{iteracaoes_str}_id{ids_str}_fop')
        if not TXT().salvar(path_arquivo=f'{path}.mero', conteudo=cont):
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever aquivo {path}.')
            keys = deepcopy(list(unipro.keys()))
            for ii in range(len(keys)):
                prefixo = keys[ii]
                iteracao = unipro[prefixo]['iteracao']
                id = unipro[prefixo]['id']
                self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever fop.mero para a solucao  {prefixo}) iteracao [{iteracao}] e id [{id}].')
                solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Escrever_FOP.Mero"
            return solucoes
        else:
            ler_resultados = {}
            mero_executavel = InOut.ajuste_path(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_EXECUTAVEL))

            thread_argument = ''
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_FOP_MULTI_THREAD):
                if self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_FOP_MULTI_THREAD):
                    thread_argument = ' --multi-thread'

            comando = f'{mero_executavel} fop -i {path}.mero -t Local -s Local -p 1 -n 1 -q LocalQueue -f XML --no-wait -r{thread_argument}'
            self.log(texto=f'Executando comando [{comando}]')
            self.log(texto=f'Aguarde ...')

            retorno_terminal = Terminal().run(comando)

            path_fop_eof = f"{path}.eof.csv"
            if not os.path.isfile(path_fop_eof):
                path_fop_eof = f"{path}_{unieco_file}.eof.csv"

            if (retorno_terminal is False) or (not os.path.isfile(path_fop_eof)):
                keys = deepcopy(list(unipro.keys()))
                for ii in range(len(keys)):
                    prefixo = keys[ii]
                    iteracao = unipro[prefixo]['iteracao']
                    id = unipro[prefixo]['id']
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executar FOP para a solucao  {prefixo}) iteracao [{iteracao}] e id [{id}].')
                    solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Executando_FOP"
                return solucoes

            keys = deepcopy(list(unipro.keys()))
            for ii in range(len(keys)):
                prefixo = keys[ii]
                iteracao = unipro[prefixo]['iteracao']
                id = unipro[prefixo]['id']
                self.log(texto=f'Fop da solucao [{prefixo}] iteracao [{iteracao}] e id [{id}] foi calculada com sucesso.')
                ler_resultados[prefixo] = unipro[prefixo]

            solucoes = self._ler_dados_economicos(solucoes, path_fop_eof, ler_resultados, EnumValues.VPL.name)

        return solucoes

    def _adiciona_discretizacao_plat(self):
        """
        Metodo utilizado para utilizacao da discretizacao da plataforma
        :return:
        """
        cont = ''
        if any([self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_GAS_PRO),
                self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_LIQUID_PRO),
                self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_PRO),
                self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_INJ)]):

            cont += '\n*PLATFORM_CONSTRAINT_DISCRETIZATION_LIST\n'

            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_OIL_PRO):
                cont += f'\n{EnumValues.MAX_OIL_PRO.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_MAX_OIL_PRO)}'
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_PRO):
                cont += f'\n{EnumValues.MAX_WATER_PRO.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_PRO)}'
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_GAS_PRO):
                cont += f'\n{EnumValues.MAX_GAS_PRO.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_MAX_GAS_PRO)}'
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_LIQUID_PRO):
                cont += f'\n{EnumValues.MAX_LIQUID_PRO.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_MAX_LIQUID_PRO)}'
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_INJ):
                cont += f'\n{EnumValues.MAX_WATER_INJ.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_MAX_WATER_INJ)}'
            if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_TOLERANCE):
                cont += f'\n{EnumValues.MAX_OIL_PRO.name} {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_TOLERANCE)}'

        return cont

    def _executar_vme(self, buffer, solucoes):
        unipros = buffer['unipro']
        if len(unipros) == 0:
            return solucoes

        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        list_solucoes = solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)

        for iteracao in list_solucoes.keys():
            for id in list_solucoes[iteracao].keys():
                vme_rodou = []
                pode_vme = True
                model_list = "*MODEL_LIST\nID\n"
                for gevt_template in self._gevts_templates:
                    prefixo = f'{self._qualificador}_{iteracao}_{id}_{gevt_template}'
                    model_list += f'{prefixo} {prefixo}.unievent ({self._gevts_templates[gevt_template]["template_prob"]})\n'
                    if not prefixo in unipros:
                        pode_vme = False
                    vme_rodou.append(prefixo)

                if not pode_vme:
                    continue

                cont = "" \
                       f"*PROJECT ProjetoVME_{iteracao}_{id}\n" \
                        "*SIMULATOR IMEX 2016.10\n" \
                       f"*ECO_REFERENCE_DATE {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE)}\n" \
                       f"*HISTORY_END_DATE {self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE)}\n" \
                        "*ECO_CONTRACT CONCESSION\n" \
                        "*NPV_TYPE FOP NPVF\n" \
                        "*UNIECO_PROBABILITY_LIST\n"

                for unieco in self._uniecos.keys():
                    aux_path = InOut.ajuste_path(f'{self._path_projeto}/{self._uniecos[unieco]["unieco_path"]}')
                    cont += f'{aux_path} {self._uniecos[unieco]["unieco_prob"]}\n'
                cont += model_list

                path = InOut.ajuste_path(f'{self._path_projeto}/{self._path_simulacao}/{self._qualificador}_{iteracao}_{id}_vme')
                if not TXT().salvar(path_arquivo=f'{path}.mero', conteudo=cont):
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever aquivo {path}.')

                    for ii in range(len(vme_rodou)):
                        prefixo = vme_rodou[ii]
                        if prefixo in unipros:
                            iteracao = unipros[prefixo]['iteracao']
                            id = unipros[prefixo]['id']
                            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao escrever vme.mero para a solucao  {prefixo}) iteracao [{iteracao}] e id [{id}].')
                            solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Escrever_VME.Mero"
                    return solucoes
                else:
                    ler_resultados = {}
                    mero_executavel = InOut.ajuste_path(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_EXECUTAVEL))

                    comando = f'{mero_executavel} vme -i {path}.mero -t Local -s Local -p 1 -n 1 -q LocalQueue -f XML --no-wait -r'
                    self.log(texto=f'Executando comando [{comando}]')
                    self.log(texto=f'Aguarde ...')

                    path_fop_eof = f'{path}.vme.csv'
                    retorno_terminal = Terminal().run(comando)
                    if (retorno_terminal is False) or (not os.path.isfile(path_fop_eof)):
                        for ii in range(len(vme_rodou)):
                            prefixo = vme_rodou[ii]
                            if prefixo in unipros:
                                iteracao = unipros[prefixo]['iteracao']
                                id = unipros[prefixo]['id']
                                self.log(tipo=EnumLogStatus.ERRO, texto=f'Rodar ou ler arquivo .vme.csv da solucao {prefixo}) iteracao [{iteracao}] e id [{id}].')
                                solucoes.get_solucao_by_iteracao_id(iteracao=iteracao, id=id).has_erro = "Executando_VME"
                        return solucoes

                    for ii in range(len(vme_rodou)):
                        prefixo = vme_rodou[ii]
                        if prefixo in unipros:
                            iteracao = unipros[prefixo]['iteracao']
                            id = unipros[prefixo]['id']
                            self.log(texto=f'VME da solucao  [{prefixo}] iteracao [{iteracao}] e id [{id}] foi calculada.')
                            ler_resultados[prefixo] = unipros[prefixo]

                    solucoes = self._ler_dados_economicos(solucoes, path_fop_eof, ler_resultados)
                    return solucoes
