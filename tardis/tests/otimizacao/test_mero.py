from tests.utilitarios.PathsFiles import PathsFiles
from src.carregamento.Carregamento import Carregamento
from src.modulo.EnumModulo import EnumModulo
from src.contexto.EnumAtributo import EnumValues, EnumAtributo
import shutil
import os
from distutils.dir_util import copy_tree


modules = ['OTIMIZACAO', 'INICIALIZACAO', 'REDUCAO', 'AVALIACAO', 'CRITERIOPARADA', 'SORTEIO', 'PROBLEMA_FECHADO']


def test_mcc():
    gera_area_avaliacao()

    carregamento = Carregamento(PathsFiles.folder_projeto_teste.value,
                                PathsFiles.file_relativo_config_funcoes_test.value, modules)
    carregamento._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TYPE, EnumValues.MCC.name, sobrescreve=True)
    carregamento._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA, EnumValues.SIMULACOES_MAX.name,
                                        sobrescreve=True)
    carregamento._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX, 30, sobrescreve=True)
    carregamento._contexto.set_atributo(EnumAtributo.AVALIACAO_TYPE, EnumValues.CAMPO_NAMORADO_POSICIONAMENTO, sobrescreve=True)

    contexto = carregamento.run()

    problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
    contexto = problema_fechado.run(contexto)

    inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
    contexto = inicializacao.run(contexto)

    otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
    contexto = otimizador.run(contexto)

    assert contexto.get_atributo(EnumAtributo.SOLUCOES).melhor_solucao().of['VPL'].valor == -1416608558.96

def test_idlhc():
    tests = []

    for i in range(2):
        gera_area_avaliacao()

        carregamento = Carregamento(PathsFiles.folder_projeto_mero.value, PathsFiles.file_relativo_config_test.value, modules)
        carregamento._contexto.set_atributo(EnumAtributo.OTIMIZACAO_TYPE, EnumValues.IDLHC, sobrescreve=True)
        carregamento._contexto.set_atributo(EnumAtributo.OTIMIZACAO_IDLHC_AMOSTRAS_PDF, 20, sobrescreve=True)
        carregamento._contexto.set_atributo(EnumAtributo.OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO, 30, sobrescreve=True)
        carregamento._contexto.set_atributo(EnumAtributo.CRITERIO_PARADA_SIMULACOES_MAX, 50, sobrescreve=True)

        contexto = carregamento.run()

        problema_fechado = contexto.get_modulo(EnumModulo.PROBLEMA_FECHADO)
        contexto = problema_fechado.run(contexto)

        inicializacao = contexto.get_modulo(EnumModulo.INICIALIZACAO)
        contexto = inicializacao.run(contexto)

        otimizador = contexto.get_modulo(EnumModulo.OTIMIZACAO)
        contexto = otimizador.run(contexto)

        ultima_iteracao = max(contexto.get_atributo(EnumAtributo.SOLUCOES).solucoes)

        solucoes_1_iteracao = contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao(1)
        solucoes_ultima_iteracao = contexto.get_atributo(EnumAtributo.SOLUCOES).get_solucoes_by_iteracao(
            ultima_iteracao)

        ofs1 = []
        for id in solucoes_1_iteracao[1]:
            ofs1.append(solucoes_1_iteracao[1][id].of['VPL'].valor)

        ofs_ultima_iteracao = []
        for id in solucoes_ultima_iteracao[ultima_iteracao]:
            ofs_ultima_iteracao.append(solucoes_ultima_iteracao[ultima_iteracao][id].of['VPL'].valor)

        tests.append(sum(ofs1) / len(ofs1) < sum(ofs_ultima_iteracao) / len(ofs_ultima_iteracao))

    assert all(tests)


def gera_area_avaliacao():
    if os.path.exists(PathsFiles.folder_area_test_mero.value):
        shutil.rmtree(PathsFiles.folder_area_test_mero.value)

    # PASSANDO ARQUIVOS DO MOCK PARA H:, PARA QUE AS SIMULACOES SEJAM FEITAS PELO TORQUE
    copy_tree(PathsFiles.folder_base_mocks.value, PathsFiles.folder_base_mero.value)
    os.mkdir(PathsFiles.folder_projeto_mero.value)
    shutil.copyfile(PathsFiles.file_config_src.value, PathsFiles.file_relativo_config_mero.value)


