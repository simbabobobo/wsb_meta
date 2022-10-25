from pyomo.environ import *

model = ConcreteModel()
model.x = Var(within=Reals, bounds=(0,10))
model.y = Var(within=Reals, bounds=(0,10))

model.profit = Objective(expr=3 * model.x + 4 * model.y, sense=minimize)

model.c1 = Constraint(expr=2 * model.x + model.y >= 15)
model.c2 = Constraint(expr=model.x + 2 * model.y >= 17)
model.c3 = Constraint(expr=model.x + model.y >= 10)

model.write("Example.mps")




model.pprint()
opt = SolverFactory('gurobi')

solution = opt.solve(model)
solution.write()
print('\nProfit=', model.profit())
print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('c1 = ', model.c1())
print('c2 = ', model.c2())
print('c3 = ', model.c3())

#print(model.objVal)

