from module.parse_mps import *
#from smps_loader import *
from module.PSO import *
import os
import pandas as pd
import time

# 开始
start_time = time.time()
# 读取文件
base_path = os.path.dirname(os.path.dirname(__file__))
modelname = 'PyomoExample.mps'
input_path = os.path.join(base_path, 'model_file_mps', modelname)
# os.path.join 将目录和文件名合成一个路径
print(input_path)

# 解析（mps）
penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj=parse_mps(input_path)

# 启发算法
algorithm = 'pso'
print('PSO Start')
pso = PSO(func=penalty_obj, n_dim=dimensions, pop=100, max_iter=1000, lb=lb, ub=ub, w=0.8, c1=0.5, c2=0.5)
result = list(pso.run())

#结束
end_time = time.time()
time = end_time - start_time

#print(result[0],result[1])

# 结果
best = result[1]
x = result[0]
zeit = time

ori = origin_obj(x)
eq = penalty_eq_obj(x)
ueq = penalty_ueq_obj(x)

# 输出结果
base_path = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(base_path, 'results', 'metaheuristic.csv')

data = [[modelname, algorithm, 'non', best, x, zeit, ori, eq[0], ueq[0], eq[1], ueq[1]]]
df = pd.DataFrame(data)
# 1-6 ModelName/Algorithm/Parameter/Best_obj/Variable/Time
# 7-11 origin_obj/eq/ueq/eq_number/ueq_number
#print(df)
#df.to_csv(output_path, index=True, mode='a+', header=False)




