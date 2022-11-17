from scripts.Component import Component


class HeatExchanger(Component):

    def __init__(self, comp_name, comp_type="HeatExchanger", comp_model=None,
                 min_size=0, max_size=1000, current_size=0):
        self.inputs = ['heat']
        self.outputs = ['heat']

        super().__init__(comp_name=comp_name,
                         comp_type=comp_type,
                         comp_model=comp_model,
                         min_size=min_size,
                         max_size=max_size,
                         current_size=current_size)
