import numpy as np


def fobj(x):
    return 3*x[0]+4*x[1]


precision=['not', 'not']
popsize = 20
jichenggailv=0.5
tubiangailv=0.03
dimensions = 2
bounds = [[0, 10], [0, 10]]
its=1
pop = np.random.rand(popsize, dimensions)
min_b, max_b = np.asarray(bounds).T
diff = np.fabs(min_b - max_b)
pop_denorm = min_b + pop * diff
for seq in range(dimensions):
    if precision[seq] == 'integral':
        pop_denorm[::, seq] = np.round(pop_denorm[::, seq])

fitness = [[i, fobj(ind)] for ind in pop_denorm for i in pop]
fitness.sort(key=lambda x:x[1])
fitness=np.asarray(fitness,dtype=object)
best_fitness = fitness[0][1]
best_variable = fitness[0][0]
pop=[]
for i in range(its):
    for j in range(0,popsize, 2):
        father = fitness[j][0]
        mother = fitness[j+1][0]
        childs = np.asarray([father, father, father, father])
        for k in range(4):
            cross = np.random.rand(dimensions) < jichenggailv
            for l in range(dimensions):
                if cross[l]:
                    childs[k][l] = mother[l]
                mutation = np.random.rand()
                if mutation < tubiangailv:
                    childs[k][l] = np.random.rand()
            pop.append(childs[k])
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    for seq in range(dimensions):
        if precision[seq] == 'integral':
            pop_denorm[::, seq] = np.round(pop_denorm[::, seq])

    fitness = [[i, fobj(ind)] for ind in pop_denorm for i in pop]
    fitness.sort(key=lambda x: x[1])
    fitness = np.asarray(fitness,dtype=object)
    if fitness[0][1] < best_fitness:
        best_fitness = fitness[0][1]
        best_variable = fitness[0][0]
    fitness=fitness[0:popsize]
























