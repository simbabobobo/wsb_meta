import warnings
import os
import pandas as pd
import pyomo.environ as pyo
from scripts.components.HeatPump import HeatPump
from scripts.FluidComponent import FluidComponent


class GroundHeatPumpFluid(HeatPump, FluidComponent):

    def __init__(self, comp_name, temp_profile, comp_type="GroundHeatPumpFluid",
                 comp_model=None,
                 min_size=0, max_size=1000, current_size=0):
        # Define inputs and outputs before the initialisation of component,
        # otherwise we can't read properties properly. By getting efficiency,
        # the energy typ is needed.
        self.inputs = ['elec']
        self.outputs = ['heat']

        HeatPump.__init__(self, comp_name=comp_name,
                          temp_profile=temp_profile,
                          comp_type=comp_type,
                          comp_model=comp_model,
                          min_size=min_size,
                          max_size=max_size,
                          current_size=current_size)

        FluidComponent.__init__(self, comp_name=comp_name,
                                comp_type=comp_type,
                                comp_model=comp_model,
                                min_size=min_size,
                                max_size=max_size,
                                current_size=current_size)

        self.energy_flows_in = None
        self.temp_profile = temp_profile

    def _constraint_conver(self, model):
        """
        Energy conservation equation for heat pump with variable COP value.
        Heat pump has only one input and one output, maybe? be caution for 5
        generation heat network.
        """

        input_powers = model.find_component('input_' + self.inputs[0] + '_' +
                                            self.name)
        output_powers = model.find_component('output_' + self.outputs[0] +
                                             '_' + self.name)
        cop = model.find_component('cop_' + self.name)

        temp_var = model.find_component('temp_' + self.name)
        return_temp_var = model.find_component('return_temp_' + self.name)

        for t in model.time_step:
            # index in pyomo model and python list is different

            model.cons.add(
                output_powers[t] == input_powers[t] * cop[t])

    '''The refrigerant used in almost all air source and geothermal source heat
         pumps on the market is R410a, and according to the article 'Mass flow rate
        of R-410A through short tubes working near the critical point' the
        critical temperature of R410a is 72.031 degrees Celsius, and the maximum
        heating temperature of common commercially available geothermal source heat
         pumps is 55 degrees Celsius.'''

    def _constraint_temp(self, model):
        temp_var = model.find_component('temp_' + self.name)
        for t in model.time_step:
            model.cons.add(temp_var[t] <= 65)
        for heat_output in self.heat_flows_out:
            t_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'temp')
            for t in range(len(model.time_step)):
                model.cons.add(temp_var[t + 1] == t_out[t + 1])

    def _constraint_return_temp(self, model):
        return_temp_var = model.find_component('return_temp_' + self.name)
        # for t in range(len(model.time_step)):
        # model.cons.add(return_temp_var[t + 1] <= 35)
        for heat_output in self.heat_flows_out:
            t_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'temp')
            for t in range(len(model.time_step)):
                model.cons.add(return_temp_var[t + 1] == t_in[t + 1])

    def add_cons(self, model):
        self._constraint_conver(model)
        self._constraint_temp(model)
        self._constraint_return_temp(model)
        self._constraint_vdi2067(model)
        self._constraint_cop(model, self.temp_profile)
        self._constraint_heat_outputs(model)
        self._constraint_maxpower(model)

    def add_vars(self, model):
        super().add_vars(model)

        return_temp = pyo.Var(model.time_step, bounds=(0, None))
        model.add_component('return_temp_' + self.name, return_temp)
