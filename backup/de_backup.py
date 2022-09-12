"""
Develop the DE Tool for GAMS model, which could be generated from pyomo.
"""
import numpy as np


def de(fobj, bounds, binary, mut=0.8, crossp=0.2,
       popsize=200, its=500):
    dimensions = len(bounds)
    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)
    for seq in range(len(binary)):
        if binary[seq]:
            pop[::, seq] = np.round(pop[::, seq])
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    # scale particle positions according to bounds
    pop_denorm = min_b + pop * diff
    # initial objective function value
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    # global best particle position
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            # get indices of all particles except current
            idxs = [idx for idx in range(popsize) if idx != j]
            # randomly select 3 particles
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            # mix them into new mutant particle
            mutant = np.clip(a + mut * (b - c), 0, 1)
            for seq in range(len(binary)):
                if binary[seq]:
                    mutant[seq] = np.round(mutant[seq])
            # exchange some coordinates between mutant and current particle
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            # scale new trial particle to bounds
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]


def de_backup(fobj, bounds, binary, mut=0.8, crossp=0.2,
        popsize=200, its=500):
    # coeff = 3

    # for eq_method in eq_list:
    #     fobj += coeff * (max(0, abs(eq_method(var)))) ** 2
    #
    # for ueq_method in ueq_list:
    #     fobj += coeff * (max(0, ueq_method(var))) ** 3

    dimensions = len(bounds)
    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)
    for seq in range(len(binary)):
        if binary[seq]:
            pop[::, seq] = np.round(pop[::, seq])
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    # scale particle positions according to bounds
    pop_denorm = min_b + pop * diff
    # initial objective function value
    # fitness = np.asarray([fobj(ind) for ind in pop_denorm]) + np.asarray([(coeff * (max(0, abs(eq(ind)))) ** 2 for eq in eq_list) for
    #            ind in pop_denorm]) + np.asarray([(coeff * (max(0, ueq(ind))) ** 3 for ueq in
    #                        ueq_list) for ind in pop_denorm])
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    # for eq in eq_list:
    #     for ind in pop_denorm:
    #         fitness += coeff * (max(0, abs(eq(ind)))) ** 2
    # for ueq in ueq_list:
    #     for ind in pop_denorm:
    #         fitness += coeff * (max(0, ueq(ind))) ** 3
    # print(fitness)
    # fitness = np.asarray([fobj(ind) +
    #                       (coeff * (max(0, abs(eq(ind)))) **
    #                        2 for eq in eq_list) +
    #                       (coeff * (max(0, ueq(ind))) ** 3 for ueq in ueq_list)
    #                       for ind in pop_denorm])

    # global best particle position
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            # get indices of all particles except current
            idxs = [idx for idx in range(popsize) if idx != j]
            # randomly select 3 particles
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            # mix them into new mutant particle
            mutant = np.clip(a + mut * (b - c), 0, 1)
            for seq in range(len(binary)):
                if binary[seq]:
                    mutant[seq] = np.round(mutant[seq])
            # mutant[2] = np.round(mutant[2])
            # mutant[3] = np.round(mutant[3])
            # exchange some coordinates between mutant and current particle
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            # scale new trial particle to bounds
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            # for eq in eq_list:
            #     f += coeff * (max(0, abs(eq(trial_denorm)))) ** 2
            # for ueq in ueq_list:
            #     f += coeff * (max(0, ueq(trial_denorm))) ** 3
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]


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
