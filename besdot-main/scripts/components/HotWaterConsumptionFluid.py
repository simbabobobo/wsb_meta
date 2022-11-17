import os
import warnings
import pandas as pd
import pyomo.environ as pyo
from scripts.FluidComponent import FluidComponent

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))


class HotWaterConsumptionFluid(FluidComponent):

    def __init__(self, comp_name, consum_profile,
                 comp_type="HotWaterConsumptionFluid", comp_model=None,
                 min_size=0, max_size=1000, current_size=0):
        self.inputs = ['heat']

        super().__init__(comp_name=comp_name,
                         comp_type=comp_type,
                         comp_model=comp_model,
                         min_size=min_size,
                         max_size=max_size,
                         current_size=current_size)

        self.consum_profile = consum_profile
        self.cold_water_temp = 12
        self.heat_flows_out = None

    def _constraint_vdi2067(self, model):
        """
        The hot water consumption has currently no max. power or investment
        constraint. However, in the future this can used to implement costs
        of electric energy consumers.
        """
        pass

    def _constraint_maxpower(self, model):
        """
        The hot water consumption has currently no max. power or investment
        constraint. However, in the future this can be used to implement the
        max. power of single power socket etc.
        """
        pass

    def _constraint_conver(self, model):
        """The input energy for Consumption should equal to the demand profil"""
        input_energy = model.find_component('input_' + self.inputs[0] + '_' +
                                            self.name)
        for t in model.time_step:
            ####################################################################
            # ATTENTION!!! The time_step in pyomo is from 1 to 8760 and
            # python list is from 0 to 8759, so the index should be modified.
            ####################################################################
            model.cons.add(input_energy[t] == self.consum_profile[t-1])

    # todo (qli): HotWaterConsumption.py anpassen
    def _constraint_cold_water_temp(self, model, cold_water_temp=12):
        for heat_input in self.heat_flows_in:
            t_out = model.find_component(heat_input[1] + '_' + heat_input[0] +
                                         '_' + 'temp')
            for t in model.time_step:
                model.cons.add(cold_water_temp == t_out[t])

    # todo (qli): HotWaterConsumption.py anpassen
    def _constraint_hot_water_temp(self, model, hot_water_temp=60):
        for heat_input in self.heat_flows_in:
            t_in = model.find_component(heat_input[0] + '_' + heat_input[1] +
                                        '_' + 'temp')
            for t in model.time_step:
                model.cons.add(hot_water_temp == t_in[t])

    def add_cons(self, model):
        self._constraint_conver(model)
        # todo: (qli) anpassen
        self._constraint_cold_water_temp(model)
        # todo: (qli) anpassen
        self._constraint_hot_water_temp(model)
        self._constraint_heat_inputs(model)

    def add_vars(self, model):
        #super().add_vars(model)

        input_energy = pyo.Var(model.time_step, bounds=(0, None))
        model.add_component('input_' + self.inputs[0] + '_' + self.name,
                            input_energy)

