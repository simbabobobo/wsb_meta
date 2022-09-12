# from sko.GA import GA
from sko.DE import DE


def obj_func(p):
    x1, x2, x3, x4, x5 = p
    return -(2*x1*x2 - 0.2*x1 - x5)


constraint_eq = [
    lambda x: x[2] + x[3] - 1,
]

constraint_ueq = [
    lambda x: x[0]*x[1] - 2,
    lambda x: 0 - (x[0] - ((-8*x[1]) + 9) - (-9)*(1 - x[2])),
    lambda x: x[0] - ((-8*x[1]) + 9) - 7*(1 - x[2]) - 0,
    lambda x: 0.2 - (x[1] - (-0.2)*(1 - x[2])),
    lambda x: x[1] - 0.05*(1 - x[2]) - 0.95,
    lambda x: 2.5 - (x[4] - (- (1 - x[2]))),
    lambda x: x[4] - 2.5,
    lambda x: 0 - (x[0] - ((-10*x[1]) + 15) - (-15)*(1 - x[3])),
    lambda x: x[0] - ((-10*x[1]) + 15) - 3*(1 - x[3]) - 0,
    lambda x:  0.7 - x[1] - (-0.69999999999999996)*(1 - x[3]),
    lambda x: x[1] - 0.010000000000000009*(1 - x[3]) - 0.98999999999999999,
    lambda x: 1.5 - x[4],
    lambda x: x[4] - (1 - x[3]) - 1.5,
]

# demo_func = lambda x: (x[0] - 1) ** 2 + (x[1] - 0.05) ** 2 + x[2] ** 2
ga = DE(func=obj_func, n_dim=5, max_iter=30000, lb=[0, 0, 0, 0, 1.5],
        ub=[8, 1, 1, 1, 2.5],
        precision=[1e-7, 1e-7, 1, 1, 1e-7])
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
