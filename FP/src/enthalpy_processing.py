import numpy as np
import pandas as pd
from typing import List

from FP.src.heat_distribution import HeatDistribution


class EnthalpyProcessing:
    def __init__(self):
        self.enthalpy_data_frame = None

    def show_dataframe(self):
        return self.enthalpy_data_frame

    def create_data(self, temp_list: List, cp_list: List):
        self.enthalpy_data_frame = pd.DataFrame({"temp": temp_list, "cp": cp_list})

    @staticmethod
    def repair_types(data: pd.DataFrame):
        for index, value in enumerate(data["temp"]):
            data["temp"][index] = int(float(value))
        for index, value in enumerate(data["cp"]):
            data["cp"][index] = float(value)

    def prepare_enthalpy(self, data):
        enthalpy = []
        for index in range(len(data["temp"])):
            index = int(index)
            if index == 0:
                enthalpy.append(0)
            else:
                enthalpy.append(enthalpy[index - 1] + (data["temp"][index] - data["temp"][index - 1])
                                * (data["cp"][index] + data["cp"][index - 1]) * (1 / 2))
        data["enthalpy"] = np.array(enthalpy)
        self.enthalpy_data_frame = data

    @staticmethod
    def interpolate(temp: pd.Series, data_to_interpolate: pd.Series, value: int):
        for index in range(len(temp)):
            if value > temp[index]:
                continue
            else:
                return (((value - temp[index - 1])
                         * ((data_to_interpolate[index] - data_to_interpolate[index - 1])
                            / (temp[index] - temp[index - 1]))) + data_to_interpolate[index - 1])

    def thicken_list(self, thin_table: pd.DataFrame, start_point: int, end_point: int):
        temps = []
        cps = []
        enthalpys = []
        for temp in range(int(start_point), int(end_point)):
            if temp not in thin_table["temp"]:
                temps.append(temp)
                cps.append(self.interpolate(thin_table["temp"], thin_table["cp"], temp))
                enthalpys.append(self.interpolate(thin_table["temp"], thin_table["enthalpy"], temp))
        thin_table = thin_table.append(pd.DataFrame({"temp": temps, "cp": cps, "enthalpy": enthalpys}),
                                       ignore_index=True)
        return thin_table.sort_values("temp")

    def add_phase_transition(self, data: pd.DataFrame, t_start: int, t_end: int, value: float,
                             heat_distributer: HeatDistribution):
        data = self.thicken_list(data, t_start, t_end)
        data = data.reset_index(drop=True)
        data = heat_distributer.distribution_choser(data, t_start, t_end, value)
        return data
