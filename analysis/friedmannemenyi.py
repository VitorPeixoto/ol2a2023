from pprint import pprint

import numpy as np
from scipy import stats
import scikit_posthocs as sp
import matplotlib.pyplot as plt

# def calculate(hypervolumes):


hypervolumes = {'NSGA3': [5157130.129857484,
                          2744778.4986239155,
                          7552997.814104264,
                          9864225.552579697,
                          7607466.884496484,
                          5560424.142419531,
                          6156852.684424909,
                          5068343.860996801,
                          5001525.130954265,
                          5711291.518486208],
                'CTAEA': [4033543.262352362,
                          8289665.372310442,
                          7709294.669560645,
                          3585306.2404374676,
                          4354275.934349351,
                          9631847.827914892,
                          3962147.3187923688,
                          7104467.618538811,
                          3313163.1254213094,
                          1564057.4416384886],
                'RVEA': [429089.4017060971,
                         331207.98904608627,
                         564567.9749612606,
                         269942.76275334094,
                         725715.9395328824,
                         806516.2818063865,
                         216169.22265356607,
                         767985.1279437178,
                         1138507.3273177252,
                         527796.4689750206]}

for algorithm in hypervolumes.keys():
    plt.hist(hypervolumes[algorithm], alpha=0.5, label=algorithm)

plt.legend(loc='upper right')

plt.show()

plt.boxplot(hypervolumes.values(), labels=hypervolumes.keys())

plt.show()

print(stats.friedmanchisquare(*hypervolumes.values()))

data = np.array([*hypervolumes.values()])

r = sp.posthoc_nemenyi_friedman(data.T)

print(r)
