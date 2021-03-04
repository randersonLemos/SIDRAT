from src.contexto.Contexto import Contexto
from src.contexto.EnumAtributo import EnumAtributo
from src.contexto.EnumAtributo import EnumValues
from src.modulo.ModuloPadrao import ModuloPadrao
from src.modulo.problemas_fechados.ProblemaFechadoPadrao import ProblemaFechadoPadrao
from src.modulo.problemas_fechados.campo_namorado_numero_pocos import CampoNamoradoNumeroPocos
from src.modulo.problemas_fechados.campo_namorado_posicionamento.CampoNamoradoPosicionamento import CampoNamoradoPosicionamento
from src.modulo.problemas_fechados.funcoes_teste.Clustering import Clustering
from src.modulo.problemas_fechados.funcoes_teste.Knapsack import Knapsack
from src.modulo.problemas_fechados.funcoes_teste.Rastrigin import Rastrigin
from src.modulo.problemas_fechados.funcoes_teste.Rosenbrock import Rosenbrock
from src.modulo.problemas_fechados.funcoes_teste.Sphere import Sphere


class ProblemaFechado(ModuloPadrao):
    """

    Classe destinada a gerenciar e setar arquivos quando utilizado problemas fechados
    """


    def __init__(self):
        super().__init__()

        self._name = __name__
        
        if EnumAtributo.OTIMIZACAO_TYPE not in self._necessidade:
            self._necessidade.append(EnumAtributo.OTIMIZACAO_TYPE)

        if EnumAtributo.PATH_RESULTADO not in self._necessidade:
            self._necessidade.append(EnumAtributo.PATH_RESULTADO)

        if EnumAtributo.AVALIACAO_TYPE not in self._necessidade:
            self._necessidade.append(EnumAtributo.AVALIACAO_TYPE)

        self._problema_fechado = ProblemaFechadoPadrao()


    def carrega(self, contexto):
        """
        Método para obter o modulo selecionado.

        :param Contexto contexto: contexto com todas as informações necessárias
        """
        self.log(texto=f"Carregando {self._name}")
        self._contexto = contexto

        if self._contexto.tem_atributo(EnumAtributo.AVALIACAO_TYPE):
            tipo = self._contexto.get_atributo(EnumAtributo.AVALIACAO_TYPE)
            if isinstance(tipo, str):
                tipo = tipo.upper()

            if (tipo == EnumValues.RASTRIGIN.name) or (tipo == EnumValues.RASTRIGIN):
                self.log(texto=f"O modulo de inicialização [{EnumValues.RASTRIGIN.name}] foi definido.")
                self._problema_fechado = Rastrigin()

            if (tipo == EnumValues.ROSENBROCK.name) or (tipo == EnumValues.ROSENBROCK):
                self.log(texto=f"O modulo de inicialização [{EnumValues.ROSENBROCK.name}] foi definido.")
                self._problema_fechado = Rosenbrock()

            if (tipo == EnumValues.SPHERE.name) or (tipo == EnumValues.SPHERE):
                self.log(texto=f"O modulo de inicialização [{EnumValues.SPHERE.name}] foi definido.")
                self._problema_fechado = Sphere()

            if (tipo == EnumValues.CAMPO_NAMORADO_POSICIONAMENTO.name) or (tipo == EnumValues.CAMPO_NAMORADO_POSICIONAMENTO):
                self.log(texto=f"O modulo de inicialização [{EnumValues.CAMPO_NAMORADO_POSICIONAMENTO.name}] foi definido.")
                self._problema_fechado = CampoNamoradoPosicionamento()

            if (tipo == EnumValues.KNAPSACK.name) or (tipo == EnumValues.KNAPSACK):
                self.log(texto=f"O modulo de inicialização [{EnumValues.KNAPSACK.name}] foi definido.")
                self._problema_fechado = Knapsack()

            if (tipo == EnumValues.CLUSTERING.name) or (tipo == EnumValues.CLUSTERING):
                self.log(texto=f"O modulo de inicialização [{EnumValues.CLUSTERING.name}] foi definido.")
                self._problema_fechado = Clustering()

            if (tipo == EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name) or (tipo == EnumValues.CAMPO_NAMORADO_NUMERO_POCOS):
                self.log(texto=f"O modulo de inicialização [{EnumValues.CAMPO_NAMORADO_NUMERO_POCOS.name}] foi definido.")
                self._problema_fechado = CampoNamoradoNumeroPocos()

            for necessidade in self._problema_fechado.necessidade:
                if necessidade not in self._necessidade:
                    self._necessidade.append(necessidade)


    def run(self, contexto) -> Contexto:
        """
        Executa o problema fecahdo desejado.

        :param Contexto contexto: contexto com todas as informações necessárias
        :return Contexto contexto: contexto com todas as informações necessárias
        """
        #self._name = self._problema_fechado.name

        self.log(texto=f'Executando {self._name}')

        self._contexto = contexto
 
        self._problema_fechado.run(self._contexto)

        return self._problema_fechado.contexto
