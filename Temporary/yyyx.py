import time
import numpy as np


def yyyx(fobj, dimensions, lb, ub, precision,
       jichenggailv = 0.5,
       tubiangailv = 0.03, popsize=200, its=100):

    start_time = time.time()
    print('YYYX Start')
    bounds = list(zip(lb, ub))

    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    for seq in range(dimensions):
        if precision[seq] == 'integral':
            pop_denorm[::, seq] = np.round(pop_denorm[::, seq])
    fitness = [[i, fobj(ind)] for ind in pop_denorm for i in pop]
    fitness.sort(key=lambda x: x[1])
    fitness = np.asarray(fitness, dtype=object)
    best_fitness = fitness[0][1]
    best_variable = fitness[0][0]
    pop = [[]]
    for i in range(its):
        for j in range(0, popsize, 2):
            father = fitness[j][0]
            mother = fitness[j + 1][0]
            childs = np.asarray([father, father, father, father])
            for k in range(4):
                cross_points = np.random.randint(low=0, high=dimensions)
                childs[k][cross_points:] = mother[cross_points:]
                if np.random.rand() < tubiangailv:
                    mut_points = np.random.randint(low=0, high=dimensions)
                    childs[k][mut_points] = np.random.rand()
                np.append(pop, childs[k])
        pop = np.random.rand(popsize, dimensions)
        min_b, max_b = np.asarray(bounds).T
        diff = np.fabs(min_b - max_b)
        pop_denorm = min_b + pop * diff
        for seq in range(dimensions):
            if precision[seq] == 'integral':
                pop_denorm[::, seq] = np.round(pop_denorm[::, seq])
        fitness = [[i, fobj(ind)] for ind in pop_denorm for i in pop]
        fitness.sort(key=lambda x: x[1])
        fitness = np.asarray(fitness, dtype=object)
        if fitness[0][1] < best_fitness:
            best_fitness = fitness[0][1]
            best_variable = fitness[0][0]
        fitness = fitness[0:popsize]

    end_time = time.time()
    zeit = end_time - start_time
    print('\nBest objective: ', best_fitness, '\nTime:', zeit,'seconds')
    print('Variable:', best_variable)

    yield best_variable, best_fitness, zeit

