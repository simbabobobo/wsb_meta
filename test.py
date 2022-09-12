from parse_mps import *
from smps_loader import *
from PSO import *
import os

base_path = os.path.dirname(os.path.dirname(__file__))
example_path = os.path.join('mps', 'gen-ip054.mps')
# os.path.join 将目录和文件名合成一个路径

penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj=parse_mps(example_path)

pso = PSO(func=penalty_obj, n_dim=dimensions, pop=100, max_iter=1000, lb=lb, ub=ub, w=0.8, c1=0.5, c2=0.5)
best_x, bext_y = pso.run()
print(f'{demo_func(pso.gbest_x)}\t{pso.gbest_x}')


