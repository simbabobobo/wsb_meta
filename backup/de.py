"""
Develop the DE Tool for GAMS model, which could be generated from pyomo.
"""
import numpy as np
import time


def de(fobj, bounds, integer, mutschema=1, crosschema=1, mut=0.8, mut2=0.8,
       crossp=0.2, popsize=200, its=500):

    start_time = time.time()

    dimensions = len(bounds)
    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)
    for seq in range(len(integer)):
        if integer[seq]:
            pop[::, seq] = np.round(pop[::, seq])
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    # scale particle positions according to bounds
    pop_denorm = min_b + pop * diff
    # initial objective function value
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    # global best particle position
    best_idx = np.argmin(fitness)
    best_variable = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            # get indices of all particles except current
            idxs = [idx for idx in range(popsize) if idx != j]
            # randomly select 3 particles
            mutant=[]
            if mutschema == 1:
                a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + mut * (b - c), 0, 1)
                # Rand/1
            if mutschema == 2:
                a, b, c, d, e = pop[np.random.choice(idxs, 5, replace=False)]
                mutant = np.clip(a + mut * (b - c +d -e), 0, 1)
                # Rand/2
            if mutschema == 3:
                b, c = pop[np.random.choice(idxs, 2, replace=False)]
                mutant = np.clip(pop[best_idx] + mut * (b - c), 0, 1)
                # Best/1
            if mutschema == 4:
                b, c, d, e = pop[np.random.choice(idxs, 4, replace=False)]
                mutant = np.clip(pop[best_idx] + mut * (b - c + d - e), 0, 1)
                # Best/2
            if mutschema == 5:
                a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + mut * (b - c) +mut2 * (pop[best_idx] - a),
                                 0, 1)
                # Rand-to-best/1
            for seq in range(len(integer)):
                if integer[seq]:
                    mutant[seq] = np.round(mutant[seq])
            # exchange some coordinates between mutant and current particle
            trial = []
            if crosschema == 1:
                cross_points = np.random.rand(dimensions) < crossp
                if not np.any(cross_points):
                    cross_points[np.random.randint(0, dimensions)] = True
                trial = np.where(cross_points, mutant, pop[j])
                # Binomial (bin)
                # scale new trial particle to bounds
            if crosschema == 2:
                cross_points = np.random.rand(dimensions) < (dimensions + 1)
                location = np.sort(np.random.randint(dimensions, size=2))
                cross_points[location[0]:location[1]] = False
                trial = np.where(cross_points, mutant, pop[j])
                # Exponential (exp)
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
    best_value = fitness[best_idx]
    end_time = time.time()
    zeit = 0
    zeit = end_time - start_time
    print('Best objective ', best_value,'in', zeit,'seconds')

    yield best_variable, best_value


def add_penalty(orig_obj, eq_method_list, ueq_method_list):
    def penalty_obj(var):
        obj_func = orig_obj(var)

        eq_penalty_coeff = 3
        ueq_penalty_coeff = 20

        for eq_nr in range(len(eq_method_list)):
            equation = eq_method_list[eq_nr]
            eq_method = lambda x: eval(equation)
            obj_func += eq_penalty_coeff * (max(0, abs(eq_method(var)))) ** 2

        for ueq_nr in range(len(ueq_method_list)):
            equation = ueq_method_list[ueq_nr]
            ueq_method = lambda x: eval(equation)
            obj_func += ueq_penalty_coeff * (max(0, ueq_method(var))) ** 3

        return obj_func

    return penalty_obj
