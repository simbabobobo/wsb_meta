import numpy as np
import time
import matplotlib.pyplot as plt
import math


class PSO:
    def __init__(self, ori, eq, ueq, n_dim, lb, ub, precision,
                 time_limit=3600, pop=40, max_iter=150, w=0.8, c1=0.5, c2=0.5):
        self.ori = ori
        self.eq = eq
        self.ueq = ueq
        self.w = w  # inertia
        self.cp, self.cg = c1, c2
        # parameters to control personal best, global best respectively
        self.pop = pop  # number of particles
        self.n_dim = n_dim
        # dimension of particles, which is the number of variables of func
        self.max_iter = max_iter  # max iter

        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'

        # 添加
        self.timelimit = time_limit
        self.run_time = None
        self.curve = np.zeros([max_iter, 1])
        self.precision = precision
        self.X = None
        self.V = None
        self.Y = None
        self.p_best_x = None
        self.p_best_y = None
        self.g_best_x = None
        self.g_best_y = None

    def initialization(self):
        self.X = np.random.uniform(low=self.lb, high=self.ub,
                                   size=(self.pop, self.n_dim))
        # 生成pop行 dim列的随机数组
        for seq in range(self.n_dim):
            if self.precision[seq] == 'integral':
                self.X[::, seq] = np.round(self.X[::, seq])

        v_high = self.ub - self.lb
        self.V = np.random.uniform(low=-v_high, high=v_high,
                                   size=(self.pop, self.n_dim))
        # speed of particles
        self.Y = [self.func(self.X[i]) for i in range(len(self.X))]
        # f(x) for all particles

        self.p_best_x = self.X.copy()
        # personal best location of every particle in history
        self.p_best_y = [np.inf for i in range(self.pop)]
        # best image of every particle in history
        self.g_best_x = self.p_best_x.mean(axis=0).reshape(1, -1)
        # global best location for all particles
        self.g_best_y = np.inf

    def func(self, x):
        x_constrain = np.concatenate((x, np.array([1])), axis=0)
        eq_value = np.sum(
            np.abs([np.sum(c_i * x_constrain) ** 2 for c_i in self.eq]))
        print('eq_value', eq_value)
        ueq_value = np.sum(
            np.abs(
                [max(0, np.sum(c_i * x_constrain)) for c_i in self.ueq]))
        print('ueq_value', ueq_value)
        value = np.sum(self.ori * x) + 1e5 * eq_value + 1e5 * ueq_value
        print('value', value)
        return value

    def update_p_best(self):
        """
        personal best
        :return:
        """
        for i in range(len(self.Y)):
            if self.p_best_y[i] > self.Y[i]:
                self.p_best_x[i] = self.X[i]
                self.p_best_y[i] = self.Y[i]

    def update_g_best(self):
        """
        global best
        :return:
        """
        idx_min = self.p_best_y.index(min(self.p_best_y))
        if self.g_best_y > self.p_best_y[idx_min]:
            self.g_best_x = self.X[idx_min, :].copy()
            self.g_best_y = self.p_best_y[idx_min]

    def update_v(self):
        r1 = np.random.rand(self.pop, self.n_dim)
        # 随机生成pop行dim列数组
        r2 = np.random.rand(self.pop, self.n_dim)
        self.V = self.w * self.V + self.cp * r1 * (self.p_best_x - self.X) + \
                 self.cg * r2 * (self.g_best_x - self.X)

    def update_y(self):
        for i in range(self.pop):
            self.X[i] += self.V[i]
        for seq in range(self.n_dim):
            if self.precision[seq] == 'integral':
                self.X[::, seq] = np.round(self.X[::, seq])
        self.X = np.clip(self.X, self.lb, self.ub)
        self.Y = [self.func(self.X[i]) for i in range(len(self.X))]

    # 添加
    def update_curve(self, its):
        self.curve[its] = self.g_best_y

    def run(self):
        start_time = time.time()
        self.initialization()
        for iter_no in range(self.max_iter):
            self.update_v()
            self.update_y()
            self.update_p_best()
            self.update_g_best()
            self.update_curve(iter_no)
            # self.gbest_y_hist.append(self.gbest_y)
            end_time = time.time()
            self.run_time = end_time - start_time
            if self.run_time > self.timelimit:
                # self.best_x, self.best_y = self.gbest_x, self.gbest_y
                return self.g_best_x, self.g_best_y, self.run_time, self.curve
        # self.best_x, self.best_y = self.gbest_x, self.gbest_y
        return self.g_best_x, self.g_best_y, self.run_time, self.curve

