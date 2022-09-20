from grb_test_func import *
import os
import pandas as pd

Parameter=[['Method', 0.0], ['Method', 1.0], ['Method', 2.0], ['BranchDir', -1.0], ['BranchDir', 1.0], ['Heuristics', 0.0], ['Heuristics', 0.1], ['Heuristics', 0.3], ['Heuristics', 0.5], ['Heuristics', 0.7], ['Heuristics', 1.0], ['MIPFocus', 1.0], ['MIPFocus', 2.0], ['MIPFocus', 3.0], ['VarBranch', 1.0], ['VarBranch', 2.0], ['VarBranch', 3.0], ['Cuts', 0.0], ['Cuts', 1.0], ['Cuts', 2.0], ['Cuts', 3.0], ['CutPasses', 1.0], ['CutPasses', 3.0], ['CutPasses', 5.0], ['GomoryPasses', 0.0]]
base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join( base_path, 'ModelFile', 'p0201.mps')
output_path = os.path.join(base_path, 'Result', 'gurobi_result.csv')

#data = [[1,2,3,4,5,6,7,8,9]]
#df = pd.DataFrame(data,columns=['pm_name', 'pm_name', 'mipgap','nodes','simplex', 'time','best_obj', 'best_bound', 'gap'])
#df.to_csv(output_path, index= False, mode='a+', header=True)


for i in range(len(Parameter)):
    pm_name = Parameter[i][0]
    pm_value = Parameter[i][1]
    result = grb(input_path, pm_name, pm_value )
    result=[result]
    df = pd.DataFrame(result)
    print(df)
    df.to_csv(output_path, index= False, mode='a+', header=False)

