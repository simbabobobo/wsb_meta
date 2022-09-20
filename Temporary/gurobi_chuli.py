import grb_test_func
import os
Parameter=[['Method',0],['Method',1]]

base_path = os.path.dirname(os.path.dirname(__file__))
input_path = os.path.join( base_path, 'ModelFile', '30n20b8.mps')


for i in range(len(Parameter)):
    pm_name = Parameter[i][0]
    pm_value = Parameter[i][1]
    result = grb(input_path, pm_name, pm_value )
    print('result is', result)
