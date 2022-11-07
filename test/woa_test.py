from module.parse_mps import *
from module.woa import *
import os
import pandas as pd
from matplotlib import pyplot as plt



def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


def output(x, best, zeit, ori_obj, p_eq, p_ueq, change):
    base_path = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_path, 'results', 'metaheuristic.csv')
    output_path_v = os.path.join(base_path, 'results', 'meta_variable.csv')

    ori = ori_obj(x)
    eq = p_eq(x)
    ueq = p_ueq(x)

    data = [[model, algorithm, change, best, zeit, ori, eq[0], ueq[0],
             eq[1], ueq[1]]]
    data_v = x
    df = pd.DataFrame(data)
    df_v = pd.DataFrame(data_v)
    '''
    1-6 ModelName/Algorithm/Parameter/Best_obj/Variable/Time
    7-11 origin_obj/eq/ueq/eq_number/ueq_number
    '''
    df.to_csv(output_path, index=True, mode='a+', header=False)
    #df_v.to_csv(output_path_v, index=True, mode='a+', header=False)


def bild(curve, zeit):
    zeit1=str(zeit)+'seconds'
    plt.figure(algorithm)
    # 标题
    plt.semilogy(curve, 'r-', linewidth=2) # hongse shi best obj
    # 绘制y轴上具有对数缩放
    plt.xlabel('Iteration', fontsize='medium')
    plt.ylabel("Fitness", fontsize='medium')
    plt.grid()
    plt.title(zeit1, fontsize='large')
    plt.show()

"""
penalty_obj, dimensions, low, up, 
precision, ori_obj, penalty_eq_obj, penalty_ueq_obj
"""

if __name__ == "__main__":
    model = 'PyomoExample.mps'
    algorithm = 'woa'
    setting = 'test'
    input_path = read_mps(model)
    PR = parse_mps(input_path, penalty_coeff=100000)
    '''
    # PR[0]penalty_obj, PR[1]dimensions, PR[2]low, PR[3]up, PR[4]precision, 
    PR[5]ori_obj, PR[6]penalty_eq_obj, PR[7]penalty_ueq_obj
    '''
    result = WOA(func=PR[0], dim=PR[1], lb=PR[2], ub=PR[3], precision=PR[4],
              time_limit=3600,
              pop=30, MaxIter=1000)
    # 默认 pop=30, MaxIter=1000
    '''
    result[0]self.gbest_x, result[1]self.gbest_y, result[2]run_time, 
    result[3]self.curve
    '''
    # mut=0.8, crossp=0.2, popsize=200, its=100
    #print(PR[7])
    output(result[0], result[1], result[2], PR[5], PR[6], PR[7], setting)
    bild(result[3], result[2])

