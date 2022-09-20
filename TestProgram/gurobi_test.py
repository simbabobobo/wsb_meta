from gurobipy import *
#import csv
#import time
import os



#def data_cb(model, where):
    #if where == GRB.Callback.MIP:
        #cur_obj = model.cbGet(GRB.Callback.MIP_OBJBST)
        #cur_bd = model.cbGet(GRB.Callback.MIP_OBJBND)
        #cur_node=cur_bd = model.cbGet(GRB.Callback.MIP_NODCNT)


        # Did objective value or best bound change?
        #if model._obj != cur_obj or model._bd != cur_bd:
            #model._obj = cur_obj
            #model._bd = cur_bd
            #model._data.append([time.time() - model._start, cur_obj, cur_bd])

base_path = os.path.dirname(os.path.dirname(__file__))
example_path_1 = os.path.join( base_path, 'ModelFile', '30n20b8.mps')
example_path = os.path.normcase(example_path_1)
#example_path = '30n20b8.mps'
print(example_path)

# Build model m here
model = read(example_path)
#model.resetParams()
#model.setParam("MIPGap",0.001)
#model.setParam("GomoryPasses", 0)
#model.Params.TuneTimeLimit=60
#model.tune()
model.optimize()
obj_res = model.getObjective().getValue()

#model._obj = None
#model._bd = None
#model._data = []
#model._start = time.time()
#model.optimize(callback=data_cb)

#with open('data.csv', 'w') as f:
    #writer = csv.writer(f)
    #writer.writerows(model._data)