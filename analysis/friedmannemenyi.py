import numpy as np
from scipy import stats
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def configure_plot(title='Hipervolumes calculados para os algoritmos', xlabel='Algoritmos', ylabel='Hipervolume'):
    plt.title(title, fontsize=28)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    sns.despine()
def raincloud_plot(hypervolumes):
    plt.figure(figsize=(15, 10))
    data = []
    for algorithm in hypervolumes.keys():
        for result in hypervolumes[algorithm]:
            data.append({ 'algorithm': algorithm, 'value': result })

    df = pd.DataFrame.from_dict(data)

    # Create violin plots without mini-boxplots inside.
    ax = sns.violinplot(x='algorithm', y='value', data=df,
                        color='mediumslateblue',
                        cut=0, inner=None)
    # Clip the lower half of each violin.
    for item in ax.collections:
        x0, y0, width, height = item.get_paths()[0].get_extents().bounds
        item.set_clip_path(plt.Rectangle((x0, y0), width / 2, height,
                                         transform=ax.transData))

    # Create strip plots with partially transparent points of different colors depending on the group.
    num_items = len(ax.collections)
    sns.stripplot(x='algorithm', y='value', data=df, alpha=0.4, size=7)
    # Shift each strip plot strictly below the correponding volin.
    for item in ax.collections[num_items:]:
        item.set_offsets(item.get_offsets() + 0.15)

    # Shift each strip plot strictly below the correponding volin.
    for item in ax.collections[num_items:]:
        item.set_offsets(item.get_offsets() + 0.15)
    # Create narrow boxplots on top of the corresponding violin and strip plots, with thick lines, the mean values, without the outliers.
    sns.boxplot(y='value', x='algorithm', data=df, width=0.25,
                showfliers=False, showmeans=True,
                meanprops=dict(marker='o', markerfacecolor='darkorange',
                               markersize=10, zorder=3),
                boxprops=dict(facecolor=(0, 0, 0, 0),
                              linewidth=3, zorder=3),
                whiskerprops=dict(linewidth=3),
                capprops=dict(linewidth=3),
                medianprops=dict(linewidth=3))
    plt.legend(frameon=False, fontsize=15, loc='lower left')

    configure_plot()
    plt.show()


# hypervolumes = {'NSGA3': [5157130.129857484,
#                           2744778.4986239155,
#                           7552997.814104264,
#                           9864225.552579697,
#                           7607466.884496484,
#                           5560424.142419531,
#                           6156852.684424909,
#                           5068343.860996801,
#                           5001525.130954265,
#                           5711291.518486208],
#                 'CTAEA': [4033543.262352362,
#                           8289665.372310442,
#                           7709294.669560645,
#                           3585306.2404374676,
#                           4354275.934349351,
#                           9631847.827914892,
#                           3962147.3187923688,
#                           7104467.618538811,
#                           3313163.1254213094,
#                           1564057.4416384886],
#                 'RVEA': [429089.4017060971,
#                          331207.98904608627,
#                          564567.9749612606,
#                          269942.76275334094,
#                          725715.9395328824,
#                          806516.2818063865,
#                          216169.22265356607,
#                          767985.1279437178,
#                          1138507.3273177252,
#                          527796.4689750206]}

hypervolumes = {'NSGA3': [
             53190183485.27835,
             77676277524.21054,
            133230775135.1225,
             99662649792.63287,
             69495314714.20898,
             97196778792.88419,
            100500695622.3662,
             66206604837.65506,
            124249774796.14462,
             99615995803.21445,
            101124043758.60541,
             77606262384.4333,
             41686353018.69386,
             98385243648.21487,
            137452783316.48538,
            115363105946.35947,
             90627463586.13081,
            129736159409.37599,
            122864630281.98871,
            135046028119.76598,
            100072047805.99258,
            109954340317.44917,
            125751549551.28188,
            110292720552.80608,
            124525164335.00302,
             71009550603.04462,
             59066044231.86562,
             52782654462.61406,
             60435785442.739624,
             85683632874.55402],
 'CTAEA': [70615564386.61479,
            24038669202.756424,
            82249118076.73532,
            98666625224.2399,
            90718925394.22574,
            81073593495.79642,
            44153028819.727844,
            72763524007.84346,
            45364703250.895065,
            55852451618.39308,
            105153111406.36494,
            110900049693.73294,
            71334705903.97571,
            53948404349.83673,
            19988864257.410454,
            36981267950.073685,
            111421981586.06537,
            88928227121.67955,
            45362581826.895706,
            98982253915.59518,
            77648159485.5908,
            55509579785.94014,
            72424899782.58946,
            34431235311.938126,
            95437327416.56717,
            50450447130.690636,
            48934842367.87425,
            58953336359.4506,
            93318245764.79971,
            39358436418.2393],
 'RVEA': [62878204.231188126,
           3889875377.656712,
           894436073.3063691,
           3626633075.953395,
           642097023.7399108,
           460436078.4478649,
           2217866484.0498004,
           8616844784.564106,
           1376170807.6104264,
           8208117367.009384,
           10401683143.961958,
           3643538816.8587484,
           3181144573.3671627,
           4576727968.11132,
           7502491797.430126,
           22221066306.49041,
           1972020195.3171225,
           300997087.73158616,
           504863048.657601,
           1621966307.4648018,
           654719683.085288,
           2321121457.9648643,
           14580288301.403759,
           10405369024.756573,
           6578685656.838186,
           6286418448.141466,
           1132272709.6732874,
           7032125049.043454,
           1314841406.7807128,
           3653568663.067421]}


raincloud_plot(hypervolumes)

for algorithm in hypervolumes.keys():
    plt.hist(hypervolumes[algorithm], alpha=0.5, label=algorithm)

plt.legend(loc='upper right')

plt.show()

print(stats.friedmanchisquare(*hypervolumes.values()))

data = np.array([*hypervolumes.values()])

r = sp.posthoc_nemenyi_friedman(data.T)

print(r)
