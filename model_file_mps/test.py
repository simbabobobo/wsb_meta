from gurobipy import *

model = read('PyomoExample.mps')
model.optimize()
time_grb = model.Runtime
best_grb = model.ObjVal