import sys
import time

from pymoo.algorithms.moo.ctaea import CTAEA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_reference_directions
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover
from pymoo.optimize import minimize
from pymoo.util.termination.default import MultiObjectiveDefaultTermination
from pymoo.util.termination.max_eval import MaximumFunctionCallTermination
from pymoo.visualization.scatter import Scatter
from ManyObjectiveGenerator import ManyObjectiveGenerator
from manyobjective.algorithms import params
from visualization.Plots import plot_solutions
from random import randrange

dimensions = [
    {"pop_size": 10, "max_evals": 100},
    {"pop_size": 25, "max_evals": 500},
    {"pop_size": 40, "max_evals": 800},
]

problem = ManyObjectiveGenerator()

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

    for algorithm in [NSGA3, CTAEA, RVEA]:
        #seed = 1 + randrange(2**32 - 1)
        for run in range(0, 10):
            print("Starting minimization " + str(run) + "/10 with dimension " + str(dimension) + " using " + algorithm.__name__)
            start_time = time.time()

            if(algorithm.__name__ == "RVEA"):
                termination = MaximumFunctionCallTermination(
                    n_max_evals=dimension['max_evals']
                    # Mais usado na literatura, numero de avaliações de fitness, "1 por individuo por geração"
                )

            res = minimize(
                problem,
                algorithm(**params(dimension)),
                termination,
                verbose=True
                #seed=seed
            )

            print("Minimization stopped. Time elapsed: %s seconds" % (time.time() - start_time))

            print("Non-dominated solutions (x):")
            print(res.X)
            print("Non-dominated solutions (f):")
            print(res.F)

            print(problem.individuals)

            plot_solutions(problem, res, algorithm, dimension, run)

#now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#outputPath = os.path.join(os.getcwd(), 'outputs', now)

#os.makedirs(outputPath)

#with open(outFilePath, 'w') as sys.stdout:
for dimension in dimensions:
    run_dimension(dimension)