"""
:author: Rafael
:data: 06/12/2019
"""
from enum import Enum


class EnumAtributo(Enum):
    """
    Enum com todos os atributos existentes
    """

    PATH_CONFIGURACAO = 1
    """
    Onde é o carminho do arquivo de configuracao, arquivo absoluto
    """

    PATH_PROJETO = 2
    """
    Atributo que informa o caminho absoluto do projeto
    """

    ARQUIVO_LOG = 3
    """
    Qual o caminho do arquivo de log, partindo do PATH_PROJETO
    """

    MODULE = 4
    """
    Quais são os módulos possiveis
    """

    INICIALIZACAO_TYPE = 5
    """
    Defini qual o timpo de inicializacao, 
        Values.DEFAULT => usar os valores setados com default, 
        Values.RANDOM => usar valores aleatórios dentro do intervalor, 
        Values.REESTART => ler dos arquivos de rodaddas anteriores 
    """

    PATH_LOG = 6
    """
    Caminho para o arquivo de log. Predefinido como PATH_CONFIGURACAO.log
    Nao deve ser definico no configuracao
    """

    OTIMIZACAO_TYPE = 7
    """
    Qual o algoritmo de otimizacao escolhid, tenho ate agora:
        Values.MCC
        Values.HLDG
    """

    INICIALIZACAO_DOMINIO = 8
    """
    Caminho onde esta especificado o dominio do problema
    """

    AVALIACAO_TYPE = 9
    """
    Defini qual o timpo de avaliador
        Values.MERO => envia cada solucao para o Mero para efetuar a avaliacao da OF 
    """

    SOLUCOES = 10
    """
    Contem o objeto da solucao que percorrerá todo programa
    """

    OTIMIZACAO_MCC_ORDEM_VARIAVEL_ALEATORIA = 11
    """
    Habilitar a eliminação de variaveis cujos níveis não evoluem
    """

    AVALIACAO_ITERACAO_AVALIAR = 12
    """
    É uma lista de quais serão as iterações que deveram ser avaliadas, ou seja, simuladas.
    """

    AVALIACAO_QUALIFICADOR = 13
    """
    É um texto usado para definir um qualificador para colocar nos arquivos de configuracao
    """

    PATH_SIMULACAO = 14
    """
    Caminho da pasta que esta toda simulacao
    """

    AVALIACAO_MERO_EXECUTAVEL = 15
    """
    Defini o caminho do executavel do mero
    """

    SIMULADOR_NOME = 16
    """
    Qual o simulador que será usado
    """

    SIMULADOR_VERSAO = 17
    """
    Qual será a versão do simulador
    """

    AVALIACAO_MERO_GEP_INCLUDE_PATH = 18
    """
    Atributo para definir se será adicionado um include no GEP
    """

    AVALIACAO_MERO_GEVT_TEMPLATE = 19
    """
    Caminho do arquivo de template
    """

    AVALIACAO_MERO_UNIMAP_PATH = 20
    """
    Caminho para o arquivo de UNIMAP
    """

    AVALIACAO_MERO_UNIECO_PATH = 21
    """
    Caminho para o Unieco
    """

    AVALIACAO_MERO_ECO_REFERENCE_DATE = 22
    """
    A data para inicio do calculo economico
    """

    SOLUCAO_BASE = 23
    """
    Solucao base, que contém a solucao refletida pelo arquivo de problema ou a melhor salva e recuperada
    """

    OTIMIZACAO_MCC_VARIAVEIS_ITERACAO = 24
    """
    Quantas avaliações sendo avaliadas por iteracao
    """

    PATH_RESULTADO = 25
    """
    Define nome dos arquivos de exportacao
    """

    INICIALIZACAO_RESUME_PATH = 26
    """
    Define caminho relativo ao projeto do objeto para resume
    """

    AVALIACAO_QUANTIDADE_SIMULACAO = 27
    """
    Define numero maximo de avaliacoes por otimizacao
    """

    OTIMIZACAO_IDLHC_AMOSTRAS_ITERACAO = 28
    """
    Define número de amostras utilizadas por iteração pelo metodo de otimização idlhc
    """

    CRITERIO_PARADA_ITERACOES = 29
    """
    Define número de iteracoes ate convergencia
    """

    OTIMIZACAO_IDLHC_AMOSTRAS_PDF = 30
    """
    Define número de amostras utilizadas para atualização das pdfs
    """

    CRITERIO_PARADA_VARIACAO_FO = 31
    """
    Define variacao minima esperada em porcentagem entre maximos de 3 iteracoes
    """

    OTIMIZACAO_PYMOO_POPULATON = 32
    """
    Tamanho da populacao para os algoritmos que são baseados em populacao da biblioteca pymoo
    """

    INICIALIZACAO_SIMULA_BASE = 33
    """
    Define simulacao ou nao do caso base no inicio da otimizacao
    """

    REDUCAO_DATA_INICIAL_SIMULACAO = 34
    """
    Define primeira data de simulacao
    """

    REDUCAO_GEVT_DATA_FINAL = 35
    """
    Define ultima data da simulacao com tempo otimo
    """

    REDUCAO_GEVT_DIA_FINAL = 36
    """
    Define ultimo dia da simulacao com tempo otimo
    """

    REDUCAO_GEVT_TIME_LIST = 37
    """
    Define dias de previsao com o tempo otimo
    """

    REDUCAO_QUANTIDADE_SIMULACAO_TOTAL = 38
    """
    Defini numero de amostras simuladas totais utilizadas para o estudo de reducao
    """

    REDUCAO_RANK_ANALISE = 39
    """
    Defini o numero de rank utilizado para o estudo de reducao
    """

    CRITERIO_PARADA_SIMULACOES_MAX = 41
    """
    Defini número máximo de simulações permitidas
    """

    CRITERIO_PARADA = 42
    """
    Defini o critério de parada a ser utilizado e parametro necessário para sua utilização
        SIMULACOES_MAX
        VARIACAO_OF
        ITERACOES_MAX
    """

    REDUCAO_TYPE = 43
    """
    Qual o algoritmo de reducao utilizado:
    SIMULACAO_PARCIAL
    """

    AVALIACAO_MERO_GEVTS_TEMPLATES_EXECUTAR = 44
    """
    Arquivo do gevt contendo todas as variaveis e sera o efetivamente executado
    """

    REDUCAO_MERO_GEVT_MARCAS_PATH = 45
    """
    Contem o path do arquivo gevt do mero com as marcas para o redutor
    """

    OTIMIZACAO_PSO_QTD_POPULACAO = 46
    """
    Defini o tamnho da populacao no pso
    """

    OTIMIZACAO_PSO_POPULACAO = 47
    """
    Guarda a populacao para resume
    """

    OTIMIZACAO_PSO_W = 48
    """
    Guarda a o decrescimo de w 
    """

    AVALIACAO_OF_NOME_MONO = 50
    """
    Escreve o nome da funçaõ mono objetivo, até para multi-objetivo de função 
    """

    AVALIACAO_MERO_TEMPO_MAX_SIM = 49
    """
    Define tempo em horas maximo para simulacoes na mesma iteracao
    """

    AVALIACAO_WAHOO_PATH = 51
    """
    Definir o campinho do arquivo de entrada do WAHOO
    """

    AVALIACAO_MERO_UNIECOS_EXECUTAR = 52
    """
    Arquivo do unieco para execução
    """

    SORTEIO_TYPE = 53
    """
    Define sorteio a ser usado
    HLDG -
    """

    AVALIACAO_PATH_MELHORES = 54
    """
    Define caminho relativo ao path do projeto da pasta que acumula os n melhores resultados
    """

    PATH_TESTES_UNITARIOS = 55
    """
    Define caminho em que simulacoes de testes serao feitas
    """

    AVALIACAO_MERO_FOP_MULTI_THREAD = 56
    """
    Booleano que especifica o uso de multi_thread pelo fop
    """

    AVALIACAO_MELHORES_QTD_SALVAR = 57
    """
    Define numero das melhores avaliacoes a serem salvas
    """

    AVALIACAO_MERO_DS_PARAMS = 58
    """
    Define parametros que serão utilizados pela ferramenta DS do Mero
    """

    OTIMIZACAO_MCC_ELIMINA_NIVEIS_QUANTIDADE = 100
    """
    Define a quantidade de nives que devem ser eliminados
    """

    AVALIACAO_MERO_TEMPOS_G2_PATH = 101
    """
    Caminho para o arquivo com a lista de tempos para controle de G2
    """

    OTIMIZACAO_MCC_SOLUCOES_USADAS = 102
    """
    Armazena as solucoes usadas para iniciar os caminhos
    """

    AVALIACAO_PYTHON_PATH = 202
    """
    Armazena caminho relativo ao projeto que contem o arquivo para avaliacao python
    """

    OTIMIZACAO_TABUSEARCH_TABU_LIST = 203
    """
    Armazena lista de tabu do metodo TABUSEARCH
    """

    OTIMIZACAO_TABUSEARCH_VARIAVEIS_ITERACAO = 204
    """
    Numero de variaveis alteradas entre solucoes vizinhas
    """

    OTIMIZACAO_TABUSEARCH_BESTSTRATEGY = 205
    """
    Armazena melhor estratégia da última iteracao gerada pelo metodo TABUSEARCH
    """

    OTIMIZACAO_TABUSEARCH_NUMERO_AMOSTRAS = 206
    """
    Numero de amostras utilizadas por iteração pelo metodo tabusearch
    """

    OTIMIZACAO_TABUSEARCH_TAMANHO_TABU_LIST = 207
    """
    Numero de solucoes que podem ser armazenadas na lista de tabus
    """

    OTIMIZACAO_ABC_FONTE_ALIMENTO = 103
    """
    Quantidade da fonte de alimento para as abelhas
    """

    RANDOM_SEED = 104
    """
    Semente para ser usada e todos os inicios de random
    """

    QTD_SOLUCES_AVALIADAS = 105
    """
    Quantidade de soluções que foram avaliad
    """

    AVALIACAO_MERO_MAX_OIL_PRO = 208
    """
    Utilizado para definir maxima producao de oleo, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    AVALIACAO_MERO_MAX_WATER_PRO = 209
    """
    Utilizado para definir maxima producao de agua, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    AVALIACAO_MERO_MAX_GAS_PRO = 210
    """
    Utilizado para definir maxima producao de gas, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    AVALIACAO_MERO_MAX_LIQUID_PRO = 211
    """
    Utilizado para definir maxima producao de liquido, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    AVALIACAO_MERO_MAX_WATER_INJ = 212
    """
    Utilizado para definir maxima injecao de agua, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    AVALIACAO_MERO_TOLERANCE = 213
    """
    Utilizado para definir tolerancia, quando capacidade da plataforma ser testada como variavel
    em relacao as producores maximas
    """

    SORTEIO_SOLUCOES_NOVAS = 107
    """
    Armazerna as novas solucoes do sorteio
    """

    OTIMIZACAO_IDLHC_SOLUCAO_HISTORICO = 108
    """
    Armazena as soluções de historico para efetuar a próxima atualização de probabilidade
    """

    OTIMIZACAO_ACOPLADO_OTIMIZACAO_TYPE = 109
    """
    Define quais serão os otimizadores usados e quais suas ordens
    """

    OTIMIZACAO_ACOPLADO_SIMULACOES_MAX = 110
    """
    Defini quantas avaliações terá cada ciclo
    """

    AVALIACAO_QTD_SOLUCOES_REPETIDAS = 111
    """
    Defini quantas avaliações repetidas tem na ultima avaliação
    """

    CRITERIO_PARADA_QTD_SOLUCAO_NOVA = 112
    """
    Verifica se a quantidade de nova solução para avaliar é maior que o número informado
    """

    INTERNO_CRITERIO_PARADA_QTD_SOLUCAO_NOVA = 113
    """
    Informa a quantidade de soluções novas foram avaliadas
    """

    OTIMIZACAO_PSO_ULTIMA_ITERACAO = 114
    """
    Guarda qual foi a ultima iteraco do pso
    """

    INTERNO_OTIMIZACAO_ABC_FONTE_ALIMENTO = 115
    """
    Guardar as fontes de alimento usadas no ABC
    """

    INTERNO_OTIMIZACAO_ABC_ULTIMA_ITERACAO = 116
    """
    Guardar qual foi a ultima iteracao feita pelo ABC
    """

    VISUALIZACAO_TYPE = 117
    """
    Informa qual o tipo de visualizacao desejado
    """

    AVALIACAO_MERO_LIC = 118
    """
    Informa qual o caminho da licenca para o MERO
    """

    VISUALIZACAO_COMPARACAO_BOXPLOT_AVALIACOES = 119
    """
    Informa numero de avaliacoes em que sera feita as comparacoes de boxplot
    """

    VISUALIZACAO_COMPARACAO_MAX_AVALIACOES = 120
    """
    Define o numero de avaliacoes maximas que serao considerados por estudo. O que exceder este valor sera desconsiderado
    """

    VISUALIZACAO_COMPARACAO_PATH_SAIDA = 121
    """
    Define o nome do arquivo de saida de comparacao
    """

    VISUALIZACAO_COMPARACAO_PATH_RESULTADO_NOME = 122
    """
    Informa qual o tipo de visualizacao desejado
    """

    CRITERIO_PARADA_QTD_MEMORIA_USADA_MB = 123
    """
    Defini a quantidade máxima de memória permitida para o sistema, em megabytes
    """

    AVALIACAO_NOMES_DIRECOES_OFS = 124
    """
    Informar qual o nome da of que sera usada para o processo de otimização
    """

    AVALIACAO_DIRECAO_OF = 125
    """
    Seta qual a direcao e nome da of
    """

    OTIMIZACAO_IDLHC_CORTE_PDF = 214
    """
    Define um valor mínimo de probabilidade dos níveis das variáveis. Caso seja atingido o valor definido, é forcado
    a probabilidade do nível para 0
    """
    
    FOFE = 300
    """
    Defina qual FOFE será utilizada
    """

    NN_BINARY_CLASSIFIER_NCLASS1 = 320
    """
    Número de melhores simulações consideradas como classe 1 para o treinamento
    da NN
    """

    NN_BINARY_CLASSIFIER_NMODELS = 330
    """
    Número de modelos para formação no conjunto de NNs
    """

    NN_BINARY_CLASSIFIER_THRESHOLD = 340
    """
    Limiar de probabilidade considerado para classificar uma amostra como sendo
    da classe 1
    """


class EnumValues(Enum):
    DEFAULT = 1
    """
    Usando para definir valores padroes
    """

    RANDOM = 2
    """
    Usaodo para definir valores aleatorios
    """

    RESUME = 3
    """
    Usando para definir quando executaremos um resume
    """

    MCC = 4
    """
    Metodo de otimizacao chamado metodo das coordenadas ciclicas
    """

    IDLHC = 5
    """
    Metodo de otimizacao chamado hiper cubo latino
    """

    MERO = 6
    """
    Defini o mero como valor
    """

    PYMOO_DE = 7
    """
    Especifica qual algoritimo do Pymoo será usando, nesse caso será usado o DE - Differential Evolution https://pymoo.org/algorithms/differential_evolution.html
    """

    PYMOO_GA = 8
    """
    Especifica qual algoritimo do Pymoo será usando, nesse caso será usado o GA - Genetic Algorithm https://pymoo.org/algorithms/genetic_algorithm.html
    """

    PYMOO_NSGA3 = 9
    """
    Especifica qual algoritimo do Pymoo será usando, nesse caso será usado o https://pymoo.org/algorithms/nsga2.html 
    0
