"""
:author: Rafael
:data: 04/05/2020
"""
from src.contexto.EnumAtributo import EnumAtributo, EnumValues
from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.inout.TXT import TXT
from src.inout.CSV import CSV
from src.inout.InOut import InOut
from src.contexto.Contexto import Contexto
import numpy as np


class Gerenciamento(Loggin):
    """
    Isto é um comentário da classe MyClass
    """

    def __init__(self):
        """
        Comentário do construtor
        
        :param int var1: Isto é o valor do atributo 1
        """
        super(Gerenciamento, self).__init__()
        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

        self._funcao = EnumValues.SIGMOIDE.name
        """
        Função de ajuste do gerenciamento, atualmente só tem a sigmoide
        """

        self._BHP_Min = 190
        """
        Min BHP esta definido com 190 e em codigo
        """

        self._BHP_Max = 350
        """
        Máximo BHP esta definido em 350 e em codigo
        """

        self._tempos = None
        """
        Lista dos tempos de atuação do gerenciamento
        """

    def run(self, param_path: str, contexto: Contexto):

        if not contexto.tem_atributo(EnumAtributo.AVALIACAO_MERO_TEMPOS_G2_PATH):
            return

        self.log(texto=f'Executando o {__name__}')

        tempos_path = InOut.ajuste_path(contexto.get_atributo(EnumAtributo.AVALIACAO_MERO_TEMPOS_G2_PATH))
        tempos_path = InOut.ajuste_path(f'{contexto.get_atributo(EnumAtributo.PATH_PROJETO)}/{tempos_path}')
        self._tempos = list(((CSV()).ler(tempos_path, False)).index)
        if len(self._tempos) < 1:
            return

        count = ""
        estrutura = {}
        params = TXT().ler(param_path)

        for key in params:
            try:
                chave = key.split(" ")[0]
                valor = key.split(" ")[1]
                if (chave[0] != "#") and ("@" in chave):
                    try:
                        aux = chave.split("@")
                        local = (aux[1]).upper()
                        variavel = (aux[0]).upper()
                        evento = (aux[2]).upper()

                        if self._has_evento(evento) is None:
                            continue
                        else:
                            if not local in estrutura:
                                estrutura[local] = {}
                            if not evento in estrutura[local]:
                                estrutura[local][evento] = {}
                            estrutura[local][evento][variavel] = valor
                        count += f'{key}'
                    except Exception as ex:
                        count += f'{key}'
                        print(ex)
                else:
                    count += f'{key}'
            except Exception:
                count += f'{key}'

        count += f'***Variaveis de gerenciamento segundo formula {self._funcao}\n'
        for local in estrutura:
            for evento in estrutura[local]:
                f_tempo = self._aplicando(estrutura[local][evento])
                for tempo in f_tempo:
                    count += f'{local}@{evento}@{tempo} {f_tempo[tempo]}\n'

        TXT().salvar(param_path, count)

    def _has_evento(self, evento):

        if evento in self._eventos():
            return evento
        return None

    def _aplicando(self, variavel):
        if self._funcao.upper() == EnumValues.SIGMOIDE.name.upper():
            try:
                a = InOut.ajusta_entrada(variavel["A"])
                b = InOut.ajusta_entrada(variavel["B"])
                c = InOut.ajusta_entrada(variavel["C"])
                f_tempo = {}
                for tt in self._tempos:
                    funcao = self._BHP_Min
                    try:
                        vars = np.array([a, b, c, tt], dtype=np.float)
                        #[('divide', 'ignore'), ('invalid', 'ignore'), ('over', 'ignore'), ('under', 'ignore')]
                        with np.errstate(over='ignore', invalid='ignore', divide='ignore', under='ignore'):
                            expoente = vars[2] + vars[1] * (vars[3] / 22.762) + vars[0] * (vars[3] / 22.762) ** 2
                            funcao = np.round(self._BHP_Min + (self._BHP_Max - self._BHP_Min) / (1 + np.exp(expoente)), 0)
                    except Exception as ex:
                        self.log(tipo=EnumLogStatus.WARN, texto='Erro na criação da equacao', info_ex=str(ex))
                        funcao = self._BHP_Min
                    f_tempo[tt] = funcao

            except Exception as ex:
                self.log(tipo=EnumLogStatus.WARN, texto='Erro no método _aplicando', info_ex=str(ex))
            return f_tempo

    def _eventos(self) -> list:
        eventos = []
        eventos.append('ABANDONMENT')
        eventos.append('APPOR_METHOD')
        eventos.append('ATTACHEDTO')
        eventos.append('BLOCKS')
        eventos.append('COMPLETION')
        eventos.append('CONNECTION')
        eventos.append('CONSIDER')
        eventos.append('CONVERSION')
        eventos.append('CYCLING')
        eventos.append('DIRECTION')
        eventos.append('DRILLING')
        eventos.append('EFFICIENCY')
        eventos.append('FF')
        eventos.append('FLOWLINE')
        eventos.append('FLUID')
        eventos.append('GAS_FRAC_RECYCLE')
        eventos.append('GAS_RATE_RECYCLE')
        eventos.append('GASLIFT_LENGTH')
        eventos.append('GASLIFT_ON')
        eventos.append('GOR')
        eventos.append('IJK')
        eventos.append('INSTALL')
        eventos.append('INVESTMENT')
        eventos.append('LENGTH')
        eventos.append('LINER')
        eventos.append('MAX_BHP')
        eventos.append('MAX_GAS_INJ')
        eventos.append('MAX_GAS_PRO')
        eventos.append('MAX_LIQUID_PRO')
        eventos.append('MAX_OIL_PRO')
        eventos.append('MAX_WATER_INJ')
        eventos.append('MAX_WATER_PRO')
        eventos.append('MAX_WHP')
        eventos.append('MIN_BHP')
        eventos.append('MIN_GAS_PRO')
        eventos.append('MIN_OIL_PRO')
        eventos.append('MIN_WHP')
        eventos.append('OPEN')
        eventos.append('PRES_MAINT')
        eventos.append('PRODCOLUMN')
        return eventos
