"""
:author: Luis
:data: 17/01/2020
"""
import pickle

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.modulo.inicializacao.InicializadorPadrao import InicializadorPadrao
from src.inout.InOut import InOut
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.modulo.EnumModulo import EnumModulo


class Resume(InicializadorPadrao):

    def __init__(self):

        super(Resume, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.INICIALIZACAO_RESUME_PATH] + super(Resume, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

    def run(self, contexto):

        """
        Executa a inicizalicao Reestart

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o contexto atualizado
        :rtype: Contexto
        """
        super(Resume, self).run(contexto)

        contexto_carregado: Contexto = self._carregar_contexto()
        for modulo in list(EnumModulo):
            if modulo == EnumModulo.INICIALIZACAO:
                continue

            valor = self._contexto.get_modulo(modulo)
            if valor is not None:
                contexto_carregado.set_modulo(modulo, valor)

        try:
            for atributo in list(EnumAtributo):
                self.log(texto=f'Lendo atribudo arquivo resume [{atributo.name}].')
                if atributo == EnumAtributo.SOLUCOES:
                    continue
                if atributo == EnumAtributo.SOLUCAO_BASE:
                    continue

                if self._contexto.tem_atributo(atributo):
                    valor = self._contexto.get_atributo(atributo)
                    contexto_carregado.set_atributo(atributo, valor, True)
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto="Erro ao setar atributos", info_ex=str(ex))

        self._contexto = contexto_carregado

    def _carregar_contexto(self):
        try:
            path_resume = InOut().ajuste_path('\\'.join([self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), self._contexto.get_atributo(EnumAtributo.INICIALIZACAO_RESUME_PATH)]))
            with open(path_resume, 'rb') as file:
                contexto_resume = pickle.load(file)

            Loggin.set_arquivo_log(self._contexto.arquivo_log)
            contexto_resume.set_arquivo_log(self._contexto.arquivo_log)
            contexto_resume.set_atributo(EnumAtributo.PATH_PROJETO, self._contexto.get_atributo(EnumAtributo.PATH_PROJETO), True)
            contexto_resume.set_atributo(EnumAtributo.PATH_CONFIGURACAO, self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO), True)
            contexto_resume.set_atributo(EnumAtributo.PATH_LOG, self._contexto.get_atributo(EnumAtributo.PATH_LOG), True)

            return contexto_resume
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto='Erro ao carregar arquivo de resume', info_ex=str(ex))
