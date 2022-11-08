import numpy as np
import time
import matplotlib.pyplot as plt
import math


class PSO():
    def __init__(self, func, n_dim, lb, ub, precision,
                 time_limit=3600, pop=40, max_iter=150, w=0.8, c1=0.5, c2=0.5):
        self.func = func
        self.w = w  # inertia
        self.cp, self.cg = c1, c2  # parameters to control personal best, global best respectively
        self.pop = pop  # number of particles
        self.n_dim = n_dim  # dimension of particles, which is the number of variables of func
        self.max_iter = max_iter  # max iter

        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'

        # 添加
        self.timelimit = time_limit
        self.run_time = None
        self.curve = np.zeros([max_iter, 1])
        self.precision = precision

        self.X = np.random.uniform(low=self.lb, high=self.ub, size=(self.pop, self.n_dim))
        # 生成pop行 dim列的随机数组
        for seq in range(self.n_dim):
            if self.precision[seq] == 'integral':
                self.X[::, seq] = np.round(self.X[::, seq])

        v_high = self.ub - self.lb
        self.V = np.random.uniform(low=-v_high, high=v_high, size=(self.pop, self.n_dim))  # speed of particles
        self.Y = [self.func(self.X[i]) for i in range(len(self.X))]  # y = f(x) for all particles

        self.pbest_x = self.X.copy()  # personal best location of every particle in history
        self.pbest_y = [np.inf for i in range(self.pop)]  # best image of every particle in history
        self.gbest_x = self.pbest_x.mean(axis=0).reshape(1, -1)  # global best location for all particles
        self.gbest_y = np.inf  # global best y for all particles
        # self.gbest_y_hist = []  # gbest_y of every iteration
        self.update_gbest()



    def update_pbest(self):
        '''
        personal best
        :return:
        '''
        for i in range(len(self.Y)):
            if self.pbest_y[i] > self.Y[i]:
                self.pbest_x[i] = self.X[i]
                self.pbest_y[i] = self.Y[i]

    def update_gbest(self):
        '''
        global best
        :return:
        '''
        idx_min = self.pbest_y.index(min(self.pbest_y))
        if self.gbest_y > self.pbest_y[idx_min]:
            self.gbest_x = self.X[idx_min, :].copy()
            self.gbest_y = self.pbest_y[idx_min]

    def update_V(self):
        r1 = np.random.rand(self.pop, self.n_dim)
        # 随机生成pop行dim列数组
        r2 = np.random.rand(self.pop, self.n_dim)
        self.V = self.w * self.V + self.cp * r1 * (self.pbest_x - self.X) + self.cg * r2 * (self.gbest_x - self.X)

    def update(self):
        for i in range(self.pop):
            self.X[i] += self.V[i]
        self.X = np.clip(self.X, self.lb, self.ub)
        for seq in range(self.n_dim):
            if self.precision[seq] == 'integral':
                self.X[::, seq] = np.round(self.X[::, seq])
        self.Y = [self.func(self.X[i]) for i in range(len(self.X))]

    # 添加
    def update_curve(self, its):
        self.curve[its] = self.gbest_y

    def run(self):
        start_time = time.time()
        for iter_no in range(self.max_iter):
            self.update_V()
            self.update()
            self.update_pbest()
            self.update_gbest()
            self.update_curve(iter_no)
            # self.gbest_y_hist.append(self.gbest_y)
            end_time = time.time()
            self.run_time = end_time - start_time
            if self.run_time > self.timelimit:
                # self.best_x, self.best_y = self.gbest_x, self.gbest_y
                return self.gbest_x, self.gbest_y, self.run_time, self.curve
        # self.best_x, self.best_y = self.gbest_x, self.gbest_y
        return self.gbest_x, self.gbest_y, self.run_time, self.curve

