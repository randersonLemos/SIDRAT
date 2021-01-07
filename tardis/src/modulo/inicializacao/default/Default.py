"""
:author: Rafael
:data: 10/12/2019
"""
from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.modulo.inicializacao.InicializadorPadrao import InicializadorPadrao
from src.inout.Exportacao import Exportacao
from src.inout.InOut import InOut
from src.inout.TXT import TXT
from src.loggin.Enum import EnumLogStatus
from src.modulo.EnumModulo import EnumModulo
from src.problema.Dominio import Dominio
from src.problema.EnumTipoVariaveis import EnumTipoVariaveis
from src.problema.Solucao import Solucao, Of
from src.problema.Solucoes import Solucoes
from src.problema.Variavel import Variavel


class Default(InicializadorPadrao):
    """
    Classe para inicializacao dos dados.
    """

    def __init__(self):
        super(Default, self).__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._necessidade = [EnumAtributo.INICIALIZACAO_DOMINIO] + super(Default, self).necessidade
        """
        Contem a lista de todos os atributos necessários para o módulo ser executado.
        """

        self._solucao = None
        """
        Objeto com todos os dominios
        """

    def run(self, contexto):
        """
        Executa a inicizalicao default

        :param Contexto contexto: contexto com todas as informações necessárias
        :return: Devolve o contexto atualizado
        :rtype: Contexto
        """
        super(Default, self).run(contexto)

        caminho_dominio = TXT().ajuste_path(f'{self._contexto.get_atributo(EnumAtributo.PATH_PROJETO)}/{self._contexto.get_atributo(EnumAtributo.INICIALIZACAO_DOMINIO)}')

        iteracao = 0
        identificador = 0
        self._solucao = Solucao(id=identificador, iteracao=iteracao)
        for nome_of in self._nomes_direcoes_of:
            direcao = self._nomes_direcoes_of[nome_of][EnumValues.DIRECAO.name]
            self._solucao.of = Of(nome_of, direcao=direcao)

        dominio = TXT().ler(caminho_dominio)
        for ii in range(1, len(dominio)):
            try:
                if str(dominio[ii]).strip() == "":
                    continue
                dom = self._linha_2_dominio(dominio[ii])
                self.log(texto=f'Criando variavel {dom.to_string()}')
                variavel = Variavel(dom)
                self._solucao.add_in_variaveis(variavel)
            except Exception as ex:
                self.log(tipo=EnumLogStatus.WARN, texto=f'Erro para adicionar variavel', info_ex=str(ex))

        self._contexto.set_atributo(EnumAtributo.SOLUCAO_BASE, self._solucao)

        self._contexto.set_atributo(EnumAtributo.AVALIACAO_ITERACAO_AVALIAR, [0], True)

        solucoes = Solucoes()
        solucoes.add_in_solucoes(self._solucao)
        self._contexto.set_atributo(EnumAtributo.SOLUCOES, solucoes, True)

        if self._contexto.get_atributo(EnumAtributo.INICIALIZACAO_SIMULA_BASE):

            avaliacao = self._contexto.get_modulo(EnumModulo.AVALIACAO)
            self._contexto = avaliacao.run(self._contexto)

            Exportacao().csv(self._contexto)
            Exportacao().obejto(self._contexto)

    def _linha_2_dominio(self, linha):
        """
        Converte a linha do arquivo de donimio.csv em um objto do tipo dominio

        :param linha: Linha do arquivo de problema nome, problema, default, probabilidade
        :type linha: str
        :return: retorna o objeto do dominio
        :rtype: Dominio
        """
        tipo = EnumTipoVariaveis.VARIAVEL
        linha = linha.strip()
        if len(linha.split(";")) < 2:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Dominio {linha} esta com erro.")

        if linha[0] == "#":
            tipo = EnumTipoVariaveis.CONSTANTE
            linha = linha.replace("#", "")

        args = linha.split(";")
        nome = args[0].strip()
        default = None
        niveis = None
        probabilidade = None
        equacao = None

        if '=' in linha:
            tipo = EnumTipoVariaveis.CONDICIONAL
            if len(args) > 2:
                self.log(tipo=EnumLogStatus.WARN, texto=f"Para variavel tipo condicional, são usados somentes dois parametros, nome [{args[0]}] e equacao [{args[1]}].")
            equacao = args[1].strip()
            equacao = equacao.replace("=", "").strip()
        else:
            niveis, probabilidade = self._str_2_niveis(args[1].strip())

            if len(args) > 2:
                default = InOut.ajusta_entrada(args[2].strip().replace("'", "").replace('"', ''))
                if default == "":
                    self.log(tipo=EnumLogStatus.WARN, texto=f'O valor default, não existe, com isso o default será [{niveis[0]}]')
                    default = niveis[0]
                else:
                    if default in niveis:
                        pass
                    else:
                        self.log(tipo=EnumLogStatus.WARN, texto=f'O valor default [{default}], não existe no domínio, com isso o default será [{niveis[0]}]')
                        default = niveis[0]
            if len(args) > 3:
                probabilidade = args[3].strip()
                if probabilidade == "":
                    probabilidade = None
                else:
                    probabilidade = probabilidade.replace("[", "").replace("]", "").replace(" ", "").split(",")
                    for ii in range(len(probabilidade)):
                        probabilidade[ii] = InOut.ajusta_entrada(probabilidade[ii])
            if len(niveis) != len(probabilidade):
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Quantidade de níveis [{len(niveis)}] é diferente da quantidade de probabilidades [{len(probabilidade)}].")

        return Dominio(nome, niveis, probabilidade, default, equacao, tipo)

    def _monta_niveis(self, linha, replace):
        linha = linha.strip()
        linha = linha.replace(replace, "")
        args = linha.split(";")
        if len(args) < 2:
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Dominio {linha} esta com erro.")
        nome = args[0].strip()
        default = None
        niveis, probabilidade = self._str_2_niveis(args[1].strip())

        return nome, niveis, probabilidade, default

    def _str_2_niveis(self, str_niveis: str) -> tuple:
        """
        Converte as string [ | ] ou { } exemplo [1 | 3] ou {1 2 3} em list [1, 2, 3]
        :param str_niveis: string nos formatos [ | ] ou { } exemplo [1 | 3] ou {1 2 3}
        :type str_niveis: str
        :return: list do problema
        :rtype: list
        """
        niveis = []
        probabilidade = []
        discretizacao = str_niveis

        try:
            if str_niveis.find("[") >= 0:
                str_niveis = str_niveis.replace(",", "|")
            if str_niveis.find("{") >= 0:
                str_niveis = str_niveis.replace(",", " ")

            if str_niveis.find("[") >= 0 and str_niveis.find("]") > 0 and str_niveis.find("|") > 0:
                discretizacao = discretizacao.replace("[", "")
                discretizacao = discretizacao.replace("]", "")
                discretizacao = discretizacao.strip()
                limite = discretizacao.split("|")

                for rr in range(int(InOut.ajusta_entrada(limite[0].strip())), int(InOut.ajusta_entrada(limite[1].strip())) + 1):
                    niveis.append(InOut.ajusta_entrada(str(rr)))
                    probabilidade.append(0)

            elif str_niveis.find("{") >= 0 and str_niveis.find("}") > 0:
                discretizacao = discretizacao.replace("{", "")
                discretizacao = discretizacao.replace("}", "")
                discretizacao = discretizacao.strip()
                possiveis = discretizacao.split(" ")
                for rr in range(len(possiveis)):
                    niveis.append(InOut.ajusta_entrada(possiveis[rr].strip().replace("'", "").replace('"', '')))
                    probabilidade.append(0)

            if len(niveis) > 0:
                for ii in range(len(probabilidade)):
                    probabilidade[ii] = 1 / len(probabilidade)
        except Exception as ex:
            niveis = []
            probabilidade = []
            self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f"Erro para criar problema [{str_niveis}].", info_ex=str(ex))

        return niveis, probabilidade