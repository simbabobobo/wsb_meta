from module.smps_loader import *
# 将mps文件所对应的 有约束模型 利用 惩罚函数 输出为 无约束模型 输出为：目标函数、维度、下界、上界、精度、惩罚函数值


def parse_mps(mps_file,  eq_penalty_coeff = 3,  ueq_penalty_coeff = 20, k=5):

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
            eq_list.append(eq_list1)

        if types[i] == 'G':
            ueq_list1 = []
            for j in range(len(var)):
                ueq_list1.append('(' + str(A[i][j]) + '*' + str(var[j]) + ')')
            ueq_list1 = "+".join(ueq_list1)
            ueq_list1 = str(rhs1[i])  + '-(' + ueq_list1 + ')'
            ueq_list.append(ueq_list1)
            #lambda x: eval

        if types[i] == 'L':
            ueq_list2 = []
            for k in range(len(var)):
                ueq_list2.append('(' + str(A[i][k]) + '*' + str(var[k]) + ')')
            ueq_list2 = "+".join(ueq_list2)
            ueq_list2 = ueq_list2 + '-(' + str(rhs1[i]) + ')'
            ueq_list.append(ueq_list2)
    # 生成等式和不等式约束

    print('Constraint Declarations')

    def penalty_obj(var):
        obj_func = ori_obj(var)

        for i in range(len(eq_list)):
            equation = eq_list[i]
            eq_method = lambda x: eval(equation)
            obj_func += eq_penalty_coeff * (max(0, abs(eq_method(var)))) ** 2

        for i in range(len(ueq_list)):
            equation = ueq_list[i]
            ueq_method = lambda x: eval(equation)
            obj_func += ueq_penalty_coeff * (max(0, ueq_method(var))) ** 3

        return obj_func
    # 生成惩罚函数

    def origin_obj(v):
        ori_value = ori_obj(v)
        #print('\nOrigin objective function value:', ori_value)
        return ori_value

    def penalty_eq_obj(v):
        p_eq_value = 0
        eq_value = []
        counter = 0
        p_eq = []

        for i in eq_list:
            constraint = lambda x: eval(i)
            p_eq_value += eq_penalty_coeff * (max(0, abs(constraint(v)))) ** 2
            eq_value.append(constraint(v))
            if constraint(v) != 0:
                counter += 1

        #print('\np_eq_value is', p_eq_value,)
        # print('eq_value is', eq_value, )
        #print('number break eq is', counter )
        eq = [p_eq_value, counter]

        return eq

    def penalty_ueq_obj(v):
        p_ueq_value = 0
        ueq_value = []
        counter=0
        ueq=[]

        for i in ueq_list:
            #print(i)
            constraint = lambda x: eval(i)
            p_ueq_value += ueq_penalty_coeff * (max(0, constraint(v))) ** 3
            ueq_value.append(constraint(v))
            if constraint(v) > 0:
                counter += 1
                # dayu 0 cai wei bei

        #print('\np_ueq_value is', p_ueq_value, )
        # print('ueq_value is', ueq_value, )
        #print('number break ueq is', counter)
        ueq = [p_ueq_value, counter]

        return ueq

    precision = col_types

    bnd_names1 = bnd_names[0]
    lb = bnd[bnd_names1]['LO']
    ub = bnd[bnd_names1]['UP']

    k=5
    maxvalue = k*max(rhs1)
    if maxvalue >= 1000000:
        maxvalue = 1000000

    #maxvalue = 1000000

    for i in range(len(lb)):
        if str(ub[i]) == 'inf':
            ub[i] = maxvalue
            # mo ren up bound wei 10

    return penalty_obj, dimensions, lb, ub, precision, origin_obj, \
           penalty_eq_obj, penalty_ueq_obj









