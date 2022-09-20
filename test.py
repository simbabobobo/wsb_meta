from parse_mps import *
from smps_loader import *
from PSO import *
import os

base_path = os.path.dirname(os.path.dirname(__file__))
example_path = os.path.join('Example.mps')

name, objective_name, row_names, col_names, col_types, types, c, A, \
rhs_names, rhs, bnd_names, bnd = load_mps(example_path)

var = []
for i in range(len(col_names)):
    var.append('x[' + str(i) + ']')
# 生成形式为x[0]、x[i]的变量
print('Var Declarations')

obj = []
for i in range(len(var)):
    obj.append('(' + str(c[i]) + '*' + str(var[i]) + ')')
obj = "+".join(obj)
print(obj)
# join：通过指定字符连接序列中元素后生成的新字符串
ori_obj = lambda x: eval(obj)

print(ori_obj([1,1]))

eq_list = []
ueq_list = []
rhs_names1 = rhs_names[0]
rhs1 = rhs[rhs_names1]

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
        ueq_list1 = ueq_list1 + '-(' + str(rhs1[i]) + ')'
        print('ueq_list1 is', ueq_list1)
        #a=lambda x: eval(ueq_list1)
        #print('[1,1]', a([1,1]))
        ueq_list.append(ueq_list1)
        print(ueq_list)

    if types[i] == 'L':
        ueq_list2 = []
        for k in range(len(var)):
            ueq_list2.append('(' + str(A[i][k]) + '*' + str(var[k]) + ')')
        ueq_list2 = "+".join(ueq_list2)
        ueq_list2 = ueq_list2 + '-(' + str(rhs1[i]) + ')'
        print('ueq_list2', ueq_list2)
        ueq_list.append(lambda x: eval(ueq_list2))

for i in range(len(ueq_list)):
    a2= lambda x: eval(ueq_list[i])
    print('ueq',a2([2, 2]))






a1=[lambda x:x+1,lambda x:x+2]
b1=0
c1=[]
c1.append(a1)
print('c1 is', c1)
