"""
results not good enough for constrained problems
"""

from sko.GA import GA
from sko.DE import DE


def obj_func(p):
    x11, x12, x13, x21, x22, x23, x31, x32, x33, x41, x42, x43, x51, x52, \
    x53 = p
    return 4*x11+6*x12+9*x13+5*x21+4*x22+7*x23+6*x31+3*x32+4*x33+8*x41+5*x42+2*x43+10*x51+8*x52+4*x53


constraint_eq = [
    lambda x: x[0] + x[1] + x[2] - 80,
    lambda x: x[3] + x[4] + x[5] - 270,
    lambda x: x[6] + x[7] + x[8] - 250,
    lambda x: x[9] + x[10] + x[11] - 160,
    lambda x: x[12] + x[13] + x[14] - 180,
]

constraint_ueq = [
    lambda x: x[0] + x[3] + x[6] + x[9] + x[12] - 500,
    lambda x: x[1] + x[4] + x[7] + x[10] + x[13] - 500,
    lambda x: x[2] + x[5] + x[8] + x[11] + x[14] - 500,
]

# demo_func = lambda x: (x[0] - 1) ** 2 + (x[1] - 0.05) ** 2 + x[2] ** 2
# ga = DE(func=obj_func, n_dim=15, max_iter=500, lb=[0, 0, 0, 0, 0]*3,
#         ub=[500, 500, 500, 500, 500]*3)
ga = GA(func=obj_func, n_dim=15, max_iter=1000, lb=[0, 0, 0, 0, 0]*3,
        ub=[500, 500, 500, 500, 500]*3,
        precision=[1e-7, 1e-7, 1e-7, 1e-7, 1e-7]*3)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
