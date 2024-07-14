# Sintonizador de Parâmetros para o Mario AI Framework
Este repositório contém um sintonizador de fases para o Mario AI Framework utilizando otimização multi-objetivo, construido com a biblioteca [Pymoo](https://pymoo.org/). 
Dois trabalhos foram realizados utilizando este sintonizador:
- [Trabalho de Conclusão de Curso](https://github.com/VitorPeixoto/ol2a2023/blob/main/Trabalho%20de%20Conclus%C3%A3o%20de%20Curso.pdf)
- [Artigo para o OL2A 2023](https://www.researchgate.net/publication/377855114_A_Multiobjective_Tuning_of_a_Procedural_Content_Generator_for_Game_Level_Design_via_Evolutionary_Algorithms)

## Os experimentos
Os experimentos consistiram em executar varios batches de otimização para cada algoritmo. Um exemplo de pseudocódigo para ilustrar o comportamento seria:
```python
algorithms = ['CTAEA', 'NSGA2']
num_batches = 30

for algorithm in algorithms:
  for batch in range(0, num_batches):
    run_optimization(algorithm, batch, ...)
```

Cada execução gera como resultado uma fronteira de pareto com os indivíduos não-dominados. Cada indivíduo consiste de seus parâmetros (x) e do resultado de suas funções-objetivo (f). Dessa forma, um experimento completo terá como resultado (num_batches*algorithms.lenght) fronteiras.
Exemplo de um indivíduo:
```python
#      [type, dif, width, height, time, st_mg, hi_mg, tu_mp, ju_mp, cn_mp],      [f1,              f2,              f3             ]
{ 'x': [2,    8,   101,   29,     280,  -1,    -1,    5,     1,     2    ], 'f': [-3.33333333e+00, -2.83933594e+02, -1.81396667e+05] }
```
Exemplo do resultado de uma execução:
```python
nsga2_frontier_exec_number_18 = [
  { 'x': [2,  8, 101, 29, 280, -1, -1, 5, 1, 2], 'f': [-3.33333333e+00, -2.83933594e+02, -1.81396667e+05] },
  { 'x': [2, 11, 103, 25, 281, -3, -2, 5, 2, 4], 'f': [-2.00000000e+00, -2.86435992e+02, -1.84533333e+05] },
  ...
]
```
Exemplo do resultado de um experimento:
```python
experiment_results = {
    'nsga2': [
      nsga2_frontier_exec_number_1,
      ...
      nsga2_frontier_exec_number_18,
      ...
    ],
    'CTAEA': [
      ctaea_frontier_exec_number_1,
      ...
    ]
}
```

## Estrutura do repositório
> [!NOTE]  
> Criei este trabalho em paralelo com outras disciplinas e com um emprego full-time, então a organização foi ficando pra depois, deixando a desejar 😅. Abaixo descrevo como foi dividido o repositório, e como utilizar.

O repositório tem a seguinte estrutura:
```
analysis/                 - Módulo de Análise: Comparativos de eficiência entre algoritmos
├─ friedmannemenyi.py     - [TCC] Testes de Friedman e Nemenyi para verificar diferença estatística significativa entre a performance dos algoritmos de otimização
articles/
├─ ol2a/                  - [OL2A] Todos os scripts utilizados no artigo do ol2a. Faltou seguir a organização do TCC.
│  ├─ outputs/            - Nesta pasta são geradas as saídas dos diversos experimentos, com a data de execução
│  ├─  ├─ out.log         - Arquivo de texto que recebe toda a saída do programa. É dele onde dá pra extrair as soluções de cada execução.
│  ├─  ├─ individuals.log - Arquivo que contém o conteúdo dos mapas gerados por cada indivíduo, para consultar ou testar no Mario AI Framework.
│  ├─ algorithms.py       - Configurações comuns entre os algoritmos (mutação, crossover, etc)
│  ├─ hypervolume.py      - Calcula o hypervolume de cada execução à partir das suas respectivas fronteiras de pareto.
│  ├─ main.py             - Execução dos experimentos. Define o tamanho, instancia o gerador, e executa em paralelo gerando checkpoints
│  ├─ NonDominated.py     - Recebe os indivíduos das fronteiras de pareto de todas as execuções, e gera uma fronteira de pareto final com todos os não-dominados.
│  ├─ mstats.py           - Gera os dados estatísticos de boxplot à da fronteira de pareto final.
│  ├─ Ol2aGenerator.py    - Classe que define o problema de otimização, e que avalia o resultado das funções objetivo de um indivíduo (executa os agentes na fase e tira a média do resultado deles).
│  ├─ plot_parameters.py  - Recebe a fronteira de pareto final e gera os gráficos utilizados no artigo.
│  ├─ wilcoxon.py         - Recebe os valores de hypervolume de cada execução, e executa o teste de Wilcoxon
generator/
├─ GeneratorProblem.py    - Utiliza a lib Jnius para instanciar as classes Java do MarioAI Framework
indicators/               - [TCC] Indicadores de hypervolume
manyobjective/            - [TCC] Definição de problema many-objective
multiobjective/           - [TCC] Definição de problema multi-objective
visualization/            - Definições de plots que são gerados durante os experimentos
```

## Dicas, pontos de atenção e melhorias necessárias
- Os resultados dos experimentos estão sendo armazenados no arquivo `out.log` em formato de texto, o que torna difícil extraí-los. Uma boa melhoria seria armazená-los em um formato de fácil leitura pelo Python, como os próprios checkpoints.
  - Enquanto não há o salvamento e leitura automática destes resultados, você pode:
    1. Usando o terminal do linux, acesse a pasta onde está o arquivo de saída.
    2. Execute o comando `cat out.log | pcregrep -M "(Non-dominated solutions \(x\):\narray\([^(]*\)|using [^\n]*\n)" > filtered_file`. Este comando irá gerar um arquivo chamado `filtered_file` contendo somente os parâmetros dos indivíduos (x). Para obter os resultados das funções objetivo, troque `\(x\)` por `\(f\)`
    3. Formate o arquivo em um editor de texto à sua escolha para colocar na estrutura necessária do Python
- Os scripts acima não estão diretamente integrados ao experimento, e precisam ser executados manualmente após o término do experimento. Uma boa melhoria seria executá-los automaticamente ao final do experimento.
- O otimizador em Python se conecta ao Mario AI Framework através do arquivo compilado `.jar `. Modifique a referência à ele no arquivo `GeneratorProblem.py`. Uma boa melhoria seria tornar esse valor parametrizável, ou relativo.
