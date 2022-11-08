import os
import pandas as pd
from gurobipy import *


def grb(file, pm_name, pm_value):
    model = read(file)
    #model.setParam("MIPGap", mipgap)
    model.setParam(pm_name, pm_value)
    model.optimize()
    name = model.ModelName
    nodes = model.NodeCount
    simplex = model.IterCount
    time = model.Runtime
    best_obj = model.ObjVal
    best_bound = model.ObjBound
    gap = model.MIPGap
    output = [name, pm_name, pm_value, time, best_obj, best_bound, gap, nodes,
              simplex]

    return output


if __name__ == "__main__":
    # Parameter=[['Method', 0.0], ['BranchDir', -1.0], ['Heuristics', 0.0], ['Heuristics', 0.1], ['MIPFocus', 1.0],  ['VarBranch', 1.0], ['Cuts', 0.0],  ['CutPasses', 1.0], ['GomoryPasses', 0.0]]

    Parameter = [["TimeLimit", 3600]]
    Mpsfile = ['reblock115.mps', 'var-smallemery-m6j6.mps', 'neos-631710.mps']


    base_path = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_path, 'results', 'gurobi_result.csv')

    for i in range(len(Mpsfile)):
        input_path = os.path.join(base_path, 'model_file_mps', Mpsfile[i])
        for j in range(len(Parameter)):
            pm_name = Parameter[j][0]
            pm_value = Parameter[j][1]
            for k in range(3):
                result = grb(input_path, pm_name, pm_value)
                result = [result]
                df = pd.DataFrame(result)
                df.to_csv(output_path, index=False, mode='a+', header=False)






