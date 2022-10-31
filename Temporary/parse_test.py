from module.parse_mps import *
from module.ea import *
import os
import pandas as pd
from matplotlib import pyplot as plt
from gurobipy import *

def lesen(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path


if __name__ == "__main__":
    model = 'buildingenergy.mps'
    input_path = lesen(model)
    PR = parse_mps(input_path, penalty_coeff=100000)
