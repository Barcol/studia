import pandas as pd


class HeatDistribution:
    def distribution_choser(self, data: pd.DataFrame, t_start: int, t_end: int, value: float):
        return self.include_transition_heat_rect(data, t_start, t_end, value)

    @staticmethod
    def include_transition_heat_rect(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor = 0
        factor_inc = value / (t_end - t_start)
        for index in range(len(data["temp"])):
            if (t_start <= data["temp"][index]) and (t_end >= data["temp"][index]):
                data["enthalpy"].at[index] += factor
                factor += factor_inc
            elif data["temp"][index] > t_end:
                data["enthalpy"].at[index] += factor
        return data
