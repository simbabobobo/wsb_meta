from module.parse_mps import *
from module.ea_new import *
import os
import pandas as pd
from matplotlib import pyplot as plt

# 读取文件
base_path = os.path.dirname(os.path.dirname(__file__))
# example_path = os.path.join(base_path, 'ModelFile', 'gen-ip054.mps')
modelname = 'p0201.mps'
input_path = os.path.join(base_path, 'model_file_mps', modelname)
# os.path.join 将目录和文件名合成一个路径
print(input_path)

# 解析（mps）
penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj = parse_mps(input_path, eq_penalty_coeff = 3,  \
                                                            ueq_penalty_coeff = 20)

# 启发算法
algorithm = 'ea'
DE = list(de(penalty_obj, origin_obj, dimensions, lb, ub, precision, mut=0.6,
             crossp=0.6,
             popsize=200,
             its=100))
# mut=0.8, crossp=0.6, popsize=200, its=100
# 结束

# 结果
best = DE[0][1]
x = DE[0][0]
zeit = DE[0][2]
curve = DE[0][3]
curve_ori = DE[0][4]

ori = origin_obj(x)
eq = penalty_eq_obj(x)
ueq = penalty_ueq_obj(x)

# 输出结果
output_path = os.path.join(base_path, 'Result', 'metaheuristic.csv')
output_path_v = os.path.join(base_path, 'Result', 'meta_variable.csv')

data = [[modelname, algorithm, 'mut=0.6', best, x, zeit, ori, eq[0], ueq[0],
         eq[1], ueq[1]]]
df = pd.DataFrame(data)
# 1-6 ModelName/Algorithm/Parameter/Best_obj/Variable/Time
# 7-11 origin_obj/eq/ueq/eq_number/ueq_number
print(df)
#df.to_csv(output_path, index=True, mode='a+', header=False)

plt.figure(algorithm)
# 标题
plt.semilogy(curve, 'r-', linewidth=2)
plt.semilogy(curve_ori, 'b-', linewidth=2)
# 绘制y轴上具有对数缩放
plt.xlabel('Iteration', fontsize='medium')
plt.ylabel("Fitness", fontsize='medium')
plt.grid()
plt.title(algorithm, fontsize='large')
plt.show()
