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



F = np.array([[ 1.00000000e+00, -1.35000000e+02, -8.72975586e+02,
        -2.63820000e+05],
       [ 0.00000000e+00, -4.70000000e+01, -6.51949219e+02,
        -2.90490000e+05],
       [ 0.00000000e+00, -1.98000000e+02, -6.32186523e+02,
        -2.49220000e+05],
       [ 0.00000000e+00, -6.40000000e+01, -3.24610962e+02,
        -2.89020000e+05],
       [ 1.00000000e+00, -6.40000000e+01, -4.40691528e+02,
        -2.89440000e+05],
       [ 0.00000000e+00, -1.40000000e+02, -1.03638379e+03,
        -2.51560000e+05],
       [ 0.00000000e+00, -1.22000000e+02, -5.80494141e+02,
        -2.67670000e+05],
       [ 2.00000000e+00, -2.13000000e+02, -4.68511719e+02,
        -2.62260000e+05]])

approx_ideal = F.min(axis=0)
approx_nadir = F.max(axis=0)

plot = Petal(bounds=(approx_ideal, approx_nadir), normalize_each_objective=True, axis_label_style={'size': 'large'}, title=["Solução %s" % (t + 1) for t in range(8)], figsize=(15,15))
for chunk in list(chunks(F, 4)):
    plot.add(chunk)

plot.show()