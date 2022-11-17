import os
from scripts.Project import Project
from scripts.Environment import Environment
from scripts.Building import Building
import tools.post_solar_chp as post_pro

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

################################################################################
#                           Generate python objects
################################################################################

# Generate a project object at first.
project = Project(name='project_12', typ='building')


# Generate the environment object
env_12 = Environment(time_step=8)
project.add_environment(env_12)

# If the objective of the project is the optimization for building, a building
# should be added to the project.
bld_12 = Building(name='bld_12', area=200, bld_typ='Wohngebäude')

# Add the energy demand profiles to the building object
# Attention! generate thermal with profile whole year temperature profile
#bld_12.add_thermal_profile('heat', env_12)
#bld_12.add_elec_profile(2021, env_12)
#bld_12.add_hot_water_profile(env_12)
# bld_12.add_hot_water_profile_TBL(1968, env_12)

bld_12.demand_profile['heat_demand'] = [10, 10, 10, 10, 0, 10, 10, 10]
bld_12.demand_profile["elec_demand"] = [0, 0, 0]*10

# Pre define the building energy system with the topology for different
# components and add components to the building.
# todo: 1 hinter 'chp_fluid_small' kann man löschen oder hinzufügen.
# (keine Auslauftemperaturanforderung)
topo_file = os.path.join(base_path, 'data', 'topology',
                         'chp_fluid_small.csv')
bld_12.add_topology(topo_file)
bld_12.add_components(project.environment)
project.add_building(bld_12)

################################################################################
#                        Build pyomo model and run optimization
################################################################################
project.build_model(obj_typ='annual_cost')
project.run_optimization('gurobi', save_lp=True, save_result=True)

################################################################################
#                                  Post-processing
################################################################################

result_output_path = os.path.join(base_path, 'data', 'opt_output',
                                  project.name + '_result.csv')
#post_pro.plot_all(result_output_path, time_interval=[0, env_12.time_step])
post_pro.print_size(result_output_path)