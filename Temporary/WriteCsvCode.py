import os

import pandas as pd

base_path = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(base_path, 'Result', 'metaheuristic.csv')

data = [[2,2,3,4,5,6,7,8,9,10,11]]
df = pd.DataFrame(data)

#df.to_csv(output_path, index=True, mode='a+', header=False)



# bixushi[[]]
#df = pd.DataFrame(data,columns=['ModelName', 'Algorithm', 'Parameter',
#                                                          'Best_obj',
#                                'Variable', 'Time','origin_obj', 'eq', 'ueq',
#                                'eq_number', 'ueq_number'])
#df = pd.DataFrame(data)
#df.to_csv(output_path, index=True, mode='a+', header=False)

#data2 = pd.DataFrame({'name':['wang'], 'nianling': [11]})

print(df)

#data2.to_csv(output_path, index=False, mode='a+', header=)
# index表示索引 header表示列名

#df.to_csv(output_path, index=True, mode='a+', header=True)


