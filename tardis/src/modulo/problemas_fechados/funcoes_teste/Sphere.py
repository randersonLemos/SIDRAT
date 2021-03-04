import os
from datetime import datetime

import src.modulo.problemas_fechados.funcoes_teste.base.sphere
from src.contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.inout.Copy import Copy
from src.inout.TXT import TXT
from src.loggin.Loggin import EnumLogStatus
from src.modulo.problemas_fechados.ProblemaFechadoPadrao import ProblemaFechadoPadrao


class Sphere(ProblemaFechadoPadrao):
    def __init__(self):
        super().__init__()

        self._name = __name__

        self._necessidade.append(EnumAtributo.PATH_RESULTADO)

        self._base_folder_name = 'base_SPHERE'

        self._dominio_file_name = 'dominio_sphere.txt'


    def run(self, contexto: Contexto):
        """
        Metodo responsavel por setar configuracao ao utilizar funcoes de teste para avaliacao.

        :param Contexto contexto: contexto com todas as informações necessárias.
        """
        self.log(texto=f'Executando {self._name}')

        self._contexto = contexto
 
        new_base_path = os.path.join(self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), self._base_folder_name)

        folder_data_base = os.path.dirname(src.modulo.problemas_fechados.funcoes_teste.base.sphere.__file__)

        Copy.copy_file(os.path.join(folder_data_base, self._dominio_file_name),
                       os.path.join(new_base_path, self._dominio_file_name))

        self._verifica_config()


    def _verifica_config(self):
        if not (self._contexto.tem_atributo(EnumAtributo.INICIALIZACAO_DOMINIO) and
                self._contexto.get_atributo(EnumAtributo.INICIALIZACAO_DOMINIO) == os.path.join(self._base_folder_name, self._dominio_file_name)
               ):

            self._contexto.set_atributo(EnumAtributo.INICIALIZACAO_DOMINIO,
                                        [os.path.join(self._base_folder_name, self._dominio_file_name)],
                                        sobrescreve=True)
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
