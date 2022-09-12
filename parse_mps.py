from smps_loader import *
# 将mps文件所对应的 有约束模型 利用 惩罚函数 输出为 无约束模型 输出为：目标函数、维度、下界、上界、精度、惩罚函数值


def parse_mps(mps_file,  eq_penalty_coeff = 3,  ueq_penalty_coeff = 20):

    name, objective_name, row_names, col_names, col_types, types, c, A, \
    rhs_names, rhs, bnd_names, bnd = load_mps(mps_file)
    # name: 优化模型名称
    # rows_names: 目标函数及约束名称
    # types: 约束类型
    # col_names: 变量名称
    # col_types: 变量类型
    # c: 目标函数系数
    # A: 约束矩阵
    # rhs: 定义约束条件等号右边的值
    # bnd: 定义决策变量的上界或下界
    print('Start parse')

    rhs_names1 = rhs_names[0]
    rhs1 = rhs[rhs_names1]

    dimensions = 0
    dimensions = len(col_names)

    var = []
    for i in range(len(col_names)):
        var.append('x[' + str(i) + ']')
    # 生成形式为x[0]、x[i]的变量
    print('Var Declarations')

    obj = []
    for i in range(len(var)):
        obj.append('(' + str(c[i]) + '*' + str(var[i]) + ')')
    obj = "+".join(obj)
    # join：通过指定字符连接序列中元素后生成的新字符串
    ori_obj = lambda x: eval(obj)
    # 生成目标函数
    print('Objective Declarations')

    eq_list = []
    ueq_list = []

    for i in range(len(types)):
        if types[i] == 'E':
            eq_list1 = []
            for j in range(len(var)):
                eq_list1.append('(' + str(A[i][j]) + '*' + str(var[j]) + ')')
            eq_list1 = "+".join(eq_list1)
            eq_list1 = eq_list1 + '-(' + str(rhs1[i]) + ')'
            eq_list.append(lambda x: eval(eq_list1))

        if types[i] == 'G':
            ueq_list1 = []
            for j in range(len(var)):
                ueq_list1.append('(' + str(A[i][j]) + '*' + str(var[j]) + ')')
            ueq_list1 = "+".join(ueq_list1)
            ueq_list1 = str(rhs1[i]) + '-(' + ueq_list1 + ')'
            ueq_list.append(lambda x: eval(ueq_list1))

        if types[i] == 'L':
            ueq_list2 = []
            for k in range(len(var)):
                ueq_list2.append('(' + str(A[i][k]) + '*' + str(var[k]) + ')')
            ueq_list2 = "+".join(ueq_list2)
            ueq_list2 = ueq_list2 + '-(' + str(rhs1[i]) + ')'
            ueq_list.append(lambda x: eval(ueq_list2))
    # 生成等式和不等式约束

    print('Constraint Declarations')

    def penalty_obj(var):
        obj_func = ori_obj(var)

        for eq_method in eq_list:
            obj_func += eq_penalty_coeff * (max(0, abs(eq_method(var)))) ** 2

        for ueq_method in ueq_list:
            obj_func += ueq_penalty_coeff * (max(0, ueq_method(var))) ** 3

        return obj_func
    # 生成惩罚函数

    def origin_obj(v):
        ori_value = ori_obj(v)

        return ori_value

    def penalty_eq_obj(v):
        p_eq_value = 0
        counter = 0

        for constraint in eq_list:
            p_eq_value += eq_penalty_coeff * (max(0, abs(constraint(v)))) ** 2
            if constraint(v) != 0:
                counter += 1
        print('number eq is:', counter)
        return p_eq_value

    def penalty_ueq_obj(v):
        p_ueq_value = 0
        counter=0

        for constraint in ueq_list:
            p_ueq_value += ueq_penalty_coeff * (max(0, constraint(v))) ** 3
            if constraint(v) != 0:
                counter += 1
        print('number ueq is', counter)

        return p_ueq_value

    precision = col_types

    bnd_names1 = bnd_names[0]
    lb = bnd[bnd_names1]['LO']
    ub = bnd[bnd_names1]['UP']

    for i in range(len(lb)):
        if str(ub[i]) == 'inf':
            if col_types[i] == 'integral':
                ub[i] = 1.0
                lb[i] = 0.0

            else:
                ub[i] = None
                lb[i] = None

    return penalty_obj, dimensions, lb, ub, precision, origin_obj, \
           penalty_eq_obj, penalty_ueq_obj









