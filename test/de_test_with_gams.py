"""
This example is from pyomo tutorial, which has solved the global optimal
point.
The original problem could be modeled as following:
     max Z = c_1 * F* X — c_2 * F — C_rxn
        st. F * X < d
        [ Y_I
        F = a_I * X + b_I
        X_I_LB <= X <= X_I_UB
        C_rxn = c_I]
        or
        [Y_II
        F = a_II * X + b_II
        X_II_LB <= X <= X_II_UB
        C_rxn = c_II]

        Y_I or Y_II = True
        C_rxn, X , F in R
        F_LB <= F <= F_UB
        Y_I, Y_II in {True,False}
The solved optimal is
F=2.438 x=0.82, C_rnx=2.5, Z=1.01

###############################################################################
#                   pyomo codes for validation
###############################################################################
m = pyo.ConcreteModel('gdp_test')

m.F = pyo.Var(bounds=(0, 8), doc="Flow into reactor")
m.X = pyo.Var(bounds=(0, 1), doc="Reactor conversion")
m.d = pyo.Param(initialize=2, doc="Max product demand")

m.c = pyo.Param([1, 2, 'I', 'II'], doc="Costs", initialize={
    1: 2,  # Value of product
    2: 0.2,  # Cost of raw material
    'I': 2.5,  # Cost of reactor I
    'II': 1.5  # Cost of reactor II
})
m.alpha = pyo.Param(['I', 'II'], doc="Reactor coefficient",
                    initialize={'I': -8, 'II': -10})
m.beta = pyo.Param(['I', 'II'], doc="Reactor coefficient",
                   initialize={'I': 9, 'II': 15})
m.X_LB = pyo.Param(['I', 'II'], doc="Reactor conversion lower bound",
                   initialize={'I': 0.2, 'II': 0.7})
m.X_UB = pyo.Param(['I', 'II'], doc="Reactor conversion upper bound",
                   initialize={'I': 0.95, 'II': 0.99})
m.C_rxn = pyo.Var(bounds=(1.5, 2.5), doc="Cost of reactor")
m.max_demand = pyo.Constraint(expr=m.F * m.X <= m.d, doc="product demand")
m.reactor_choice = Disjunction(expr=[[m.F == m.alpha['I'] * m.X + m.beta['I'],
                                      m.X_LB['I'] <= m.X, m.X <= m.X_UB['I'],
                                      m.C_rxn == m.c['I']],
                                     # Disjunct 2: Choose reactor II
                                     [m.F == m.alpha['II'] * m.X + m.beta['II'],
                                      m.X_LB['II'] <= m.X,
                                      m.X <= m.X_UB['II'],
                                      m.C_rxn == m.c['II']]
                                     ], xor=True)
m.profit = pyo.Objective(expr=m.c[1] * m.F * m.X - m.c[2] * m.F - m.C_rxn,
                         sense=pyo.maximize)

pyo.TransformationFactory('gdp.bigm').apply_to(m)
run_data = pyo.SolverFactory('bonmin').solve(m)

for v in m.component_objects(pyo.Var, active=True):
    for index in v:
        print("   ", v[index], v[index].value)
"""
import os
import numpy as pd

from module.parse_gams import *
from module.de import *

########
# Parse GAMS file
########
base_path = os.path.dirname(os.path.dirname(__file__))
example_path = os.path.join(base_path, 'GamsFile', 'pyomo_gdp.gams')
contents = parse_gams(example_path)
eq_list, ueq_list, obj_func, bounds, binary = gen_model(contents)
new_obj = add_penalty(obj_func, eq_list, ueq_list)
print(obj_func([1,2,3,4,5]))
print(new_obj([0,0,0,0,0]))
########
# Solve with evolutionary algorithm
########
bounds = list(bounds.values())
print(bounds)
# DE = list(de(obj_func, bounds, binary, eq_list, ueq_list))
DE = list(de(new_obj, bounds, binary, its=1000))

print(DE[-1][-1])
x = DE[-1][0]
# ofunc_value = DE[-1][-1]
# pen_eq= penalty_eq_cons(x)
# pen_ueq = penalty_ueq_cons(x)
# ori_obj = original_obj(x)
#
# print('RESULT:')
# print('Objective function value:', ofunc_value)
# print('Penalty eq:', pen_eq)
# print('Penalty ueq:', pen_ueq)
# print('Objective function value clean:',
#       ofunc_value - pen_eq - pen_ueq)
print('Objective function value clean:',
      obj_func(x))
print('Variables: ', x)
