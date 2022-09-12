import numpy as np


def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=200, its=500):
    dimensions = len(bounds)
    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)
    # todo: this step need to be modified for integer variables
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


def original_obj(var):
    """var are the variables in a problem"""
    x1, x2, x3, x4, x5 = var
    return -(2 * x1 * x2 - 0.2 * x1 - x5)


eq_method_list = [
    lambda x: x[2] + x[3] - 1,
]

ueq_method_list = [
    lambda x: x[0] * x[1] - 2,
    lambda x: 0 - (x[0] - ((-8 * x[1]) + 9) - (-9) * (1 - x[2])),
    lambda x: x[0] - ((-8 * x[1]) + 9) - 7 * (1 - x[2]) - 0,
    lambda x: 0.2 - (x[1] - (-0.2) * (1 - x[2])),
    lambda x: x[1] - 0.05 * (1 - x[2]) - 0.95,
    lambda x: 2.5 - (x[4] - (- (1 - x[2]))),
    lambda x: x[4] - 2.5,
    lambda x: 0 - (x[0] - ((-10 * x[1]) + 15) - (-15) * (1 - x[3])),
    lambda x: x[0] - ((-10 * x[1]) + 15) - 3 * (1 - x[3]) - 0,
    lambda x: 0.7 - x[1] - (-0.69999999999999996) * (1 - x[3]),
    lambda x: x[1] - 0.010000000000000009 * (
            1 - x[3]) - 0.98999999999999999,
    lambda x: 1.5 - x[4],
    lambda x: x[4] - (1 - x[3]) - 1.5,
]


def penalty_eq_cons(var):
    """ori_obj is the original objective method, equal equation list should
    be """
    obj_func = original_obj(var)

    for eq_method in eq_method_list:
        obj_func += (max(0, abs(eq_method(var)))) ** 2

    return obj_func


def penalty_ueq_cons(var):
    obj_func = original_obj(var)

    for ueq_method in ueq_method_list:
        obj_func += (max(0, ueq_method(var))) ** 3

    return obj_func


def penalty_obj(var):
    obj_func = original_obj(var)

    for eq_method in eq_method_list:
        obj_func += (max(0, abs(eq_method(var)))) ** 2

    for ueq_method in ueq_method_list:
        obj_func += (max(0, ueq_method(var))) ** 3

    return obj_func


bounds = [(0, 8), (0, 1), (0, 1), (0, 1), (1.5, 2.5)]

# Run Differential Evolution optimization
DE = list(de(penalty_obj, bounds, mut=0.8, crossp=0.7, popsize=200, its=500))
# print(DE[-1][-1])
x = DE[-1][0]
ofunc_value = DE[-1][-1]
pen_eq= penalty_eq_cons(x)
pen_ueq = penalty_ueq_cons(x)
ori_obj = original_obj(x)

print('RESULT:')
print('Objective function value:', ofunc_value)
print('Penalty eq:', pen_eq)
print('Penalty ueq:', pen_ueq)
print('Objective function value clean:',
      ofunc_value - pen_eq - pen_ueq)
print('Objective function value clean:',
      ori_obj)
print('Variables: ', x)
