import numpy as np
import time


class GA:
    def __init__(self, ori, eq, ueq, n_dim, lb, ub, precision, time_limit=3600,
                 size_pop=50, max_iter=200, prob_mut=0.001,
                 prob_cros=0.9):

        self.ori = ori
        self.eq = eq
        self.ueq = ueq
        assert size_pop % 2 == 0, 'size_pop must be even integer'
        self.size_pop = size_pop  # size of population
        self.max_iter = max_iter
        self.prob_mut = prob_mut  # probability of mutation
        self.n_dim = n_dim
        # self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub)
        # * np.ones(self.n_dim)
        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(
            ub) * np.ones(self.n_dim)
        self.prob_cros = prob_cros

        self.Chrom = None
        self.X = None  # shape = (size_pop, n_dim)
        self.Y_raw = None  # shape = (size_pop,) , value is f(x)
        self.Y = None  # shape = (size_pop,) , value is f(x) + penalty for constraint
        self.FitV = None  # shape = (size_pop,)

        # self.FitV_history = []
        self.generation_best_X = []
        self.generation_best_Y = []

        self.all_history_Y = []
        self.all_history_FitV = []

        self.best_x, self.best_y = None, None

        self.timelimit = time_limit
        self.run_time = None
        self.curve = np.zeros([max_iter, 1])
        self.precision = precision

    def crtbp(self):
        # create the population, random floating point numbers of 0 ~ 1
        self.Chrom = np.random.random([self.size_pop, self.n_dim])
        return self.Chrom

    def chrom2x(self):
        self.X = self.lb + (self.ub - self.lb) * self.Chrom
        for seq in range(self.n_dim):
            if self.precision[seq] == 'integral':
                self.X[::, seq] = np.round(self.X[::, seq])

        return self.X

    def crossover(self):
        """
        simulated binary crossover
        :param self:
        :return self.Chrom:
        """
        Chrom, size_pop, len_chrom, Y = self.Chrom, self.size_pop, len(self.Chrom[0]), self.FitV
        for i in range(0, size_pop, 2):

            if np.random.random() > self.prob_cros:
                continue
            for j in range(len_chrom):

                ylow = 0
                yup = 1
                y1 = Chrom[i][j]
                y2 = Chrom[i + 1][j]
                r = np.random.random()
                if r <= 0.5:
                    betaq = (2 * r) ** (1.0 / (1 + 1.0))
                else:
                    betaq = (0.5 / (1.0 - r)) ** (1.0 / (1 + 1.0))

                child1 = 0.5 * ((1 + betaq) * y1 + (1 - betaq) * y2)
                child2 = 0.5 * ((1 - betaq) * y1 + (1 + betaq) * y2)


                child1 = min(max(child1, ylow), yup)
                child2 = min(max(child2, ylow), yup)

                self.Chrom[i][j] = child1
                self.Chrom[i + 1][j] = child2
        return self.Chrom

    def mutation(self):
        '''
        Routine for real polynomial mutation of an individual
        mutation of 0/1 type chromosome
        :param self:
        :return:
        '''
        #
        size_pop, n_dim, Chrom = self.size_pop, self.n_dim, self.Chrom
        for i in range(size_pop):
            for j in range(n_dim):
                r = np.random.random()
                if r <= self.prob_mut:
                    y = Chrom[i][j]
                    ylow = 0
                    yup = 1
                    delta1 = 1.0 * (y - ylow) / (yup - ylow)
                    delta2 = 1.0 * (yup - y) / (yup - ylow)
                    r = np.random.random()
                    mut_pow = 1.0 / (1 + 1.0)
                    if r <= 0.5:
                        xy = 1.0 - delta1
                        val = 2.0 * r + (1.0 - 2.0 * r) * (xy ** (1 + 1.0))
                        deltaq = val ** mut_pow - 1.0
                    else:
                        xy = 1.0 - delta2
                        val = 2.0 * (1.0 - r) + 2.0 * (r - 0.5) * (xy ** (1 + 1.0))
                        deltaq = 1.0 - val ** mut_pow
                    y = y + deltaq * (yup - ylow)
                    y = min(yup, max(y, ylow))
                    self.Chrom[i][j] = y
        return self.Chrom

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

    def x2y(self):
        #self.Y = self.func(self.X)
        self.Y = [self.func(self.X[i]) for i in range(len(self.X))]

        return np.array(self.Y)

    def ranking(self):
        # GA select the biggest one, but we want to minimize func, so we put a negative here
        self.FitV = -self.Y

    def selection(self, tourn_size=3):
        '''
        Select the best individual among *tournsize* randomly chosen
        Same with `selection_tournament` but much faster using numpy
        individuals,
        :param self:
        :param tourn_size:
        :return:
        '''
        aspirants_idx = np.random.randint(self.size_pop,
                                          size=(self.size_pop, tourn_size))
        aspirants_values = self.FitV[aspirants_idx]
        winner = aspirants_values.argmax(axis=1)  # winner index in every team
        sel_index = [aspirants_idx[i, j] for i, j in enumerate(winner)]
        self.Chrom = self.Chrom[sel_index, :]

        return self.Chrom

    def update_curve(self, its):
        self.curve[its] = self.best_y

    def run(self, max_iter=None):
        start_time = time.time()
        self.max_iter = max_iter or self.max_iter
        self.crtbp()
        for i in range(self.max_iter):
            self.X = self.chrom2x()
            self.Y = self.x2y()
            self.ranking()
            self.selection()
            self.crossover()
            self.mutation()

            # record the best ones
            generation_best_index = self.FitV.argmax()
            self.generation_best_X.append(self.X[generation_best_index, :])
            self.generation_best_Y.append(self.Y[generation_best_index])
            self.all_history_Y.append(self.Y)
            self.all_history_FitV.append(self.FitV)
            global_best_index = np.array(self.generation_best_Y).argmin()
            self.best_x = self.generation_best_X[global_best_index]
            self.best_y = self.func(np.array(self.best_x))
            self.update_curve(i)
            end_time = time.time()
            self.run_time = end_time - start_time
            if self.run_time > self.timelimit:
                # self.best_x, self.best_y = self.gbest_x, self.gbest_y
                return self.best_x, self.best_y, self.run_time, self.curve

        return self.best_x, self.best_y, self.run_time, self.curve













