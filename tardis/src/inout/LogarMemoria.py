import os
import psutil

from src.loggin.Enum import EnumLogStatus
from src.loggin.Loggin import Loggin
from src.inout.TXT import TXT
from src.contexto.EnumAtributo import EnumAtributo


def LogarMemoria(contexto):
    """
    Método que libera memória e retorna a quantidade de memória usada.
    :param contexto:
    :type contexto:
    :return: Quantidade de mem�ria usada
    :rtype: int
    """
    memoria_usada = 0
    try:
        LiberarMemoria()
        pid = os.getpid()
        p = psutil.Process(pid)
        memorias = (p.memory_info())
        memoria_usada = int(memorias.rss / 1000000)

        n_solucoes = 0
        if contexto.tem_atributo(EnumAtributo.SOLUCOES):
            solucoes = contexto.get_atributo(EnumAtributo.SOLUCOES)
            if solucoes is not None:
                for it in solucoes.solucoes:
                    n_solucoes += len(solucoes.solucoes[it])

        Loggin().log(texto=f'Quantilidade de solucao = {n_solucoes}')
        Loggin().log(texto=f'Memoria usada [{memoria_usada}Mb]')
        path_arquivo = f'{contexto.get_atributo(EnumAtributo.PATH_PROJETO)}/memoria_info.csv'

        if int(n_solucoes) == 0:
            try:
                os.remove(path_arquivo)
                Loggin().log(texto=f'Removido o arquivo {arquivo_remover}')
            except Exception as ex:
                pass
            conteudo = f'solucoes;memoria_usada[Mb];Mb/solucao\n{n_solucoes};{memoria_usada};inf\n'
            TXT().salvar(path_arquivo, conteudo, '+a')
        else:
            TXT().salvar(path_arquivo, f'{n_solucoes};{memoria_usada};{memoria_usada/(n_solucoes)}\n', '+a')
    except Exception as ex:
        Loggin().log(tipo=EnumLogStatus.WARN, texto='Erro ao logar memoria', info_ex=str(ex))
    finally:
        return memoria_usada


def LiberarMemoria():
    import gc
    gc.collect()
    del gc.garbage[:]
