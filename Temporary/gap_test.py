from gap_test_func import *
import os
import pandas as pd



base_path = os.path.dirname(os.path.dirname(__file__))

output_path = os.path.join(base_path, 'results', 'gap_result.csv')

# Parameter=[['p0201', 0.0001], ['p0201', 0.001], ['p0201', 0.01], ['neos-3754480-nidda', 0.0001], ['neos-3754480-nidda', 0.001], ['neos-3754480-nidda', 0.01], ['gen-ip054', 0.0001], ['gen-ip054', 0.001], ['gen-ip054', 0.01]]
Parameter=[['proteindesign121hz512p9.mps', 0.01]]
#


for i in range(len(Parameter)):

    filename = Parameter[i][0]
    input_path = os.path.join(base_path, 'model_file_mps', filename)
    mipgap = Parameter[i][1]
    result = gap(input_path, mipgap)
    result = [result]
    df = pd.DataFrame(result)
    # print(df)
    df.to_csv(output_path, index= False, mode='a+', header=False)