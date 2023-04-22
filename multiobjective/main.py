from pymoo.algorithms.moo.nsga2 import NSGA2
from MultiObjectiveGenerator import MultiObjectiveGenerator
from pymoo.optimize import minimize
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.util.termination.default import MultiObjectiveDefaultTermination
from pymoo.visualization.scatter import Scatter
import matplotlib.pyplot as plt
import numpy as np
import time

dimensions = [
    {"pop_size": 10, "max_evals": 100},
    {"pop_size": 25, "max_evals": 500},
    {"pop_size": 40, "max_evals": 800},
]

problem = MultiObjectiveGenerator()

mask = ['int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int']

sampling = MixedVariableSampling(mask, {
    "real": get_sampling("real_random"),
    "int": get_sampling("int_random")
})

crossover = MixedVariableCrossover(mask, {
    "real": get_crossover("real_sbx"),
    "int": get_crossover("int_sbx")
})

mutation = MixedVariableMutation(mask, {
    "real": get_mutation("real_pm"),
    "int": get_mutation("int_pm")
})


def run_dimension(dimension):
    termination = MultiObjectiveDefaultTermination(
        x_tol=1e-8,  # Tolerância da distância euclidiana das variáveis
        cv_tol=1e-6,  # Convergência de restrições.
        f_tol=0.0025,  # Valor absoluto da diferença entre melhor e pior individuo. Se menor que isso, estagnou e para.
        nth_gen=5,  # De quantas em quantas gerações são calculados os critérios de parada
        n_last=30,  # Número de gerações consideradas nos cálculos
        n_max_gen=1000000,  # Número máximo de gerações
        n_max_evals=dimension['max_evals']
        # Mais usado na literatura, numero de avaliações de fitness, "1 por individuo por geração"
    )

    algorithm = NSGA2(
        pop_size=dimension['pop_size'],
        sampling=sampling,
        crossover=crossover,
        mutation=mutation,
        eliminate_duplicates=True
    )

    print("Starting minimization with dimension " + str(dimension))
    start_time = time.time()

    res = minimize(
        problem,
        algorithm,
        termination,
        # ('n_gen', 10),
        # seed=1,
        verbose=True
    )

    print("Minimization stopped. Time elapsed: %s seconds" % (time.time() - start_time))

    print("Non-dominated solutions (x):")
    print(res.X)
    print("Non-dominated solutions (f):")
    print(res.F)

    print(problem.individuals)

    plot = Scatter(label=['f1', 'f2'], title="Soluções não-dominadas")

    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    plot.add(res.F, facecolor="none", edgecolor="red")

    plot.save('pareto_' + str(dimension['pop_size']) + "_" + str(dimension['max_evals']) + ".pdf", transparent=False,
              dpi=80, bbox_inches="tight")


for dimension in dimensions:
    run_dimension(dimension)