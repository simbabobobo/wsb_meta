from backup.de import *


def original_obj(x):
    return -(2*x[0]*x[1] - 0.2*x[0] - x[4])

eq_method_list = [
    lambda x: x[2] + x[3] - 1,
]

ueq_method_list = [
    lambda x: x[0] * x[1] - 2,
    lambda x: 0 - (x[0] - ((-8 * x[1]) + 9) - (-9) * (1 - x[2])),
    lambda x: x[0] - ((-8 * x[1]) + 9) - 7 * (1 - x[2]) - 0,
    lambda x: 0.2 - (x[1] - (-0.2) * (1 - x[2])),
    lambda x: x[1] - 0.05 * (1 - x[2]) - 0.95,
    lambda x: 2.5 - (x[4] - (- (1 - x[2]))),
    lambda x: x[4] - 2.5,
    lambda x: 0 - (x[0] - ((-10 * x[1]) + 15) - (-15) * (1 - x[3])),
    lambda x: x[0] - ((-10 * x[1]) + 15) - 3 * (1 - x[3]) - 0,
    lambda x: 0.7 - x[1] + (-0.69999999999999996) * (1 - x[3]),
    lambda x: x[1] - 0.010000000000000009 * (
            1 - x[3]) - 0.98999999999999999,
    lambda x: 1.5 - x[4],
    lambda x: x[4] - (1 - x[3]) - 1.5,
]

def penalty_obj(var):
    obj_func = original_obj(var)

    eq_penalty_coeff = 3
    ueq_penalty_coeff = 20

    for eq_method in eq_method_list:
        obj_func += eq_penalty_coeff* (max(0, abs(eq_method(var)))) ** 2

    for ueq_method in ueq_method_list:
        obj_func += ueq_penalty_coeff * (max(0, ueq_method(var))) ** 3

    return obj_func

def penalty_eq_cons(var):
    """ori_obj is the original objective method, equal equation list should
    be """
    obj_func = original_obj(var)

    for eq_method in eq_method_list:
        obj_func += (max(0, abs(eq_method(var)))) ** 2

    return obj_func


def penalty_ueq_cons(var):
    obj_func = original_obj(var)

    for ueq_method in ueq_method_list:
        obj_func += (max(0, ueq_method(var))) ** 3

    return obj_func


bounds = [(0, 8.0), (0, 1.0), (0, 1), (0, 1), (1.5, 2.5)]
binary = [False, False, True, True, False]

print(original_obj([1,2,3,4,5]))
print(penalty_obj([0,0,0,0,0]))

# Run Differential Evolution optimization
DE = list(de(penalty_obj, bounds, binary, mut=0.8, crossp=0.6, popsize=200,
             its=1000))
# print(DE[-1][-1])
x = DE[-1][0]
ofunc_value = DE[-1][-1]
pen_eq= penalty_eq_cons(x)
pen_ueq = penalty_ueq_cons(x)
ori_obj = original_obj(x)

print(DE)
print('best value', DE[0][1])
print('best varible', DE[0][0])

print('RESULT:')
print('Objective function value:', ofunc_value)
print('Penalty eq:', pen_eq)
print('Penalty ueq:', pen_ueq)
print('Objective function value clean:',
      ofunc_value - pen_eq - pen_ueq)
print('Objective function value clean:',
      ori_obj)
print('Variables: ', x)
