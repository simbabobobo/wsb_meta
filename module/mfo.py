import numpy as np
import random
import math
import copy
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


''' 种群初始化函数 '''

def initial(pop, dim, ub, lb):
    X = np.zeros([pop, dim])
    for i in range(pop):
        for j in range(dim):
            X[i, j] = random.random() * (ub[j] - lb[j]) + lb[j]

    return X, lb, ub


'''边界检查函数'''


def BorderCheck(X, ub, lb, pop, dim):
    for i in range(pop):
        for j in range(dim):
            if X[i, j] > ub[j]:
                X[i, j] = ub[j]
            elif X[i, j] < lb[j]:
                X[i, j] = lb[j]
    return X


'''计算适应度函数'''


def CaculateFitness(X, fun):
    pop = X.shape[0]
    fitness = np.zeros([pop, 1])
    for i in range(pop):
        fitness[i] = fun(X[i, :])
    return fitness


'''适应度排序'''


def SortFitness(Fit):
    fitness = np.sort(Fit, axis=0)
    index = np.argsort(Fit, axis=0)
    return fitness, index


'''根据适应度对位置进行排序'''


def SortPosition(X, index):
    Xnew = np.zeros(X.shape)
    for i in range(X.shape[0]):
        Xnew[i, :] = X[index[i], :]
    return Xnew



'''飞蛾扑火算法'''


def MFO(pop, dim, lb, ub, MaxIter, fun):
   
    a = 2; #参数
    X, lb, ub = initial(pop, dim, ub, lb)  # 初始化种群
    fitness = CaculateFitness(X, fun)  # 计算适应度值
    fitnessS, sortIndex = SortFitness(fitness)  # 对适应度值排序
    Xs = SortPosition(X, sortIndex)  # 种群排序
    GbestScore = copy.copy(fitnessS[0])
    GbestPositon = np.zeros([1,dim])
    GbestPositon[0,:] = copy.copy(Xs[0,:])
    Curve = np.zeros([MaxIter, 1])
    for t in range(MaxIter):

        Flame_no=round(pop-t*((pop-1)/MaxIter))
        a = -1 + t*(-1)/MaxIter # a 线性从-1降到-2
        for i in range(pop):
            for j in range(dim):
                if i<= Flame_no:
                    distance_to_flame = np.abs(Xs[i,j] - X[i,j])
                    b = 1
                    r = (a - 1)*random.random() + 1
                    
                    X[i,j] = distance_to_flame*np.exp(b*r)*np.cos(r*2*math.pi) + Xs[i,j]
                else:
                    distance_to_flame = np.abs(Xs[i,j] - X[i,j])
                    b = 1
                    r = (a - 1)*random.random() + 1
                    X[i,j] = distance_to_flame*np.exp(b*r)*np.cos(r*2*math.pi) + Xs[Flame_no,j]
                    
            
                
            
        
        X = BorderCheck(X, ub, lb, pop, dim)  # 边界检测     
        fitness = CaculateFitness(X, fun)  # 计算适应度值
        fitnessS, sortIndex = SortFitness(fitness)  # 对适应度值排序
        Xs = SortPosition(X, sortIndex)  # 种群排序
        if fitnessS[0] <= GbestScore:  # 更新全局最优
            GbestScore = copy.copy(fitnessS[0])
            GbestPositon[0,:] = copy.copy(Xs[0, :])
        Curve[t] = GbestScore
        X[-1,:] = copy.copy(GbestPositon)
        fitness = CaculateFitness(X, fun)  # 计算适应度值
        fitnessS, sortIndex = SortFitness(fitness)  # 对适应度值排序
        Xs = SortPosition(X, sortIndex)  # 种群排序
        
        
        

    return GbestScore, GbestPositon, Curve