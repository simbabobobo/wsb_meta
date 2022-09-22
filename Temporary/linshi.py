from module.smps_loader import *
import os


base_path = os.path.dirname(os.path.dirname(__file__))
modelname = 'markshare2.mps'
input_path = os.path.join(base_path, 'model_file_mps', modelname)
name, objective_name, row_names, col_names, col_types, types, c, A, rhs_names, rhs, bnd_names, bnd = load_mps(input_path)
rhs_names1 = rhs_names[0]
rhs1 = rhs[rhs_names1]
k=2
a=k*max(rhs1)

print(a)