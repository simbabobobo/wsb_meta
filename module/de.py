"""
Develop the DE Tool
"""
import numpy as np
import time




def de(ori, eq, ueq, dimensions, lb, ub, precision, time_limit=3600,
       mutschema=3,
       crosschema=1,
       mut=0.8,
       mut2=0.8,
       crossp=0.2, popsize=200, its=500):

    def fitnessfunc(X):
        value = ori(X)
        eq_value = []
        ueq_value = []
        for i in eq:
            eq_i = lambda x: eval(i)
            eq_value.append(eq_i(X))
        eq_value = np.array(eq_value)
        penalty_eq = np.array([np.sum((np.abs(eq_value)) ** 2)])
        for i in ueq:
            ueq_i = lambda x: eval(i)
            ueq_value.append(max(0, ueq_i(X)))
        ueq_value = np.array(ueq_value)
        penalty_ueq = np.array([np.sum(ueq_value)])
        value = value + 1e5 * penalty_eq + 1e5 * penalty_ueq

        return value

    start_time = time.time()
    print('EA Start')
    bounds = list(zip(lb, ub))
    t=1
    typ = 1

    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)

    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    # scale particle positions according to bounds
    pop_denorm = min_b + pop * diff
    # initial objective function value
    for seq in range(dimensions):
        if precision[seq] == 'integral':
            pop_denorm[::, seq] = np.round(pop_denorm[::, seq])
    #fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    fitness = np.asarray([fitnessfunc(ind) for ind in pop_denorm])
    # global best particle position
    best_idx = np.argmin(fitness)
    best_variable = pop_denorm[best_idx]
    best_value = 0
    zeit = 0
    zwischen_time = time.time()
    zeit_1 = zwischen_time - start_time
    curve = np.zeros([its, 1])
    curve_ori = np.zeros([its, 1])
    if zeit_1 > time_limit:
        return best_variable, best_value, zeit_1, curve, curve_ori
    for i in range(its):
        print('its is', t)
        t += 1
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
            for seq in range(len(precision)):
                if precision[seq] == 'integral':
                    mutant[seq] = np.round(mutant[seq])
            # exchange some coordinates between mutant and current particle
            trial = []
            if crosschema == 1:
                cross_points = np.random.rand(dimensions) < crossp
                # generate random number if < crossp: it is True else Flase
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
            #f = fobj(trial_denorm)
            f = fitnessfunc(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best_variable = trial_denorm
        curve[i] = fitness[best_idx]
        curve_ori[i] = ori(best_variable)
        best_value = fitness[best_idx]
        end_time = time.time()
        zeit = end_time - start_time
        if zeit > time_limit:
            return best_variable, best_value, zeit, curve, curve_ori
        #if best_value < best_grb:
            #return best_variable, best_value, zeit, curve, curve_ori

    #best_value = fitness[best_idx]
    #end_time = time.time()
    #zeit = end_time - start_time
    #print('\nBest objective: ', best_value,'\nTime:', zeit,'seconds')
    #print('Variable:', best_variable)

    #yield best_variable, best_value, zeit, curve, curve_ori
    return best_variable, best_value, zeit, curve, curve_ori


