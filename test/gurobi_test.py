#from module.grb import *
import os
import pandas as pd
from gurobipy import *

def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


#Parameter=[['Method', 0.0], ['Method', 1.0], ['Method', 2.0], ['BranchDir', -1.0], ['BranchDir', 1.0], ['Heuristics', 0.0], ['Heuristics', 0.1], ['Heuristics', 0.3], ['Heuristics', 0.5], ['Heuristics', 0.7], ['Heuristics', 1.0], ['MIPFocus', 1.0], ['MIPFocus', 2.0], ['MIPFocus', 3.0], ['VarBranch', 1.0], ['VarBranch', 2.0], ['VarBranch', 3.0], ['Cuts', 0.0], ['Cuts', 1.0], ['Cuts', 2.0], ['Cuts', 3.0], ['CutPasses', 1.0], ['CutPasses', 3.0], ['CutPasses', 5.0], ['GomoryPasses', 0.0]]


def grb(file, pm_name, pm_value, mipgap =0.0001):
    model = read(file)
    model.setParam("MIPGap", mipgap)
    model.setParam("TimeLimit", 3600)
    model.setParam(pm_name, pm_value)
    model.optimize()
    nodes = model.NodeCount
    simplex = model.IterCount
    time = model.Runtime
    best_obj = model.ObjVal
    best_bound = model.ObjBound
    gap = model.MIPGap
    result = [pm_name, pm_value, mipgap, nodes, simplex, time, best_obj, best_bound, gap]

    return result

base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join( base_path, 'model_file_mps', 'traininstance2')
output_path = os.path.join(base_path, 'results', 'gurobi_result.csv')

#data = [[1,2,3,4,5,6,7,8,9]]
#df = pd.DataFrame(data,columns=['pm_name', 'pm_name', 'mipgap','nodes','simplex', 'time','best_obj', 'best_bound', 'gap'])
#df.to_csv(output_path, index= False, mode='a+', header=True)


for i in range(len(Parameter)):
    pm_name = Parameter[i][0]
    pm_value = Parameter[i][1]
    result = grb(input_path, pm_name, pm_value, mipgap=0.0001 )
    result=[result]


if __name__ == "__main__":
    Parameter = [['VarBranch', 2.0], ['VarBranch', 3.0], ['Cuts', 0.0], ['Cuts', 1.0], ['Cuts', 2.0], ['Cuts', 3.0],
                 ['CutPasses', 1.0], ['CutPasses', 3.0], ['CutPasses', 5.0], ['GomoryPasses', 0.0]]
    mpsfile = ['', '']

    for i in range(len(Mpsfile)):

        for j in range(len(Parameter)):
            pm_name = Parameter[i][0]
            pm_value = Parameter[i][1]
            for k in range(3):
                result = grb(input_path, pm_name, pm_value, mipgap=0.0001)
                result = [result]
                output(DE[1], DE[0], DE[2], PR[5], PR[6], PR[7], setting)
                df = pd.DataFrame(result)
                print(df)
                df.to_csv(output_path, index=False, mode='a+', header=False)






