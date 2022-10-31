from module.parse_mps import *
from module.ea import *
import os
import pandas as pd
from matplotlib import pyplot as plt
from gurobipy import *


def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


def gurobi(in_path):
    model = read('PyomoExample.mps')
    model.optimize()
    time_grb = model.Runtime
    best_grb = model.ObjVal
    print('grb', best_grb, 'in',time_grb)
    return best_grb, time_grb,


def output(best, x, zeit, ori_obj, p_eq, p_ueq, change):
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
    # 1-6 ModelName/Algorithm/Parameter/Best_obj/Variable/Time
    # 7-11 origin_obj/eq/ueq/eq_number/ueq_number
    print(df)
    df.to_csv(output_path, index=True, mode='a+', header=False)
    #df_v.to_csv(output_path_v, index=True, mode='a+', header=False)


def bild(curve,curve_ori,zeit):
    zeit1=str(zeit)+'seconds'
    plt.figure(algorithm)
    # 标题
    plt.semilogy(curve, 'r-', linewidth=2) # hongse shi best obj
    plt.semilogy(curve_ori, 'b-', linewidth=2)
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
<<<<<<< HEAD
    model = 'markshare2.mps'
    algorithm = 'ea'
    setting = 'mut 0.1 crossp 0.9'
=======
    model = 'neos-2657525-crna.mps'
    algorithm = 'ea'
    setting = 'origin'
>>>>>>> 28769de2d1110b9e1a564f26503f18aaf2273879
    input_path = read_mps(model)
    #GR = gurobi(input_path)
    PR = parse_mps(input_path, penalty_coeff=100000)
    DE = de(PR[0], PR[5], PR[1], PR[2], PR[3], PR[4], time_limit=100,
            mutschema=3, crosschema=1, mut=0.1, mut2=0.8, crossp=0.9,
            popsize=200, its=100)
    # mut=0.8, crossp=0.2, popsize=200, its=100
    output(DE[1], DE[0], DE[2], PR[5], PR[6], PR[7], setting)
    bild(DE[3], DE[4],DE[2])










