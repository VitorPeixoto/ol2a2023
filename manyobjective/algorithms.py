from pymoo.factory import get_sampling, get_crossover, get_mutation, get_reference_directions
from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover

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


def params(dimension):
    ref_dirs = get_reference_directions("energy", 4, dimension['pop_size'])
    return {
        'ref_dirs': ref_dirs,
        #'pop_size': dimension['pop_size'], Does not work with CTAEA. Also, pop_size will be equal to len(ref_dirs) on both algorithms
        'sampling': sampling,
        'crossover': crossover,
        'mutation': mutation,
        'eliminate_duplicates': True,
    }
