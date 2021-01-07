"""
:author: Rafael
:data: 12/03/2020
"""
import re

from lupa import LuaRuntime

from src.contexto.EnumAtributo import EnumAtributo
from src.inout.InOut import InOut
from src.loggin.Enum import EnumLogStatus
from src.modulo.avaliacao.AvaliadorPadrao import AvaliadorPadrao
from src.problema.Solucao import Of
from src.problema.Solucoes import Solucoes


class Wahoo(AvaliadorPadrao):
    """
    Isto é um comentário da classe MyClass
    """

    def __init__(self):
        """
        Comentário do construtor
        
        :param int var1: Isto é o valor do atributo 1
        """
        super(Wahoo, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.AVALIACAO_WAHOO_PATH] + super(Wahoo, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._qualificador = None
        self._load_file = None
        path_interface = ".".join(__name__.split(".")[1:len(__name__.split("."))-1]) + ".interface"
        self._comando_add_variavel = f'function(nome, valor)              local interf = require("{path_interface}") return add_variavel(nome, valor) end'
        self._comando_executa_wahoo = f'function(id, load_file, file_lua) local interf = require("{path_interface}") return executa_wahoo(id, load_file, file_lua) end'
        self._file_lua = None

    def run(self):
        super(Wahoo, self).run()

        lua = LuaRuntime(unpack_returned_tuples=True)
        lua_add_variavel = lua.eval(self._comando_add_variavel)
        lua_executa_wahoo = lua.eval(self._comando_executa_wahoo)

        self._load_file = self._contexto.get_atributo(EnumAtributo.AVALIACAO_WAHOO_PATH)
        self._file_lua = InOut.path_to_array(self._load_file)[-1]
        if re.search('.lua', self._file_lua, re.IGNORECASE) is None:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Caminho para o arquivo lua não esta correto [{self._load_file}]')
        self._file_lua = self._file_lua.replace(".lua", "")
        self._load_file = self._load_file.replace(self._file_lua, "?")

        iteracoes = self._contexto.get_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, valor_unico_list=True)
        iteracoes_str = ""
        for ss in iteracoes:
            iteracoes_str = f'{iteracoes_str}_{ss}'

        self._qualificador = self._contexto.get_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR)

        solucoes: Solucoes = self._contexto.get_atributo(EnumAtributo.SOLUCOES)
        list_solucoes = solucoes.get_solucoes_by_iteracao_para_avaliar(iteracoes)
        if len(list_solucoes) <= 0:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Não há estudo sem erro para avaliar')
            return self._contexto

        for k_iteracao, v_est in list_solucoes.items():
            for k_id, vv_est in v_est.items():
                try:
                    if self._add_variavel_wahoo(lua_add_variavel, vv_est) is False:
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao variaveis da solucao, iteracao [{k_iteracao}], id [{k_id}] no WAHOO.')
                        solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "WAHOO_ADD"
                        continue

                except Exception as ex:
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao adicionar variaveis no WAHOO.', info_ex=str(ex))
                    solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "WAHOO_ADD"
                    continue

                try:
                    of = self._executa_wahoo(lua_executa_wahoo, k_id)
                    if of is None:
                        self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executar o WAHOO')
                        solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "WAHOO_EXECUTE"
                    else:
                        solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).of[self._nome_of_mono].valor = of
                        solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).set_avaliada()

                except Exception as ex:
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executar no WAHOO. Verificar o caminho [{self._contexto.get_atributo(EnumAtributo.AVALIACAO_WAHOO_PATH)}]', info_ex=str(ex))
                    solucoes.get_solucao_by_iteracao_id(k_iteracao, k_id).has_erro = "WAHOO_EXECUTE"
                    continue

        self._contexto.set_atributo(EnumAtributo.SOLUCOES, [solucoes], True)

    def _add_variavel_wahoo(self, lua_add_variavel,  solucao):
        try:
            for nome, valor in solucao.get_variaveis_nome_valor().items():
                if not lua_add_variavel(nome, valor):
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Variavel [{nome}] não foi adicionada com sucesso no WAHOO')
            return True
        except Exception as ex:
            self.log(tipo=EnumLogStatus.WARN, texto=f'Erro ao escrever arquivo de parametro.', info_ex=str(ex))
            return False

    def _executa_wahoo(self, lua_executa_wahoo, id):
        return lua_executa_wahoo(id, self._load_file, self._file_lua)
