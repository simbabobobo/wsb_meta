import warnings
import os
import pandas as pd
import pyomo.environ as pyo
from scripts.components.HeatPump import HeatPump
from scripts.FluidComponent import FluidComponent


class AirHeatPumpFluid(HeatPump, FluidComponent):

    def __init__(self, comp_name, temp_profile, comp_type="AirHeatPumpFluid",
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

        '''The parameters in the model are from 'A semi-theoretical model for
         energy efficiency assessment of air source heat pump systems':
           
         '''
        self.energy_flows_in = None
        # self.loss_noload = 0.90
        # self.loss_cycling = 0.95
        self.temp_profile = temp_profile
        # self.cop = HeatPump.cop

    def _constraint_conver(self, model, t_on=10):
        """
        Energy conservation equation for heat pump with variable COP value.
        Heat pump has only one input and one output, maybe? be caution for 5
        generation heat network.
        """
        water_heat_cap = 4.18 * 10 ** 3  # Unit J/kgK
        water_density = 1000  # kg/m3
        unit_switch = 3600 * 1000  # J/kWh

        input_powers = model.find_component('input_' + self.inputs[0] + '_' +
                                            self.name)
        output_powers = model.find_component('output_' + self.outputs[0] +
                                             '_' + self.name)
        size = model.find_component('size_' + self.name)
        cop = model.find_component('cop_' + self.name)

        temp_var = model.find_component('temp_' + self.name)
        return_temp_var = model.find_component('return_temp_' + self.name)

        for t in model.time_step:
            # index in pyomo model and python list is different

            loss_defrost = 1 - (t_on - 9) * 0.089 / 3

            model.cons.add(
                output_powers[t] == input_powers[t] * cop[t]
                * loss_defrost)
            #print(cop[t])
            # self.loss_noload * self.loss_cycling)

    '''The refrigerant used in almost all air source and geothermal source heat
     pumps on the market is R410a, and according to the article 'Mass flow rate
    of R-410A through short tubes working near the critical point' the
    critical temperature of R410a is 72.031 degrees Celsius, and the maximum
    heating temperature of common commercially available air source heat
     pumps is 55 degrees Celsius.'''
    def _constraint_temp(self, model, init_temp=40):
        temp_var = model.find_component('temp_' + self.name)
        for t in model.time_step:
            model.cons.add(temp_var[t] <= 55)

        for heat_output in self.heat_flows_out:
            t_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'temp')
            for t in range(len(model.time_step)):
                model.cons.add(temp_var[t + 1] == t_out[t + 1])

    def _constraint_return_temp(self, model, init_return_temp=35):
        return_temp_var = model.find_component('return_temp_' + self.name)
        for heat_output in self.heat_flows_out:
            t_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'temp')
            for t in range(len(model.time_step)):
                model.cons.add(return_temp_var[t + 1] == t_in[t + 1])

    def _constraint_mass_flow(self, model, mass_flow=0):
        for heat_output in self.heat_flows_out:
            m_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'mass')
            m_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'mass')
            for t in range(len(model.time_step)):
                model.cons.add(m_in[t + 1] == m_out[t + 1])
                '''
                if t < 5:
                    model.cons.add(m_in[t + 1] == m_out[t + 1])
                else:
                    a = t % 24
                    if 14 < a < 20:
                        model.cons.add(m_in[t + 1] == m_out[t + 1])
                    else:
                        m_in[t + 1] = 0
                        m_out[t + 1] = 0

                        
                        model.cons.add(m_in[t + 1] == mass_flow)
                        model.cons.add(m_out[t + 1] == mass_flow)
                        #model.cons.add(m_in[t + 1] == mass_flow)'''

    def add_cons(self, model):
        self._constraint_conver(model)
        self._constraint_temp(model)
        #self._constraint_return_temp(model)
        self._constraint_vdi2067(model)
        self._constraint_maxpower(model)
        self._constraint_heat_outputs(model)
        self._constraint_cop(model, self.temp_profile)

    def add_vars(self, model):
        super().add_vars(model)

        return_temp = pyo.Var(model.time_step, bounds=(0, None))
        model.add_component('return_temp_' + self.name, return_temp)

