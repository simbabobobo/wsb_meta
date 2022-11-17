import os
import warnings
import pandas as pd
import pyomo.environ as pyo
from scripts.FluidComponent import FluidComponent
from scripts.Component import Component
from pyomo.gdp import Disjunct, Disjunction

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))

unit_switch_W = 1000  # Wh/kWh
unit_switch_J = 3600 * 1000  # J/kWh
small_num = 0.00001

class SolarThermalCollectorFluid(FluidComponent):

    def __init__(self, comp_name, temp_profile, irr_profile,
                 comp_type='SolarThermalCollectorFluid', comp_model=None,
                 min_size=0, max_size=1000, current_size=0):
        super().__init__(comp_name=comp_name,
                         comp_type=comp_type,
                         comp_model=comp_model,
                         min_size=min_size,
                         max_size=max_size,
                         current_size=current_size)
        self.inputs = ['solar']
        self.outputs = ['heat']
        self.temp_profile = temp_profile
        self.irr_profile = irr_profile
        self.solar_liquid_heat_cap = 3690  # J/kgK
        self.max_temp = 135
        self.mass_flow = None  # kg/h

    def _constraint_temp(self, model):
        outlet_temp = model.find_component('outlet_temp_' + self.name)
        inlet_temp = model.find_component('inlet_temp_' + self.name)
        for heat_output in self.heat_flows_out:
            t_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'temp')
            t_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'temp')
            for t in model.time_step:
                model.cons.add(outlet_temp[t] == t_out[t])
                model.cons.add(t_in[t] == inlet_temp[t])
                # Über die max. Temperatur verdampft die Solarflüssigkeit.
                model.cons.add(outlet_temp[t] <= self.max_temp)
                model.cons.add(inlet_temp[t] <= outlet_temp[t])

    def _constraint_efficiency(self, model):
        eff = model.find_component('eff_' + self.name)
        solar_coll_properties_path = os.path.join(base_path, "data",
                                                  "component_database",
                                                  "SolarThermalCollectorFluid",
                                                  "FPC.csv")
        solar_coll_properties = pd.read_csv(solar_coll_properties_path)
        if 'optical_eff' in solar_coll_properties.columns:
            self.OpticalEfficiency = float(solar_coll_properties['optical_eff'])
        else:
            warnings.warn(
                "In the model database for " + self.component_type +
                " lack of column for optical efficiency.")
        if 'K' in solar_coll_properties.columns:
            self.K = float(solar_coll_properties['K'])
        else:
            warnings.warn(
                "In the model database for " + self.component_type +
                " lack of column for K.")
        outlet_temp = model.find_component('outlet_temp_' + self.name)
        inlet_temp = model.find_component('inlet_temp_' + self.name)

        # G = 1000 w/m2 (Solar Keymark Certificate)
        for t in model.time_step:
            model.cons.add(eff[t] == self.OpticalEfficiency - self.K * (
                    (inlet_temp[t] + outlet_temp[t]) / 2 -
                    self.temp_profile[t - 1]) / 1000)

    # 'size' bezieht sich auf die Fläche der Solarthermie.
    def _constraint_conver(self, model):
        eff = model.find_component('eff_' + self.name)
        input_energy = model.find_component('input_' + self.inputs[0] +
                                            '_' + self.name)
        comp_size = model.find_component('size_' + self.name)
        for t in model.time_step:
            model.cons.add(input_energy[t] == self.irr_profile[t - 1] * eff[
                t] * comp_size / unit_switch_W)
        output_energy = model.find_component('output_' + self.outputs[0] +
                                             '_' + self.name)
        for heat_output in self.heat_flows_out:
            m_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'mass')
            m_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'mass')
            t_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'temp')
            t_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'temp')
            for t in model.time_step:
                # todo:Beim Stagnationszustand gilt output_energy< input_energy
                # aber das Ergebnis ist komisch
                model.cons.add(output_energy[t] <= input_energy[t])
                model.cons.add(
                    output_energy[t] == self.solar_liquid_heat_cap * (
                            m_out[t] * t_out[t] - m_in[t] * t_in[t]) /
                    unit_switch_J)

    def _constraint_output_permit_gdp(self, model, off_delta_temp=4,
                                  on_delta_temp=8, init_status='on'):
        '''
        for t in model.time_step:
            if status_var[t] = 1
                if outlet_temp[t+1] - inlet_temp[t+1] <= off_delta_temp:
                    status[t+1] = 0
                    energy[t+1] = 0
                else:
                    status[t+1] = 1
            else:
                if outlet_temp[t+1] - inlet_temp[t+1] >= on_delta_temp:
                    status[t+1] = 1
                else:
                    status[t+1] = 0
                    energy[t+1] = 0
            '''

        output_energy = model.find_component('output_' + self.outputs[0] +
                                             '_' + self.name)
        outlet_temp = model.find_component('outlet_temp_' + self.name)
        inlet_temp = model.find_component('inlet_temp_' + self.name)
        model.init = pyo.BooleanVar()

        if init_status == 'on':
            model.init_log = pyo.LogicalConstraint(
                expr=model.init.equivalent_to(True))
        elif init_status == 'off':
            model.init_log = pyo.LogicalConstraint(
                expr=model.init.equivalent_to(False))

        for t in model.time_step:
            a = Disjunct()
            c_1 = pyo.Constraint(
                expr=outlet_temp[t] - inlet_temp[t] <= off_delta_temp)
            c_2 = pyo.Constraint(expr=output_energy[t] == 0)
            model.add_component('a_dis_' + str(t), a)
            a.add_component('a_1_' + str(t), c_1)
            a.add_component('a_2_' + str(t), c_2)

            b = Disjunct()
            c_7 = pyo.Constraint(
                expr=outlet_temp[t] - inlet_temp[
                    t] >= off_delta_temp + small_num)
            model.add_component('b_dis_' + str(t), b)
            b.add_component('b_1_' + str(t), c_7)

            c = Disjunct()
            c_3 = pyo.Constraint(
                expr=outlet_temp[t] - inlet_temp[t] >= on_delta_temp)
            model.add_component('c_dis_' + str(t), c)
            c.add_component('c_' + str(t), c_3)

            d = Disjunct()
            c_4 = pyo.Constraint(expr=output_energy[t] == 0)
            c_6 = pyo.Constraint(expr=outlet_temp[t] - inlet_temp[
                t] <= on_delta_temp - small_num)
            model.add_component('d_dis_' + str(t), d)
            d.add_component('d_1_' + str(t), c_4)
            d.add_component('d_2_' + str(t), c_6)

            dj = Disjunction(expr=[a, b, c, d])
            model.add_component('dj3_dis_' + str(t), dj)

            if t == 1:
                p_4 = pyo.LogicalConstraint(
                    expr=model.init.equivalent_to(
                        pyo.lor(a.indicator_var, b.indicator_var)))
                p_5 = pyo.LogicalConstraint(
                    expr=~model.init.equivalent_to(
                        pyo.lor(c.indicator_var, d.indicator_var)))
            else:
                last_status = model.find_component('b_dis_' + str(t - 1))
                p_4 = pyo.LogicalConstraint(
                    expr=pyo.lor(a.indicator_var,
                                 b.indicator_var).equivalent_to(
                        last_status.indicator_var))
                p_5 = pyo.LogicalConstraint(
                    expr=~last_status.indicator_var.equivalent_to(
                        pyo.lor(c.indicator_var, d.indicator_var)))
            model.add_component('p_4_' + str(t), p_4)
            model.add_component('p_5_' + str(t), p_5)

    def _constraint_heat_cap_var(self, model):
        outlet_temp = model.find_component('outlet_temp_' + self.name)
        inlet_temp = model.find_component('inlet_temp_' + self.name)
        heat_cap = model.find_component('solar_fluid_heat_cap')
        for t in model.time_step:
            model.cons.add(heat_cap[t] == 3400 + 4 * (inlet_temp[t] +
                                                      outlet_temp[
                                                          t]) / 2)  # J/(kg*K)
    # konstanter Massenstrom
    def _constraint_mass_con(self, model, mass_flow):
        self.mass_flow = mass_flow
        for heat_output in self.heat_flows_out:
            m_in = model.find_component(
                heat_output[1] + '_' + heat_output[0] +
                '_' + 'mass')
            m_out = model.find_component(
                heat_output[0] + '_' + heat_output[1] +
                '_' + 'mass')
            for t in model.time_step:
                model.cons.add(m_in[t] == self.mass_flow)
                model.cons.add(m_out[t] == self.mass_flow)

    # Energieerhaltung beim variierten Massenstrom
    def _constraint_conver_mass_con(self, model):
        heat_cap = model.find_component('solar_fluid_heat_cap')
        eff = model.find_component('eff_' + self.name)
        input_energy = model.find_component('input_' + self.inputs[0] +
                                            '_' + self.name)
        comp_size = model.find_component('size_' + self.name)
        for t in model.time_step:
            model.cons.add(input_energy[t] == self.irr_profile[t - 1] * eff[
                t] * comp_size / unit_switch_W)
        output_energy = model.find_component('output_' + self.outputs[0] +
                                             '_' + self.name)
        for heat_output in self.heat_flows_out:
            t_in = model.find_component(heat_output[1] + '_' + heat_output[0] +
                                        '_' + 'temp')
            t_out = model.find_component(heat_output[0] + '_' + heat_output[1] +
                                         '_' + 'temp')
            for t in model.time_step:
                model.cons.add(output_energy[t] == input_energy[t])
                model.cons.add(
                    output_energy[t] == heat_cap[t] * self.mass_flow * (
                                t_out[t] - t_in[t]) / unit_switch_J)

    def add_cons(self, model, heat_cap_type='con'):
        self._constraint_vdi2067(model)
        self._constraint_temp(model)
        self._constraint_efficiency(model)
        self._constraint_output_permit_gdp(model)
        if heat_cap_type =='con':
            self._constraint_conver(model)
        if heat_cap_type == 'var':
            self._constraint_heat_cap_var(model)
            self._constraint_mass_con(model, mass_flow=200)  # kg/h
            self._constraint_conver_mass_con(model)

    def add_vars(self, model):
        super().add_vars(model)

        inlet_temp = pyo.Var(model.time_step, bounds=(0, 95))
        model.add_component('inlet_temp_' + self.name, inlet_temp)

        outlet_temp = pyo.Var(model.time_step, bounds=(0, 135))
        model.add_component('outlet_temp_' + self.name, outlet_temp)

        eff = pyo.Var(model.time_step, bounds=(0, 1))
        model.add_component('eff_' + self.name, eff)

        heat_cap = pyo.Var(model.time_step, bounds=(0, None))
        model.add_component('solar_fluid_heat_cap', heat_cap)