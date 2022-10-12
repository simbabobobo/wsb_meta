from gurobipy import *

base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join('model_file_mps', 'PyomoExample.mps')
model = read(input_path)
model.optimize()
time_grb = model.Runtime
best_grb = model.ObjVal