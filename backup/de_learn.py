"""
Develop the DE Tool for GAMS model, which could be generated from pyomo.
"""
import numpy as np


def de(fobj, bounds, binary, mut=0.8, crossp=0.2,
       popsize=200, its=500):
    dimensions = len(bounds)
    # dimensions 为粒子大小
    pop = np.random.rand(popsize, dimensions)
    # rand用生成(0,1)间浮点数
    for seq in range(len(binary)):
        if binary[seq]:
            pop[::, seq] = np.round(pop[::, seq])
            # [::,0]是指二维列表所有子列表的第零项；将binary项对应的元素圆整
    min_b, max_b = np.asarray(bounds).T
    # .T是转置矩阵; 获取最小值最大值列表
    diff = np.fabs(min_b - max_b)
    # fabs求解x的绝对值
    pop_denorm = min_b + pop * diff
    # 根据bound范围与[0,1]的倍率，将pop扩大为pop_denorm
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    # 获得所有组元素对应的obj值；asarray用于转换列表为array；此处为一维列表
    best_idx = np.argmin(fitness)
    # 获得最小值index
    best = pop_denorm[best_idx]
    # 获得最小值index对应的元素组值
    for i in range(its):
        # its 为迭代次数
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            # 获取除当前粒子之外的所有粒子的列表
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            # 随机选三个粒子
            mutant = np.clip(a + mut * (b - c), 0, 1)
            # pop为0,1浮点数；clip用于把大于1的数削为1；把处理过的粒子保存在mutant
            for seq in range(len(binary)):
                if binary[seq]:
                    mutant[seq] = np.round(mutant[seq])

            cross_points = np.random.rand(dimensions) < crossp
            # <可以接array不能接列表；=列表<b返回T&F列表；通过与crossp比较生成粒子长度的真值表
            if not np.any(cross_points):
                # any用于任意一个元素为True输出True；挑出全是False的情况
                cross_points[np.random.randint(0, dimensions)] = True
                # randint用于返回随机整数；在粒子元素中随机选一个数设为True
            trial = np.where(cross_points, mutant, pop[j])
            # where(condi,x,y)用于满足条件condi输出x否则y；真时输出mut假时输出pop；trial试验
            trial_denorm = min_b + trial * diff
            # 进化后的元素组
            f = fobj(trial_denorm)
            # f为进化后元素组对应的目标值
            if f < fitness[j]:
                fitness[j] = f
                # 如果进化后f值小于原第j组值则保存
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
