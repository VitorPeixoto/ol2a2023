import os
import sys
import time
from datetime import datetime
from pprint import pprint

import numpy as np
from pymoo.algorithms.moo.ctaea import CTAEA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA
from pymoo.optimize import minimize
from pymoo.util.termination.default import MultiObjectiveDefaultTermination
from pymoo.util.termination.max_eval import MaximumFunctionCallTermination

from ManyObjectiveGenerator import ManyObjectiveGenerator
from manyobjective.algorithms import params
from visualization.Plots import plot_solutions

dimensions = [
    #{"pop_size": 2, "max_evals": 10, "iterations": 2},
    #{"pop_size": 10, "max_evals": 100},
    #{"pop_size": 25, "max_evals": 500},
    {"pop_size": 20, "max_evals": 1000, "iterations": 30},
]

problem = ManyObjectiveGenerator()

outputPath = os.path.join(os.getcwd(), 'outputs')
tempPath = os.path.join(outputPath, 'temp')
os.makedirs(tempPath, exist_ok=True)

individuals = open(os.path.join(tempPath, 'individuals.log'), 'a')

def fetch_checkpoint(algorithm_type, termination, dimension, run):
    algorithm = algorithm_type(**params(dimension))
    filename = 'checkpoint_' + algorithm_type.__name__ + "_" + str(dimension['pop_size']) + "_" + str(
        dimension['max_evals']) + "_" + str(run)
    res = None
    try:
        checkpoint, = np.load(os.path.join(tempPath, filename + ".npy"), allow_pickle=True).flatten()
        print("Checkpoint found. Skipping...")
        res = minimize(
                problem,
                checkpoint,
                termination,
                copy_algorithm=False,
                verbose=True
            )

    except FileNotFoundError:
        start_time = time.time()
        res = minimize(
            problem,
            algorithm,
            termination,
            copy_algorithm=False,
            verbose=True
        )

        print("Minimization stopped. Time elapsed: %s / %s seconds" % (time.time() - start_time, res.exec_time))

        print("Non-dominated solutions (x):")
        pprint(res.X)
        print("Non-dominated solutions (f):")
        pprint(res.F)

        individuals.write("\n\nIndividuals from " + str(run) + "/10 with dimension " + str(dimension) + " using " + algorithm_type.__name__)
        individuals.write(str(problem.individuals))
        individuals.flush()

        plot_solutions(problem, res, algorithm_type, dimension, run)

        np.save(os.path.join(tempPath, filename), algorithm)

    return res

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

    for algorithm_type in [NSGA3, CTAEA, RVEA]:
        for run in range(0, dimension['iterations']):
            print("Starting minimization " + str(run) + "/" + str(dimension['iterations']) + " with dimension " + str(dimension) + " using " + algorithm_type.__name__, flush=True)

            if(algorithm_type.__name__ == "RVEA"):
                termination = MaximumFunctionCallTermination(
                    n_max_evals=dimension['max_evals']
                    # Mais usado na literatura, numero de avaliações de fitness, "1 por individuo por geração"
                )

            fetch_checkpoint(algorithm_type, termination, dimension, run)

with open(os.path.join(tempPath, 'out.log'), 'a') as sys.stdout:
    for dimension in dimensions:
        run_dimension(dimension)

individuals.close()

now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

os.rename(tempPath, os.path.join(outputPath, now))