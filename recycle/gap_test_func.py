from gurobipy import *


def gap(file, mipgap):
    model = read(file)
    model.setParam("MIPGap", mipgap)
    #model.setParam(pm_name, pm_value)
    model.optimize()
    name = model.ModelName
    nodes = model.NodeCount
    simplex = model.IterCount
    time = model.Runtime
    best_obj = model.ObjVal
    best_bound = model.ObjBound
    gap = model.MIPGap
    result = [name, mipgap, nodes, simplex, time, best_obj, best_bound, gap]

    return result