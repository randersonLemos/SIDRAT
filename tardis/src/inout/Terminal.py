"""
:author: Rafael
:data: 19/12/2019
"""
from src.loggin.Loggin import Loggin, EnumLogStatus
import subprocess


class Terminal(Loggin):
    """
    Classe responsavel por efetuar execução de comandos no terminarl
    """

    def __init__(self):
        """
        Comentário do construtor
        """
        super().__init__()

        self._name = __name__
        """
        Variavel com o nome do arquivo
        """

    def run(self, comando: str, erro_customizado:str="") -> bool:
        """
        Executando o comando

        :param erro_customizado: Chegar se um tipo de erro especifico ocorreu, se sim para a execução
        :type erro_customizado: str
        :param str comando: String do comando a ser executado
        :return: Se tudo correu bem
        :rtype: bool
        """
        try:
            self.log(texto=f'Executando comando [{comando}].')
            self.log(texto='Aguarde enquanto o comando é finalizado...')

            popen = subprocess.Popen(comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, err = popen.communicate()
            output = f'\n{output.decode("utf-8")}'
            err = err.decode('utf-8')
            self.log(texto=output)

            if erro_customizado != "" and erro_customizado in output:
                self.log(tipo=EnumLogStatus.ERRO_FATAL, texto=f'Erro ao executando comando [{comando}].')
                return False

            if " ERROR " in output:
                self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executando comando [{comando}].')
                return False
            if err != "":
                linha_qtd = err.count('\n')
                linha_warn = err.count('Warning: NLS missing message:')
                if linha_qtd is not linha_warn:
                    self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executando comando [{comando}].')
                    return False
        except OSError as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executando comando [{comando}].', info_ex=str(ex))
            return False
        except Exception as ex:
            self.log(tipo=EnumLogStatus.ERRO, texto=f'Erro ao executando comando [{comando}].', info_ex=str(ex))
            return False
        return True

