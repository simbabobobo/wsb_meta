from backup.parse_mps import *
import os
import pandas as pd
from matplotlib import pyplot as plt
import module.mfo as MFO
import time

# 开始
start_time = time.time()

# 读取文件
base_path = os.path.dirname(os.path.dirname(__file__))
modelname = 'p0201.mps'
input_path = os.path.join(base_path, 'model_file_mps', modelname)
# os.path.join 将目录和文件名合成一个路径
print(input_path)

# 解析（mps）
penalty_obj, dimensions, lb, ub, precision, origin_obj, penalty_eq_obj, \
penalty_ueq_obj = parse_mps(input_path, eq_penalty_coeff = 3,  \
                                                            ueq_penalty_coeff = 20)

# 启发算法
algorithm = 'mfo'
#设置参数
pop = 30 #种群数量
MaxIter = 1000 #最大迭代次数

result = MFO.MFO(pop, dimensions, lb, ub, MaxIter, penalty_obj)

#结束
end_time = time.time()
time = end_time - start_time

# 结果
best = result[0][0]
x = result[1][0]
zeit = time
Curve = result[2]

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
df.to_csv(output_path, index=True, mode='a+', header=False)


plt.figure(1)
plt.semilogy(Curve,'r-',linewidth=2)
plt.xlabel('Iteration',fontsize='medium')
plt.ylabel("Fitness",fontsize='medium')
plt.grid()
plt.title('WOA',fontsize='large')
#plt.show()