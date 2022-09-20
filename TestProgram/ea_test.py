from parse_mps import *
from ea import *
import os
import pandas as pd

base_path = os.path.dirname(os.path.dirname(__file__))
# example_path = os.path.join(base_path, 'ModelFile', 'gen-ip054.mps')
modelname = 'PyomoExample.mps'
input_path = os.path.join(base_path,'ModelFile', modelname)
# os.path.join 将目录和文件名合成一个路径
print(input_path)

penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj = parse_mps(input_path, eq_penalty_coeff = 3,  \
                                                            ueq_penalty_coeff = 20)
# 'mpsfile.mps'

DE = list(de(penalty_obj, dimensions, lb, ub, precision, mut=0.8, crossp=0.6, popsize=200,
             its=100))
#print("DE=", DE)

best = DE[0][1]
x = DE[0][0]
zeit=DE[0][2]

ori = origin_obj(x)
eq = penalty_eq_obj(x)
ueq = penalty_ueq_obj(x)


base_path = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(base_path, 'Result', 'metaheuristic.csv')

data = [[modelname, 'ea', 'non', best, x, zeit, ori, eq[0], ueq[0], eq[1], ueq[1]]]
df = pd.DataFrame(data)
# 1-6 ModelName/Algorithm/Parameter/Best_obj/Variable/Time
# 7-11 origin_obj/eq/ueq/eq_number/ueq_number
#print(df)

df.to_csv(output_path, index=True, mode='a+', header=False)
