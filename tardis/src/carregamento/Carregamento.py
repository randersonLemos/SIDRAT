"""
:author: Rafael
:data: 06/12/2019
"""
from copy import deepcopy as deepcopy

from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.InOut import InOut
from src.inout.LogarMemoria import LogarMemoria
from src.inout.TXT import TXT
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.modulo.Modulo import Modulo
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.avaliacao.Avaliador import Avaliador
from src.modulo.criterio_parada.CriterioParada import CriterioParada
from src.modulo.inicializacao.Inicializador import Inicializador
from src.modulo.otimizacao.Otimizador import Otimizador
from src.modulo.problemas_fechados.ProblemaFechado import ProblemaFechado
from src.modulo.reducao.Redutor import Redutor
from src.modulo.sorteio.Sorteio import Sorteio
from src.modulo.visualizacao.Visualizacao import Visualizacao


class Carregamento(Loggin):
    """
        Classe destinada a ler o arquivo de configuracao e salvar em uma estrutura interna.
        Onde sera possivel buscar, e editar.
    """


    def __init__(self, path_projeto: str, path_config: str, modules: list):
        """
        Chama a função de leitura das informações nor arquivo de configura no caminho path_configuracao

        :param str path_projeto: O caminho referente a raiz do projeto
        :param str arquivo_config: Caminho para o arquivo de configuracao
        """
        super().__init__()
        self._name = __name__  # variável com nome do arquivo

        path_projeto = TXT().ajuste_path(path_projeto)
        path_config  = TXT().ajuste_path(path_projeto + '/' + path_config)

        if not TXT().diretorio_existe(path_projeto):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Diretorio [{path_projeto}] não existe.")

        if not TXT().arquivo_existe(path_config):
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"O arquivo de configuracao [{path_config}] não existe.")

        path_log = TXT().ajuste_path(f'{path_projeto}/log.out')

        Loggin.set_arquivo_log(path_log)

        self.log(texto="[INICIO_TARDIS] - Iniciando Carregamento.")

        self._contexto = Contexto()

        self._contexto.set_atributo(EnumAtributo.PATH_PROJETO, [path_projeto])
        self._contexto.set_atributo(EnumAtributo.PATH_CONFIGURACAO, [path_config])
        self._contexto.set_atributo(EnumAtributo.PATH_LOG, [path_log])

        try:
            self._carregar_informacao(modules)
            self._contexto.set_defaults()
            self._valida_contexto()
        except Exception as ex:
            self.log(texto="Erro para configurar valores defaults", info_ex=str(ex), tipo=EnumLogStatus.ERRO_FATAL)


    def _carregar_informacao(self, modules: list):
        """
        Ler o arquivo carrega toda informação e adiciona na variavel _configuracao
        """

        linha = ''
        try:
            contexto = TXT().ler(str(self._contexto.get_atributo(EnumAtributo.PATH_CONFIGURACAO)))
            for module in modules:
                self._contexto.set_atributo('module', [InOut.ajusta_entrada(module)])

            for linha in contexto:
                linha = linha.replace("\n", "").strip()
                if (len(linha) > 0) and (not linha[0] == "*"):
                    sp = linha.split()
                    chave = sp[0].strip()
                    valor = sp[1].strip()
                    if len(sp) > 2:
                        for ii in range(2, len(sp)):
                            sp[ii] = sp[ii].strip()
                            if len(sp[ii]) > 0:
                                valor = f'{valor} {sp[ii]}'

                    self._contexto.set_atributo(chave, [InOut.ajusta_entrada(valor)])
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Erro ao carregar arquivos. Linha [{linha}]", info_ex=f'ex[{str(ex)}]')


    def run(self) -> Contexto:
        self.log(texto=f'Executando o {self._name}')

        modulos = self._contexto.get_atributo(EnumAtributo.MODULE)

        obj_modulo = ModuloPadrao()
        if EnumModulo.INICIALIZACAO.name in modulos:
            obj_modulo = Inicializador()
            obj_modulo.carrega(self._contexto)
            obj_modulo.check_necessidades()
        self._contexto.set_modulo(EnumModulo.INICIALIZACAO, obj_modulo)

        #problema_fechado = ModuloPadrao()
        #if EnumModulo.PROBLEMA_FECHADO.name in modulos:
        #    problema_fechado = Modulo(ProblemaFechado()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.PROBLEMA_FECHADO, problema_fechado)

        #sorteio = ModuloPadrao()
        #if EnumModulo.SORTEIO.name in modulos:
        #    sorteio = Modulo(Sorteio()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.SORTEIO, sorteio)

        #avaliacao = ModuloPadrao()
        #if EnumModulo.AVALIACAO.name in modulos:
        #    avaliacao = Modulo(Avaliador()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.AVALIACAO, avaliacao)

        #redutor = ModuloPadrao()
        #if EnumModulo.REDUCAO.name in modulos:
        #    redutor = Modulo(Redutor()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.REDUCAO, redutor)

        #criterio_parada = ModuloPadrao()
        #if EnumModulo.CRITERIOPARADA.name in modulos:
        #    criterio_parada = Modulo(CriterioParada()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.CRITERIOPARADA, criterio_parada)

        #otimizador = ModuloPadrao()
        #if EnumModulo.OTIMIZACAO.name in modulos:
        #    otimizador = Modulo(Otimizador()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.OTIMIZACAO, otimizador)

        #visualizacao = ModuloPadrao()
        #if EnumModulo.VISUALIZACAO.name in modulos:
        #    visualizacao = Modulo(Visualizacao()).run(self._contexto)
        #self._contexto.set_modulo(EnumModulo.VISUALIZACAO, visualizacao)

        #LogarMemoria(self._contexto)
        return deepcopy(self._contexto)

    def _valida_contexto(self):
        try:
            self._valida_ofs()
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto="Erro ao validar o contexto", info_ex=str(ex))

    def _valida_of_existe(self, nome_of):
        if EnumValues.VPL.name not in nome_of and \
                EnumValues.NP.name not in nome_of and \
                EnumValues.WP.name not in nome_of and \
                EnumValues.VME.name not in nome_of and \
                EnumValues.SPHERE.name not in nome_of and \
                EnumValues.RASTRIGIN.name not in nome_of and \
                EnumValues.ROSENBROCK.name not in nome_of and \
                EnumValues.PYTHON.name not in nome_of and \
                EnumValues.WAHOO.name not in nome_of and\
                EnumValues.CLUSTERING.name not in nome_of and \
                EnumValues.KNAPSACK.name not in nome_of and \
                EnumValues.WI.name not in nome_of and \
                EnumValues.GI.name not in nome_of:
            self.log(tipo=EnumLogStatus.ERRO, texto=f"A of de nome [{nome_of}] não é valida.")
            self.log(tipo=EnumLogStatus.ERRO_FATAL,
                     texto=f"Os nomes de of tem de ser um dos: "
                           f"{EnumValues.VPL.name}, "
                           f"{EnumValues.NP.name}, "
                           f"{EnumValues.WP.name}, "
                           f"{EnumValues.VME.name},"
                           f"{EnumValues.ROSENBROCK.name},"
                           f"{EnumValues.RASTRIGIN.name},"
                           f"{EnumValues.SPHERE.name},"
                           f"{EnumValues.PYTHON.name},"
                           f"{EnumValues.WAHOO.name},"
                           f"{EnumValues.WI.name},"
                           f"{EnumValues.GI.name},"
                           f"{EnumValues.KNAPSACK.name},"
                           f"{EnumValues.CLUSTERING.name}.")

    def _valida_of_direcao(self, direcao_of):
        if direcao_of not in EnumValues.MAX.name and direcao_of not in EnumValues.MIN.name:
            self.log(tipo=EnumLogStatus.ERRO, texto=f"A direção [{direcao}] não é valida.")
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"As direcções de of tem de ser um dos: {EnumValues.MIN.name}, {EnumValues.MAX.name}.")

    def _valida_of_mult_objetivo(self, nomes_direcoes_of):
        if len(nomes_direcoes_of) > 1:
            for nome_direcao_of in nomes_direcoes_of:
                if EnumValues.MULTIOBJETIVO.name in nome_direcao_of:
                    return

            if self._contexto.get_atributo(EnumAtributo.OTIMIZACAO_TYPE) not in [EnumValues.PYMOO_NSGA3.name]:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Foi definido multipla ofs, e isso caracteriza otmização mult-objetivo. Para mult-objetivo é permitido somente o otimizador [{EnumValues.PYMOO_NSGA3.name}].')

    def _valida_of_vpl_vme(self, nomes_direcoes_of):
        if EnumValues.VPL.name in nomes_direcoes_of:
            if type(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH)) is list and len(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH)) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Não deve definir vários [{EnumAtributo.AVALIACAO_MERO_UNIECO_PATH.name}] quando selecionado of [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name} = [{EnumValues.VPL.name}]]. Para usar vários [{EnumAtributo.AVALIACAO_MERO_UNIECO_PATH.name}] escolha a of [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.nome} = [{EnumValues.VME.name}]]')

            elif type(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE)) is list and len(self._contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE)) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Não deve definir vários [{EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE.name}] quando selecionado of [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name} = [{EnumValues.VPL.name}]]. Para usar vários [{EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE.name}] escolha a of [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.nome} = [{EnumValues.VME.name}]]')

            elif EnumValues.VME.name in nomes_direcoes_of:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Não deve definir as of({EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}) [{EnumValues.VME.name}] e [{EnumValues.VPL.name}] juntas.')

    def _valida_of_funcao(self, nomes_direcaoes_of):
        nome_of = None
        if EnumValues.SPHERE.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.SPHERE.name not in nomes_direcaoes_of:
                nome_of = EnumValues.SPHERE.name
        elif EnumValues.RASTRIGIN.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.RASTRIGIN.name not in nomes_direcaoes_of:
                nome_of = EnumValues.RASTRIGIN.name
        elif EnumValues.ROSENBROCK.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.ROSENBROCK.name not in nomes_direcaoes_of:
                nome_of = EnumValues.ROSENBROCK.name
        elif EnumValues.PYTHON.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.PYTHON.name not in nomes_direcaoes_of:
                nome_of = EnumValues.PYTHON.name
        elif EnumValues.WAHOO.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.WAHOO.name not in nomes_direcaoes_of:
                nome_of = EnumValues.WAHOO.name
        elif EnumValues.CLUSTERING.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.CLUSTERING.name not in nomes_direcaoes_of:
                nome_of = EnumValues.CLUSTERING.name
        elif EnumValues.KNAPSACK.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):
            if len(nomes_direcaoes_of) > 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}]=[{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}] não aceita mult-objetivo.')
            elif EnumValues.KNAPSACK.name not in nomes_direcaoes_of:
                nome_of = EnumValues.KNAPSACK.name

        if nome_of is not None:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"O atributo [{EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS.name}], só aceita valor [{nome_of}], para o [{EnumAtributo.AVALIACAO_TYPE.name}] = [{nome_of}]")

    def _valida_of_mero(self, nomes_direcaoes_of):
        ofs_nao_validas = [EnumValues.PYTHON.name,
                           EnumValues.WAHOO.name,
                           EnumValues.SPHERE.name,
                           EnumValues.RASTRIGIN.name,
                           EnumValues.ROSENBROCK.name,
                           EnumValues.CLUSTERING.name,
                           EnumValues.KNAPSACK.name]
        if EnumValues.MERO.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE) or \
            EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE) or \
            EnumValues.CAMPO_NAMORADO_POSICIONAMENTO.name in self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE):

            for of in ofs_nao_validas:
                if of in nomes_direcaoes_of:
                    self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'O atributo [{EnumAtributo.AVALIACAO_TYPE.name}] = [{self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)}]  não permite a [{EnumAtributo.AVALIACAO_DIRECAO_OF.name}] = [{of}].')

    def _valida_ofs(self):
        try:
            nomes_direcoes_of = self._contexto.get_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, valor_unico_list=True)

            # Valida mult-objetivo
            self._valida_of_mult_objetivo(nomes_direcoes_of)
            # Valida VPL e VME
            self._valida_of_vpl_vme(nomes_direcoes_of)
            # Valida Funcoes Teste e Python e Wahoo
            self._valida_of_funcao(nomes_direcoes_of)
            # Validar OFs para execução no MERO
            self._valida_of_mero(nomes_direcoes_of)

            for nome_of in nomes_direcoes_of:
                # Valida se of existe
                self._valida_of_existe(nome_of)
                # Valida se a direcao existe
                self._valida_of_direcao(nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name])

        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto="Erro ao validar o contexto", info_ex=str(ex))
