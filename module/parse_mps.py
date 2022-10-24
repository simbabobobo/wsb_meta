import re
import numpy as np
import math

"""
将mps文件所对应的 有约束模型
利用 惩罚函数
输出为 无约束模型
输出格式：目标函数、维度、下界、上界、精度、惩罚函数值

load_mps部分作者@author: Julian Märte
"""


def load_mps(path):
    CORE_FILE_ROW_MODE = "ROWS"
    CORE_FILE_COL_MODE = "COLUMNS"
    CORE_FILE_RHS_MODE = "RHS"
    CORE_FILE_BOUNDS_MODE = "BOUNDS"

    CORE_FILE_BOUNDS_MODE_NAME_GIVEN = "BOUNDS_NAME"
    CORE_FILE_BOUNDS_MODE_NO_NAME = "BOUNDS_NO_NAME"
    CORE_FILE_RHS_MODE_NAME_GIVEN = "RHS_NAME"
    CORE_FILE_RHS_MODE_NO_NAME = "RHS_NO_NAME"

    ROW_MODE_OBJ = "N"

    mode = ""
    name = None
    objective_name = None
    row_names = []
    types = []
    col_names = []
    col_types = []
    A = np.matrix([[]])
    c = np.array([])
    rhs_names = []
    rhs = {}
    bnd_names = []
    bnd = {}
    integral_marker = False

    with open(path, "r") as reader:
        for line in reader:
            if line.startswith("*"):
                continue

            line = re.split(" |\t", line)
            line = [x.strip() for x in line]
            line = list(filter(None, line))

            if len(line) == 0:
                continue
            if line[0] == "ENDATA":
                break
            if line[0] == "*":
                continue
            if line[0] == "NAME":
                name = line[1]
            elif line[0] in [CORE_FILE_ROW_MODE, CORE_FILE_COL_MODE]:
                mode = line[0]
            elif line[0] == CORE_FILE_RHS_MODE and len(line) <= 2:
                if len(line) > 1:
                    rhs_names.append(line[1])
                    rhs[line[1]] = np.zeros(len(row_names))
                    mode = CORE_FILE_RHS_MODE_NAME_GIVEN
                else:
                    mode = CORE_FILE_RHS_MODE_NO_NAME
            elif line[0] == CORE_FILE_BOUNDS_MODE and len(line) <= 2:
                if len(line) > 1:
                    bnd_names.append(line[1])
                    bnd[line[1]] = {"LO": np.zeros(len(col_names)),
                                    "UP": np.repeat(math.inf, len(col_names))}
                    mode = CORE_FILE_BOUNDS_MODE_NAME_GIVEN
                else:
                    mode = CORE_FILE_BOUNDS_MODE_NO_NAME
            elif mode == CORE_FILE_ROW_MODE:
                if line[0] == ROW_MODE_OBJ:
                    objective_name = line[1]
                else:
                    types.append(line[0])
                    row_names.append(line[1])
            elif mode == CORE_FILE_COL_MODE:
                if len(line) > 1 and line[1] == "'MARKER'":
                    if line[2] == "'INTORG'":
                        integral_marker = True
                    elif line[2] == "'INTEND'":
                        integral_marker = False
                    continue
                try:
                    i = col_names.index(line[0])
                except:
                    if A.shape[1] == 0:
                        A = np.zeros((len(row_names), 1))
                    else:
                        A = np.concatenate((A, np.zeros((len(row_names), 1))),
                                           axis=1)
                    col_names.append(line[0])
                    col_types.append(integral_marker * 'integral' + (
                        not integral_marker) * 'continuous')
                    c = np.append(c, 0)
                    i = -1
                j = 1
                while j < len(line) - 1:
                    if line[j] == objective_name:
                        c[i] = float(line[j + 1])
                    else:
                        A[row_names.index(line[j]), i] = float(line[j + 1])
                    j = j + 2
            elif mode == CORE_FILE_RHS_MODE_NAME_GIVEN:
                if line[0] != rhs_names[-1]:
                    raise Exception(
                        "Other RHS name was given even though name was set after RHS tag.")
                for kk in range((len(line) - 1) // 2):
                    idx = kk * 2
                    rhs[line[0]][row_names.index(line[idx + 1])] = float(
                        line[idx + 2])
            elif mode == CORE_FILE_RHS_MODE_NO_NAME:
                try:
                    i = rhs_names.index(line[0])
                except:
                    rhs_names.append(line[0])
                    rhs[line[0]] = np.zeros(len(row_names))
                    i = -1
                for kk in range((len(line) - 1) // 2):
                    idx = kk * 2
                    rhs[line[0]][row_names.index(line[idx + 1])] = float(
                        line[idx + 2])
            elif mode == CORE_FILE_BOUNDS_MODE_NAME_GIVEN:
                if line[1] != bnd_names[-1]:
                    raise Exception(
                        "Other BOUNDS name was given even though name was set after BOUNDS tag.")
                if line[0] in ["LO", "UP"]:
                    bnd[line[1]][line[0]][col_names.index(line[2])] = float(
                        line[3])
                elif line[0] == "FX":
                    bnd[line[1]]["LO"][col_names.index(line[2])] = float(
                        line[3])
                    bnd[line[1]]["UP"][col_names.index(line[2])] = float(
                        line[3])
                elif line[0] == "FR":
                    bnd[line[1]]["LO"][col_names.index(line[2])] = -math.inf
            elif mode == CORE_FILE_BOUNDS_MODE_NO_NAME:
                try:
                    i = bnd_names.index(line[1])
                except:
                    bnd_names.append(line[1])
                    bnd[line[1]] = {"LO": np.zeros(len(col_names)),
                                    "UP": np.repeat(math.inf, len(col_names))}
                    i = -1
                if line[0] in ["LO", "UP"]:
                    bnd[line[1]][line[0]][col_names.index(line[2])] = float(
                        line[3])
                elif line[0] == "FX":
                    bnd[line[1]]["LO"][col_names.index(line[2])] = float(
                        line[3])
                    bnd[line[1]]["UP"][col_names.index(line[2])] = float(
                        line[3])
                elif line[0] == "FR":
                    bnd[line[1]]["LO"][col_names.index(line[2])] = -math.inf
    return name, objective_name, row_names, col_names, col_types, types, c, A, rhs_names, rhs, bnd_names, bnd


def parse_mps(mps_file, penalty_coeff=100000):

    print('Start parse')
    name, objective_name, row_names, col_names, col_types, types, c, A, \
    rhs_names, rhs, bnd_names, bnd = load_mps(mps_file)
    """
    # name: 优化模型名称
    # rows_names: 目标函数及约束名称
    # types: 约束类型
    # col_names: 变量名称
    # col_types: 变量类型
    # c: 目标函数系数
    # A: 约束矩阵
    # rhs: 定义约束条件等号右边的值
    # bnd: 定义决策变量的上界或下界
    """

    dimensions = len(col_names)
    rhs_names1 = rhs_names[0]
    rhs1 = rhs[rhs_names1]

    def generate_ori():
        ori = []
        for i in range(dimensions):
            ori.append('(' + str(c[i]) + '*' + 'x[' + str(i) + ']' + ')')
        ori = "+".join(ori)
        # join：通过指定字符连接序列中元素后生成的新字符串
        return lambda x: eval(ori)

    ori_obj = generate_ori()
    # 生成目标函数

    def generate_cons():
        eq_list = []
        ueq_list = []
        for i in range(len(types)):
            if types[i] == 'E':
                eq_list1 = []
                for j in range(dimensions):
                    eq_list1.append(
                        '(' + str(A[i][j]) + '*' + 'x[' + str(j) + ']' + ')')
                eq_list1 = "+".join(eq_list1)
                eq_list1 = eq_list1 + '-(' + str(rhs1[i]) + ')'
                eq_list.append(eq_list1)
            if types[i] == 'G':
                ueq_list1 = []
                for j in range(dimensions):
                    ueq_list1.append(
                        '(' + str(A[i][j]) + '*' + 'x[' + str(j) + ']' + ')')
                ueq_list1 = "+".join(ueq_list1)
                ueq_list1 = str(rhs1[i]) + '-(' + ueq_list1 + ')'
                ueq_list.append(ueq_list1)
                # lambda x: eval
            if types[i] == 'L':
                ueq_list2 = []
                for k in range(dimensions):
                    ueq_list2.append(
                        '(' + str(A[i][k]) + '*' + 'x[' + str(k) + ']' + ')')
                ueq_list2 = "+".join(ueq_list2)
                ueq_list2 = ueq_list2 + '-(' + str(rhs1[i]) + ')'
                ueq_list.append(ueq_list2)
        return eq_list, ueq_list

    eq, ueq = generate_cons()
    # 生成等式和不等式约束

    def penalty_obj(var, typ=1, t=0):
        obj = ori_obj(var)

        if typ == 1:
            for i in range(len(eq)):
                equation = eq[i]
                eq_method = lambda x: eval(equation)
                obj += penalty_coeff * (max(0, abs(eq_method(var)))) ** 2
            for i in range(len(ueq)):
                equation = ueq[i]
                ueq_method = lambda x: eval(equation)
                obj += penalty_coeff * (max(0, ueq_method(var)))
        if typ == 2:
            print(t)
            for i in range(len(eq)):
                equation = eq[i]
                eq_method = lambda x: eval(equation)
                obj += (500 * t)**2 * (max(0, abs(eq_method(var))))**2
            for i in range(len(ueq)):
                equation = ueq[i]
                ueq_method = lambda x: eval(equation)
                obj += (500 * t)**2 * (max(0, ueq_method(var)))

        return obj
    # 生成惩罚函数

    def penalty_eq_obj(v):
        eq_value = []
        counter = 0
        for i in eq:
            constraint = lambda x: eval(i)
            eq_value.append(constraint(v))
            if constraint(v) != 0:
                counter += 1

        return eq_value, counter

    def penalty_ueq_obj(v):
        ueq_value = []
        counter = 0
        for i in ueq:
            constraint = lambda x: eval(i)
            ueq_value.append(constraint(v))
            if constraint(v) > 0:
                counter += 1

        return ueq_value, counter

    precision = col_types

    def generate_bound():
        bnd_names1 = bnd_names[0]
        lb = bnd[bnd_names1]['LO']
        ub = bnd[bnd_names1]['UP']
        kk = 5
        maxvalue = kk * max(rhs1)
        if maxvalue >= 1000000:
            maxvalue = 1000000
        # maxvalue = 1000000
        for i in range(dimensions):
            if str(ub[i]) == 'inf':
                ub[i] = maxvalue
                # mo ren up bound wei 10
        return lb, ub
    low, up = generate_bound()


    return penalty_obj, dimensions, low, up, precision, ori_obj, \
           penalty_eq_obj, penalty_ueq_obj