Julian Blank, Kalyanmoy Deb, and Proteek Chandan Roy. Investigating the normalization procedure of NSGA-III. In Kalyanmoy Deb, Erik Goodman, Carlos A. Coello Coello, Kathrin Klamroth, Kaisa Miettinen, Sanaz Mostaghim, and Patrick Reed, editors, Evolutionary Multi-Criterion Optimization, 229–240. Cham, 2019. Springer International Publishing.
    """

    SIMULACOES_MAX = 10
    """
    Especifica o uso do criterio de parada de simulacoes maximas
    """

    VARIACAO_OF = 11
    """
    Especifica o uso do criterio de parada de variacao minima entre maximos encontrados entre 3 ultimas iteracoes
    """

    SIMULACAO_PARCIAL = 12
    """
    Especifica o uso de simulacoes parciais para reducao
    """

    TOTAL = 13
    """
    Valor total usando no qualificador
    """

    PARCIAL = 14
    """
    Valor parcial do usado no qualificador
    """

    DATA_FINAL = 15
    """
    Variavel para o gevt mero
    """

    DIA_FINAL = 16
    """
    Variavel para o gevt mero
    """

    TIME_LIST = 17
    """
    Variavel para TIME_LIST dentro do gevt
    """

    PSO = 18
    """
    Otimizado PSO
    """

    ITERACOES_MAX = 19
    """
    Especifica o uso do criterio de parada de numero maximo de iteracoes
    """

    WAHOO = 20
    """
    Definindo valor WAHOO usado para escolha do avaliador
    """

    HLDG = 21
    """
    Otimizador de HLDG
    """

    SIGMOIDE = 22
    """
    Função de gerenciamento Sigmoide
    """

    SA = 23
    """
    Defini otimizador de Simulated Annealing
    """

    TABUSEARCH = 24
    """
    Defini otimizador de TABUSEARCH
    """

    PYTHON = 25
    """
    Definindo valor PYTHON usado para escolha do avaliador
    """

    RASTRIGIN = 26
    """
    Definindo funcao de teste RASTRIGIN
    """

    ROSENBROCK = 27
    """
    Definindo funcao de teste ROSENBROCK
    """

    SPHERE = 28
    """
    Definindo funcao de teste SPHERE
    """

    CAMPO_NAMORADO_POSICIONAMENTO = 29
    """
    Definindo caixa preta do campo de namorado do posicionamento. Utiliza o avaliador MERO
    """

    ABC = 30
    """
    Defini otimizador de Artificial bee colony algorithm
    """

    MAX_OIL_PRO = 31
    """
    palavra chave para uso de discretizacao de producao de oleo da plataforma
    """

    MAX_WATER_PRO = 32
    """
    palavra chave para uso de discretizacao de producao de agua da plataforma
    """

    MAX_GAS_PRO = 33
    """
    palavra chave para uso de discretizacao de producao de gas da plataforma
    """

    MAX_LIQUID_PRO = 34
    """
    palavra chave para uso de discretizacao de producao de liquido da plataforma
    """

    MAX_WATER_INJ = 35
    """
    palavra chave para uso de discretizacao de producao de liquido da plataforma
    """

    TOLERANCE = 36
    """
    palavra chave para tolerancia na discretizacao do uso da plataforma
    """

    AVALIACAO_CAMPO_NAMORADO_POSIC_SOLUCOES = 37
    """
    Arquivo com solucoes salvas para o problema do campo namorado posicionamento
    """

    KNAPSACK = 38
    """
    Definindo funcao de teste KNAPSACK
    """

    CLUSTERING = 39
    """
    Define funcao de teste de clusterizacao
    """

    CAMPO_NAMORADO_NUMERO_POCOS = 40
    """
    Definindo caixa preta do campo de namorado do numero de pocos Utiliza o avaliador MERO
    """

    AVALIACAO_CAMPO_NAMORADO_NUM_SOLUCOES = 41
    """
    Arquivo com solucoes salvas para o problema do campo namorado numero de pocos
    """

    ACOPLADO = 42
    """
    Tipo de otimizador, onde pode ser acoplado varios otimizadores juntos
    """

    EXISTE = 43
    """
    String existe
    """

    QTD_SOLUCAO_NOVA = 44
    """
    Criterio de parada de número de novas solucoes
    """

    COMPARACAO = 45
    """
    É destinado a visualizacao de comparacao entre rodadas
    """

    EXECUCAO = 46
    """
    É destinada para a visualizacao da execução da tardis
    """

    MERO_LIC = 47
    """
    Nome da variavel de ambiente da licenca do mero
    """

    COMPUTERNAME = 48
    """
    Nome do computardor que esta sendo executado a tardis.
    """

    VPL = 49
    """
    Sigla para valor presente liquido
    """

    WP = 50
    """
    Sigla para Producao de agua (wather production)
    """

    NP = 51
    """
    Sigla para volume de óleo acumulado (cumulative oil production) """

    QTD_MEMORIA_USADA_MB = 52
    """
    Qual a quantidade máxima de memória permitida pra ser usada pela tardis
    """

    VME = 53
    """
    Sigla para maximizar o  o rosbuto de calculo economico
    """

    MAX = 58
    """
    Enum para maximizar
    """

    MIN = 59
    """
    Enum para minimizar
    """
    DIRECAO = 60
    """
    Direcao da otimizacao se é maximizacao ou minimizacao
    """

    OF = 61
    """
    Enum para referenciar funco objetivo
    """

    WI = 62
    """
    Serie de producao de injeção de agua
    """

    GI = 63
    """
    Serie de producao de injeção de gás
    """

    MULTIOBJETIVO = 64
    """
    Nome da função objetivo para o multiobjetivo
    """
    
    NN_BINARY_CLASSIFIER = 70
    """
    Nome da FOFE que utiliza um classificar binário treinado com NN para
    identificar quais solucões valem a pena serem rodadas
    """
