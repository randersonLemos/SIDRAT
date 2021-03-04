"""
:author: Rafael
:data: 06/12/2019
"""
import gc

from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.inout.InOut import InOut
from src.loggin.Loggin import Loggin, EnumLogStatus
from src.modulo.EnumModulo import EnumModulo


def _get_chave(atributo: EnumAtributo):
    """
    retorna o valor correto para salvar no contexto

    :param EnumAtributo atributo: Atributo para salvar
    :return: chave correta
    :rtype: str
    """
    chave = None
    for attr in EnumAtributo:
        if isinstance(atributo, str):
            if attr.name.upper() == atributo.upper():
                chave = atributo.upper()
                break
        else:
            if attr == atributo:
                chave = atributo.name.upper()
                break
    return chave


class Contexto(Loggin):
    """
    Classe que contem todas as informações de configuracao
    """


    def __init__(self):
        super().__init__()

        self._name = __name__

        self._configuracao = {}  # Dicionário com todos os dicionários

        self._modulo = {}


    def set_modulo(self, enum_modulo: EnumModulo, modulo):
        """
        Setar os modulos da aplicação
        :param EnumModulo enum_modulo: Enum que contem todos os tipo de modulos
        :param Object modulo: O modulo para setar
        """
        if modulo is None:
            del self._modulo[enum_modulo.name]
            self._modulo[enum_modulo.name] = None
            gc.collect()
        else:
            self._modulo[enum_modulo.name] = modulo


    def get_modulo(self, enum_modulo: EnumModulo) -> object:
        """
        Buscar o modulo informado pelo enum
        :param EnumModulo enum_modulo: Enum com todos os modulos informados
        :return: Modulo desejado
        :rtype: object
        """

        if enum_modulo.name in self._modulo:
            return self._modulo[enum_modulo.name]
        return None


    def set_atributo(self, atributo: EnumAtributo, valor: list, sobrescreve: bool = False) -> None:
        """
        Método para escrever no contexto. Ele não sobrescreve o que esta escrito, a menos que se definido.

        :param EnumAtributo atributo: Chave da configuracao
        :param object valor: Valor da configuracao
        :param bool sobrescreve: Se deve ou não sobrescrever o valor a adicionar.
        :type valor: object
        """

        if valor is None:
            try:
                del self._configuracao[atributo]
                gc.collect()
                return None
            except Exception as ex:
                self.log(tipo=EnumLogStatus.WARN, texto=f"O atributo [{atributo}] apresenta valor None")
                return None

        aux_valor = []

        if type(valor) is list:
            aux_valor = valor
        elif type(valor) is dict:
            aux_valor = valor
        else:
            aux_valor.append(valor)

        chave = _get_chave(atributo)
        if chave is not None:
            if chave in self._configuracao:
                if sobrescreve is True:
                    self._configuracao[chave] = aux_valor
                else:
                    self._configuracao[chave] += aux_valor
            else:
                self._configuracao[chave] = aux_valor

            self.log(texto=f"Grava no contexto - chave [{chave}] valor [{self._configuracao[chave]}]")
        else:
            self.log(texto=f"A chave {atributo}, não é um atributo valido", tipo=EnumLogStatus.WARN)


    def get_atributo(self, atributo: EnumAtributo, valor_unico_list: bool = False) -> object:
        """
        Obtem o valor do atributo selecionado

        :param EnumAtributo atributo: Chave da configuracao
        :param bool valor_unico_list: Se só tiver um valor devemos retornar uma lista de um valor ou o valor
        :return: Devolve o valor do atributo selecionado
        :rtype: object
        """
        try:
            chave = _get_chave(atributo)
            if chave is not None:
                if len(self._configuracao[chave]) == 1:
                    if valor_unico_list:
                        return self._configuracao[chave]
                    elif type(self._configuracao[chave]) is dict:
                        return self._configuracao[chave]
                    return self._configuracao[chave][0]
                return self._configuracao[chave]
            else:
                self.log(texto=f"A chave {atributo}, não é um atributo valido", tipo=EnumLogStatus.WARN)
                return None
        except Exception as ex:
            self.log(texto=f'O atributo {atributo} não esta no contexto', tipo=EnumLogStatus.WARN, info_ex=str(ex))
            return None


    def tem_atributo(self, chave: EnumAtributo) -> bool:
        """
        Verificar se existe a chave no contexto

        :param EnumAtributo chave: Atributo de busca
        :return: True se existir, False se nao existir
        :rtype: bool
        """
        if _get_chave(chave) in self._configuracao:
            return True
        return False


    def get_gevts_templates(self, gevts_templates):
        gevts_templantes_executar = {}
        if type(gevts_templates) is list:
            for gevt_template in gevts_templates:
                separacao = gevt_template.split('#')
                gevt_path = InOut.ajuste_path(separacao[0])
                gevt_file_name = (gevt_path.split(InOut.barra())[-1]).split('.')[0]
                if len(separacao) <= 1:
                    self.log(tipo=EnumLogStatus.ERRO_FATAL,
                             texto=f"Precisa ser informado o template para o GEVT [{gevt_template}]")
                template_path = InOut.ajuste_path(separacao[1])
                template_file_name = (template_path.split(InOut.barra())[-1]).split('.')[0]
                template_prob = 1 / len(gevts_templates)
                if len(separacao) > 2:
                    template_prob = separacao[2]

                    gevts_templantes_executar[f'{gevt_file_name}_{template_file_name}'] = {'gevt_path': gevt_path,
                                                                                           'gevt_file_name': gevt_file_name,
                                                                                           'template_path': template_path,
                                                                                           'template_file_name': template_file_name,
                                                                                           'template_prob': template_prob}
        else:
            separacao = gevts_templates.split('#')
            gevt_path = InOut.ajuste_path(separacao[0])
            gevt_file_name = (gevt_path.split(InOut.barra())[-1]).split('.')[0]
            if len(separacao) <= 1:
                self.log(tipo=EnumLogStatus.ERRO_FATAL,
                         texto=f"Precisa ser informado o TPL para o GEVT [{gevts_templates}]")
            template_path = InOut.ajuste_path(separacao[1])
            template_file_name = (template_path.split(InOut.barra())[-1]).split('.')[0]
            template_prob = 1
            if len(separacao) > 2 and int(InOut.ajusta_entrada(separacao[2])) != int(1):
                self.log(tipo=EnumLogStatus.ERRO, texto=f"Não faz sentido probabilidade diferente de 1 quando há somente um template.")

            gevts_templantes_executar[f'{gevt_file_name}_{template_file_name}'] = {'gevt_path': gevt_path,
                                                                                   'gevt_file_name': gevt_file_name,
                                                                                   'template_path': template_path,
                                                                                   'template_file_name': template_file_name,
                                                                                   'template_prob': template_prob}
        return gevts_templantes_executar


    def get_uniecos(self, uniecos):
        uniecos_executar = {}
        if type(uniecos) is list:
            for unieco in uniecos:
                uni_separado = unieco.split("#")
                unieco_path = InOut.ajuste_path(uni_separado[0])
                unieco_prob = 1 / len(uniecos)
                if len(uni_separado) > 1:
                    unieco_path = uni_separado[0]
                    unieco_prob = uni_separado[1]

                unieco_file_name = (unieco_path.split(InOut().barra())[-1]).split('.')[0]
                uniecos_executar[unieco_file_name] = {'unieco_path': unieco_path,
                                                      'unieco_file_name': unieco_file_name,
                                                      'unieco_prob': unieco_prob}
        else:
            uni_separado = uniecos.split("#")
            unieco_path = InOut.ajuste_path(uni_separado[0])
            unieco_prob = 1
            if len(uni_separado) > 1:
                unieco_path = uni_separado[0]
                unieco_prob = uni_separado[1]

            unieco_file_name = (unieco_path.split(InOut().barra())[-1]).split('.')[0]
            uniecos_executar[unieco_file_name] = {'unieco_path': unieco_path,
                                                  'unieco_file_name': unieco_file_name,
                                                  'unieco_prob': unieco_prob}

        return uniecos_executar


    def set_defaults(self):
        if not self.tem_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR):
            self.set_atributo(EnumAtributo.AVALIACAO_QUALIFICADOR, [EnumValues.TOTAL.name])

        if not self.tem_atributo(EnumAtributo.INICIALIZACAO_SIMULA_BASE):
            self.set_atributo(EnumAtributo.INICIALIZACAO_SIMULA_BASE, [True])

        if not self.tem_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR):
            if self.tem_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE):
                gevts_templates = self.get_gevts_templates(self.get_atributo(EnumAtributo.AVALIACAO_MERO_GEVT_TEMPLATE))
                self.set_atributo(EnumAtributo.AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR, [gevts_templates])

        if not self.tem_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR):
            if self.tem_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH):
                uniecos = self.get_atributo(EnumAtributo.AVALIACAO_MERO_UNIECO_PATH)
                self.set_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR, self.get_uniecos(uniecos))
            else:
                self.set_atributo(EnumAtributo.AVALIACAO_MERO_UNIECOS_EXECUTAR, [None])

        if not self.tem_atributo(EnumAtributo.AVALIACAO_MERO_TEMPO_MAX_SIM):
            self.set_atributo(EnumAtributo.AVALIACAO_MERO_TEMPO_MAX_SIM, [2], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.SORTEIO_TYPE):
            self.set_atributo(EnumAtributo.SORTEIO_TYPE, [EnumValues.HLDG.name])

        if not self.tem_atributo(EnumAtributo.AVALIACAO_MELHORES_QTD_SALVAR):
            self.set_atributo(EnumAtributo.AVALIACAO_MELHORES_QTD_SALVAR, [5], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.AVALIACAO_PATH_MELHORES):
            self.set_atributo(EnumAtributo.AVALIACAO_PATH_MELHORES, ['melhores'], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.RANDOM_SEED):
            import time
            aleatoridade = int(time.time())
            self.log(texto=f'{EnumAtributo.RANDOM_SEED.name} [{aleatoridade}]')
            self.set_atributo(EnumAtributo.RANDOM_SEED, [aleatoridade], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.SORTEIO_SOLUCOES_NOVAS):
            self.set_atributo(EnumAtributo.SORTEIO_SOLUCOES_NOVAS, [None], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.INTERNO_CRITERIO_PARADA_QTD_SOLUCAO_NOVA):
            self.set_atributo(EnumAtributo.INTERNO_CRITERIO_PARADA_QTD_SOLUCAO_NOVA, [0], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.VISUALIZACAO_TYPE):
            self.set_atributo(EnumAtributo.VISUALIZACAO_TYPE, [EnumValues.EXECUCAO], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.AVALIACAO_DIRECAO_OF):
            nome_of = EnumValues.VPL.name
            direcao_of = EnumValues.MAX.name
            if EnumValues.SPHERE.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.SPHERE.name
            elif EnumValues.RASTRIGIN.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.RASTRIGIN.name
            elif EnumValues.ROSENBROCK.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.ROSENBROCK.name
            elif EnumValues.PYTHON.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.PYTHON.name
            elif EnumValues.WAHOO.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.WAHOO.name
            elif EnumValues.KNAPSACK.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.KNAPSACK.name
            elif EnumValues.CLUSTERING.name in self.get_atributo(EnumAtributo.AVALIACAO_TYPE):
                nome_of = EnumValues.CLUSTERING.name

            self.set_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, [nome_of], sobrescreve=True)
            self.set_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, {nome_of: {EnumValues.DIRECAO.name: direcao_of, EnumValues.OF.name: nome_of}}, sobrescreve=True)
            self.set_atributo(EnumAtributo.AVALIACAO_DIRECAO_OF, [str(f"{direcao_of} {nome_of}")], sobrescreve=True)
        else:
            avaliacao_direacao_of = self.get_atributo(EnumAtributo.AVALIACAO_DIRECAO_OF, valor_unico_list=True)

            if len(avaliacao_direacao_of) > 1:
                ofs_possiveis = [EnumValues.VPL.name, EnumValues.VME.name, EnumValues.WI.name, EnumValues.WP.name, EnumValues.GI.name, EnumValues.NP.name]
                nome_of_mono = None
                nomes_ofs = {}
                nomes_direcoes_ofs = []
                keys_nomes_ofs = "|"

                for nome_direcao_of in avaliacao_direacao_of:
                    aux = nome_direcao_of.upper().split(" ")
                    if len(aux) > 1:
                        nome_of = "".join(aux[1:]).upper()
                        direcao_of = str(aux[0]).upper()
                    else:
                        nome_of = str(aux[0]).upper()

                    if f'|{nome_of}|' in keys_nomes_ofs:
                        self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Não pode setar duas [{EnumAtributo.AVALIACAO_DIRECAO_OF.name}] com a mesma OF. No caso [{nome_of}]")

                    contem = False
                    for of_possivel in ofs_possiveis:
                        if f"|{of_possivel}|" in f"|{nome_of}|":
                            nomes_direcoes_ofs.append(str(f"{direcao_of} {of_possivel}"))
                            nomes_ofs[of_possivel] = {EnumValues.DIRECAO.name: direcao_of, EnumValues.OF.name: of_possivel}
                            keys_nomes_ofs += f"{of_possivel}|"
                            contem = True
                            if len(nome_of.replace(" ", "").replace(of_possivel, "")) > 0:
                                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"A OF [{nome_of}] apresenta erro. Veja as OFs possiveis {ofs_possiveis}")

                    if contem is False:
                        self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"A OF [{nome_of}] não pode ser definida com outras funções, ou não esta na lista de OFs multiobjetivo {ofs_possiveis}.")

                self.set_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, [nome_of_mono], sobrescreve=True)
                self.set_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, nomes_ofs, sobrescreve=True)
                self.set_atributo(EnumAtributo.AVALIACAO_DIRECAO_OF, nomes_direcoes_ofs, sobrescreve=True)
            else:
                ofs_possiveis_multi = [EnumValues.VPL.name, EnumValues.VME.name, EnumValues.WI.name, EnumValues.WP.name,
                                       EnumValues.GI.name, EnumValues.NP.name]
                ofs_possiveis_mono = [EnumValues.SPHERE.name, EnumValues.RASTRIGIN.name,
                                      EnumValues.ROSENBROCK.name, EnumValues.KNAPSACK.name, EnumValues.CLUSTERING.name,
                                      EnumValues.PYTHON.name, EnumValues.WAHOO.name] + ofs_possiveis_multi
                nome_of_mono = None
                nomes_ofs = {}
                nomes_direcoes_ofs = []

                nome_direcao_of = avaliacao_direacao_of[0]
                aux = nome_direcao_of.upper().split(" ")
                if len(aux) > 1:
                    nome_of = "".join(aux[1:])
                    direcao_of = aux[0]
                else:
                    nome_of = aux[0]

                eh_of_mono = False
                for of_possivel in ofs_possiveis_mono:
                    if f"|{of_possivel}|" in f"|{nome_of}|":
                        nomes_direcoes_ofs.append(str(f"{direcao_of} {of_possivel}"))
                        nomes_ofs[of_possivel] = {EnumValues.DIRECAO.name: direcao_of, EnumValues.OF.name: of_possivel}
                        eh_of_mono = True
                        break

                if eh_of_mono:
                    nome_of_mono = nome_of
                else:
                    existe_of_multi = False
                    nome_of_mono = f'{EnumValues.MULTIOBJETIVO.name}[{nome_of.replace(" ", "")}]'.upper()
                    nomes_ofs[nome_of_mono] = {EnumValues.DIRECAO.name: direcao_of, EnumValues.OF.name: nome_of_mono}
                    nomes_direcoes_ofs.append(str(f"{direcao_of} {nome_of_mono}"))

                    for of_possivel in ofs_possiveis_multi:
                        if of_possivel in nome_of:
                            nomes_direcoes_ofs.append(str(f"{direcao_of} {of_possivel}"))
                            nomes_ofs[of_possivel] = {EnumValues.DIRECAO.name: direcao_of, EnumValues.OF.name: of_possivel}
                            existe_of_multi = True
                            exec(f'{of_possivel} = 2')
                    if existe_of_multi is False:
                        self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"A OF [{nome_of}] não contem OFs da lista {ofs_possiveis_multi}.")
                    try:
                        valor_funcao_of = eval(f'{nome_of}')
                    except Exception as ex:
                        self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Há um erro na funçao [{nome_of}]")

                self.set_atributo(EnumAtributo.AVALIACAO_OF_NOME_MONO, [nome_of_mono], sobrescreve=True)
                self.set_atributo(EnumAtributo.AVALIACAO_NOMES_DIRECOES_OFS, nomes_ofs, sobrescreve=True)
                self.set_atributo(EnumAtributo.AVALIACAO_DIRECAO_OF, nomes_direcoes_ofs, sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.AVALIACAO_MERO_DS_PARAMS):
            self.set_atributo(EnumAtributo.AVALIACAO_MERO_DS_PARAMS, ['-l INFO -t hpc01 -s TORQUE -p 8 -n 1 -q normal --no-wait'], sobrescreve=True)

        if not self.tem_atributo(EnumAtributo.OTIMIZACAO_MCC_ORDEM_VARIAVEL_ALEATORIA):
            self.set_atributo(EnumAtributo.OTIMIZACAO_MCC_ORDEM_VARIAVEL_ALEATORIA, [False], sobrescreve=True)
