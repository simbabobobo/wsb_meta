from gurobipy import *

model = read('30n20b8.mps')
model.optimize()