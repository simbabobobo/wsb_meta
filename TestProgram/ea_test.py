from parse_mps import *
from ea import *
import os

base_path = os.path.dirname(os.path.dirname(__file__))
example_path = os.path.join(base_path, 'ModelFile', 'gen-ip054.mps')
#example_path = os.path.join(base_path,'ModelFile', 'PyomoExample.mps')
# os.path.join 将目录和文件名合成一个路径

penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj = parse_mps(example_path, eq_penalty_coeff = 3,  \
                                                            ueq_penalty_coeff = 20)

# 'mpsfile.mps'

print(example_path)
DE = list(de(penalty_obj, dimensions, lb, ub, precision, mut=0.8, crossp=0.6, popsize=200,
             its=100))
print("DE=", DE)

x = DE[0][0]
ofunc_value = DE[0][-1]

print('Objective function value:', origin_obj(x))
print('Penalty eq:', penalty_eq_obj(x))
print('Penalty ueq:', penalty_ueq_obj(x))
print('Variables: ', x)