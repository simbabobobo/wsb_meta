"""
This script is used to validate StratificationStorage class.
"""

import os
from scripts.Project import Project
from scripts.Environment import Environment
from scripts.Building import Building
import tools.post_processing as post_pro

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

################################################################################
#                           Generate python objects
################################################################################

# Generate a project object at first.
project = Project(name='project_4', typ='building')


# Generate the environment object
env_4 = Environment(time_step=3)
project.add_environment(env_4)

# If the objective of the project is the optimization for building, a building
# should be added to the project.
bld_4 = Building(name='bld_4', area=200)

# Add the energy demand profiles to the building object
# Attention! generate thermal with profile whole year temperature profile
# bld_2.add_thermal_profile('heat', env_2.temp_profile_original, env_2)

bld_4.demand_profile['heat_demand'] = [1, 0, 1]

# Pre define the building energy system with the topology for different
# components and add components to the building.
topo_file = os.path.join(base_path, 'data', 'topology',
                         'gasboiler.csv')
bld_4.add_topology(topo_file)
bld_4.add_components(project.environment)
project.add_building(bld_4)

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
# post_pro.plot_all(result_output_path)