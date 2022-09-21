from gurobipy import *
import os


base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join( base_path, 'model_file_mps', 'p0201.mps')

print(input_path)


model = read(input_path)

#model.setParam("Method",2)
#model.setParam("GomoryPasses", 0)
#model.Params.TuneTimeLimit=60
#model.tune()
model.optimize()
obj_res = model.getObjective().getValue()

#print('objval', model.ObjVal)

#model._obj = None
#model._bd = None
#model._data = []
#model._start = time.time()
#model.optimize(callback=data_cb)

#with open('data.csv', 'w') as f:
    #writer = csv.writer(f)
    #writer.writerows(model._data)