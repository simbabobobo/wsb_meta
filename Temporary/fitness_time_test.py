import numpy as np
import time
import os
from temporary.parse_v1 import *


def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


def fitness(X, ori, eq, ueq):
    start_time = time.time()
    one = np.array([1])
    X_constrain = np.concatenate((X, one), axis=0)
    value = np.sum(ori*X)
    print('ori_value', value)
    time1 = time.time()
    eq_value = np.array(
        [np.sum(np.abs([np.sum(c_i*X_constrain)**2 for c_i in eq]))])
    time2 = time.time()
    '''
    lst=[]
    for c_i in ueq:
        temp = np.sum(c_i * X_constrain)
        temp = max(0, temp)
        lst.append(temp)
    ueq_value =np.array([np.sum(np.abs(lst))])
    '''
    ueq_value = np.array(
        [np.sum(np.abs([max(0, np.sum(c_i * X_constrain)) for c_i in ueq]))])
    #[np.sum(np.abs([np.max(0, np.sum(c_i * X_constrain)) for c_i in ueq]))])
    print('ueq_value', ueq_value)

    time3 = time.time()
    value = value + 1e5 * eq_value + 1e5 * ueq_value
    time4 = time.time()
    end_time = time.time()
    zeit = end_time - start_time
    print('计算eq值', time1-start_time)
    print('eq值求和', time2-time1 )
    print('计算ueq值', time3-time2)
    print('ueq值求和', time4-time3)
    print(zeit, 'seconds')
    print('value', value)

    return value


def generate_variable(lb, ub, dim):
    X = np.random.uniform(low=lb, high=ub, size=(dim))

    return X

if __name__ == "__main__":
    model = 'reblock115.mps'
    setting = 'test'
    input_path = read_mps(model)
    PR = parse_mps(input_path, penalty_coeff=100000)
    '''
     # PR[0]obj, PR[1]dimensions, PR[2]low, PR[3]up, PR[4]precision, 
     PR[5]eq, PR[6]ueq, PR[7],PR[8]
     obj, dimensions, low, up, precision, eq, ueq
     '''
    #print('eq is', PR[5])
    #print('ueq is', PR[8])
    var = generate_variable(PR[2], PR[3], PR[1])
    print('var', var)
    value = fitness(var, PR[0], PR[5], PR[6])
    '''fitness(X, ori, eq, ueq)'''
