import numpy as np
from pymoo.factory import get_problem, get_reference_directions
from pymoo.visualization.pcp import PCP
from pymoo.visualization.scatter import Scatter
from pymoo.visualization.heatmap import Heatmap
from pymoo.visualization.petal import Petal
from pymoo.visualization.radar import Radar
from math import ceil, sqrt
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def plot_solutions(problem, res, algorithm, dimension, run):
        approx_ideal = res.F.min(axis=0)
        approx_nadir = res.F.max(axis=0)
        plot = Scatter(figsize=(15,15))

        #plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
        plot.add(res.F, s=10)

        plot.save('scatter_' + algorithm.__name__ + "_" + str(dimension['pop_size']) + "_" + str(dimension['max_evals']) + "_" + str(run) + ".pdf", transparent=False,
                  dpi=80, bbox_inches="tight")

        plot = PCP(figsize=(15,15))
        plot.add(res.F)

        plot.save('pcp_' + algorithm.__name__ + "_" + str(dimension['pop_size']) + "_" + str(
            dimension['max_evals']) + "_" + str(run) + ".pdf", transparent=False,
                  dpi=80, bbox_inches="tight")

        plot = Heatmap(figsize=(15,15))
        plot.add(res.F)

        plot.save('heatmap_' + algorithm.__name__ + "_" + str(dimension['pop_size']) + "_" + str(
            dimension['max_evals']) + "_" + str(run) + ".pdf", transparent=False,
                  dpi=80, bbox_inches="tight")

        plot = Petal(bounds=(approx_ideal, approx_nadir), normalize_each_objective=True, figsize=(15,15))
        for chunk in list(chunks(res.F, ceil(sqrt(len(res.F))))):
            plot.add(chunk)

        plot.save('petal_' + algorithm.__name__ + "_" + str(dimension['pop_size']) + "_" + str(
            dimension['max_evals']) + "_" + str(run) + ".pdf", transparent=False,
                  dpi=80, bbox_inches="tight")

        plot = Radar(bounds=[approx_ideal, approx_nadir], normalize_each_objective=True, figsize=(15,15))
        for chunk in list(chunks(res.F, ceil(sqrt(len(res.F))))):
            plot.add(chunk)

        plot.save('radar_' + algorithm.__name__ + "_" + str(dimension['pop_size']) + "_" + str(
            dimension['max_evals']) + "_" + str(run) + ".pdf", transparent=False,
                  dpi=80, bbox_inches="tight")