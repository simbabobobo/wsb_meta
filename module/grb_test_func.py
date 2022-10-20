from gurobipy import *


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
