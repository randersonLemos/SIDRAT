import os
import shutil
from datetime import datetime

import src.modulo.problemas_fechados.campo_namorado_posicionamento.base
import src.modulo.problemas_fechados.funcoes_teste.base
from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.Copy import Copy
from src.inout.TXT import TXT
from src.loggin.Loggin import EnumLogStatus
from src.modulo.problemas_fechados.ProblemaFechadoPadrao import ProblemaFechadoPadrao


class CampoNamoradoPosicionamento(ProblemaFechadoPadrao):
    def __init__(self):
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.PATH_RESULTADO] + super(CampoNamoradoPosicionamento, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._base_folder_name = f'base_CampoNamoradoPosicionamento'
        """
        Variavel com o nome do arquivo
        """

    def run(self, contexto: Contexto):
        super(CampoNamoradoPosicionamento, self).run(contexto)

        new_base_path = os.path.join(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), self._base_folder_name)
        folder_data_base = os.path.dirname(src.modulo.problemas_fechados.campo_namorado_posicionamento.base.__file__)

        if not os.path.exists(new_base_path):
            self.log(texto=f'Criando folder base do modelo caixa preta CampoNamoradoPosicionamento')
            if not Copy.copy_folder(folder_data_base, new_base_path):
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Erro ao gerar pasta base para o problema CampoNamoradoPosicionamento')
            try:
                os.remove(os.path.join(new_base_path, "__init__.py"))
            except:
                pass
            try:
                shutil.rmtree(os.path.join(new_base_path, "__pycache__"))
            except:
                pass

        else:
            try:
                os.remove(os.path.join(new_base_path, "campoNamorado_OPT.tpl"))
            except:
                pass
            try:
                os.remove(os.path.join(new_base_path, "campoNamorado_OPT.unieco"))
            except:
                pass
            try:
                os.remove(os.path.join(new_base_path, "campoNamorado_OPT.unimap"))
            except:
                pass
            try:
                os.remove(os.path.join(new_base_path, "dominio.csv"))
            except:
                pass
            try:
                os.remove(os.path.join(new_base_path, "gevt.mero"))
            except:
                pass
            try:
                shutil.rmtree(os.path.join(new_base_path, "includes"))
            except:
                pass
            try:
                os.remove(os.path.join(new_base_path, "__init__.py"))
            except:
                pass
            try:
                shutil.rmtree(os.path.join(new_base_path, "__pycache__"))
            except:
                pass

            Copy.copy_file(os.path.join(folder_data_base, "campoNamorado_OPT.tpl"), os.path.join(new_base_path, "campoNamorado_OPT.tpl"))
            Copy.copy_file(os.path.join(folder_data_base, "campoNamorado_OPT.unieco"), os.path.join(new_base_path, "campoNamorado_OPT.unieco"))
            Copy.copy_file(os.path.join(folder_data_base, "campoNamorado_OPT.unimap"), os.path.join(new_base_path, "campoNamorado_OPT.unimap"))
            Copy.copy_file(os.path.join(folder_data_base, "dominio.csv"), os.path.join(new_base_path, "dominio.csv"))
            Copy.copy_file(os.path.join(folder_data_base, "gevt.mero"), os.path.join(new_base_path, "gevt.mero"))
            Copy.copy_folder(os.path.join(folder_data_base, "includes"), os.path.join(new_base_path, "includes"))

        self._verifica_config()

        gevts_templates = self._contexto.get_gevts_templates(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE))
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR, gevts_templates, sobrescreve=True)

        uniecos = self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH)
        self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR, self._contexto.get_uniecos(uniecos), sobrescreve=True)

    def _verifica_config(self):
        self.log(texto=f'Ajustando configuracao para CampoNamoradoPosicionamento')

        generate_config = False

        if not (self._contexto.tem_atributo(EnumAtributo.SIMULADOR_NOME) and self._contexto.get_atributo(
                EnumAtributo.SIMULADOR_NOME) == 'IMEX'):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.SIMULADOR_NOME,
                                        ['IMEX'],
                                        sobrescreve=True)

        if not (self._contexto.tem_atributo(EnumAtributo.SIMULADOR_VERSAO) and self._contexto.get_atributo(
                EnumAtributo.SIMULADOR_VERSAO) == 2012.1):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.SIMULADOR_VERSAO,
                                        ['2012.10'],
                                        sobrescreve=True)

        if not (self._contexto.tem_atributo(EnumAtributo.INICIALIZACAO_DOMINIO) and self._contexto.get_atributo(
                EnumAtributo.INICIALIZACAO_DOMINIO) == os.path.join(self._base_folder_name, 'dominio.csv')):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.INICIALIZACAO_DOMINIO,
                                        [os.path.join(self._base_folder_name, 'dominio.csv')],
                                        sobrescreve=True)

        if not (self._contexto.tem_atributo(
                EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE) and self._contexto.get_atributo(
                EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE) == '31/05/2017'):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_ECO_REFERENCE_DATE,
                                        ['31/05/2017'],
                                        sobrescreve=True)

        if not (self._contexto.tem_atributo(
                EnumAtributo.AVALIACAO_MERO_UNIMAP_PATH) and self._contexto.get_atributo(
            EnumAtributo.AVALIACAO_MERO_UNIMAP_PATH) == os.path.join(self._base_folder_name, 'campoNamorado_OPT.unimap')):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_UNIMAP_PATH,
                                        [os.path.join(self._base_folder_name, 'campoNamorado_OPT.unimap')],
                                        sobrescreve=True)

        if not (self._contexto.tem_atributo(
                EnumAtributo.AVALIACAO_MERO_UNIECO_PATH) and self._contexto.get_atributo(
            EnumAtributo.AVALIACAO_MERO_UNIECO_PATH) == os.path.join(self._base_folder_name, 'campoNamorado_OPT.unieco')):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH,
                                        [os.path.join(self._base_folder_name, 'campoNamorado_OPT.unieco')],
                                        sobrescreve=True)

        gevt_name = 'gevt.mero'
        tpl_name = 'campoNamorado_OPT.tpl'
        if not (self._contexto.tem_atributo(
                EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE) and self._contexto.get_atributo(
            EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE) == f'{os.path.join(self._base_folder_name, gevt_name)}#'
                f'{os.path.join(self._base_folder_name, tpl_name)}'):
            generate_config = True
            self._contexto.set_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE,
                                        [f'{os.path.join(self._base_folder_name, gevt_name)}#'
                                         f'{os.path.join(self._base_folder_name, tpl_name)}'], sobrescreve=True)
            self._contexto.set_atributo(EnumAtributo.REDUCAO_TYPE,
                                        [False],
                                        sobrescreve=True)

        if generate_config:
            self._generate_copy_config()
        else:
            self._copy_config()

    def _generate_copy_config(self):
        run_key = datetime.now().strftime("%Y%m%d-%H%M%S")
        [config_name, extension] = os.path.basename(self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO)).split(
            '.')

        if not Copy.copy_file(self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO),
                              os.path.join(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
                                           self._base_folder_name,
                                           f'{config_name}_{run_key}.{extension}.bk')):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro geracao arquivo de backup da configuracao')

        cont = ''

        for [key, value] in self._contexto._configuracao.items():
            for val in value:
                if key not in [EnumAtributo.MODULE.name, EnumAtributo.PATH_PROJETO.name,
                               EnumAtributo.PATH_CONFIGURACAO.name, EnumAtributo.PATH_LOG.name]:
                    cont += f'{key}\t{val}\n'

        if not TXT().salvar(
                os.path.join(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), self._base_folder_name,
                             f'{config_name}.{extension}'), cont,
                'w'):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro geracao arquivo de configuracao')

        self.log(texto=f'Arquivo de configuracao gerado.{config_name}')

    def _copy_config(self):
        [config_name, extension] = os.path.basename(self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO)).split(
            '.')

        if not Copy.copy_file(self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO),
                              os.path.join(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO),
                                           self._base_folder_name,
                                           f'{config_name}.{extension}')):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro geracao arquivo de backup da configuracao')
