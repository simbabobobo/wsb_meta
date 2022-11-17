from module.parser_mps import *
from module.pso import *
import os
import pandas as pd
from matplotlib import pyplot as plt


def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


def output(x, best, zeit, ori_func, p_eq, p_ueq, setting_, curve):
    base_path = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_path, 'results', 'metaheuristic.csv')
    output_path_v = os.path.join(base_path, 'results', 'meta_variable.csv')

    ori = ori_func(x)
    eq = p_eq(x)
    ueq = p_ueq(x)
    break_value = [eq[0], eq[1], ueq[0], ueq[1]]

    data = [[model, algorithm, setting_, best, zeit,
             ori, break_value, x, curve]]
    data_v = x
    df = pd.DataFrame(data)
    df_v = pd.DataFrame(data_v)
    '''
    1-5 ModelName/Algorithm/Setting/Best_obj/Time/
    6-10 Origin/Break/Variable/Cruve
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
    model = 'markshare_4_0.mps'
    algorithm = 'pso'
    setting = 'test'
    input_path = read_mps(model)
    PR = parse_mps(input_path, penalty_coeff=100000)
    '''
    # PR[0]ori, PR[1]eq, PR[2]ueq, PR[3]dimensions, PR[4]low, 
    PR[5]up, PR[6]precision, PR[7]ori_func, PR[8]p_eq_func, PR[9]p_ueq_func
    ori, eq, ueq, \
           dimensions, low, up, precision, \
           ori_func, p_eq_func, p_ueq_func
    '''
    for i in range(1):
        pso = PSO(PR[0], PR[1], PR[2], PR[3], PR[4], PR[5], PR[6],
                  time_limit=3600,
                  pop=200, max_iter=100, w=0.8, c1=0.5, c2=0.5, p_typ='s')
        # 默认 pop=40, max_iter=150, w=0.8, c1=0.5, c2=0.5
        result = pso.run()
        '''
            result[0]self.gbest_x, result[1]self.gbest_y, result[2]run_time, 
            result[3]self.curve
            '''
        # mut=0.8, crossp=0.2, popsize=200, its=100
        # print(PR[7])
        output(result[0], result[1], result[2],
               PR[7], PR[8], PR[9],
               result[4], result[3])
        """
        x, best, zeit, ori_func, p_eq, p_ueq, setting_, curve
        """
        bild(result[3], result[2])







