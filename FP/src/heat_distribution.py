import pandas as pd


class HeatDistribution:
    def distribution_choser(self, data: pd.DataFrame, t_start: int, t_end: int, value: float, choose: str):
        if choose == "smooth":
            data = self.include_transition_heat_sqr(data, t_start, int((t_start + t_end)/2), value/2)
            return self.include_transition_heat_minus_sqr(data, int((t_start + t_end)/2), t_end, value/2)
        if choose == "rect":
            return self.include_transition_heat_rect(data, t_start, t_end, value)
        if choose == "sqr":
            return self.include_transition_heat_sqr(data, t_start, t_end, value)
        if choose == "minus_sqr":
            return self.include_transition_heat_minus_sqr(data, t_start, t_end, value)

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

    @staticmethod
    def include_transition_heat_sqr(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor = -1
        for index in range(len(data["temp"])):
            if (t_start < data["temp"][index]) and (t_end > data["temp"][index]):
                factor += 1
                data["enthalpy"].at[index] += value*(factor**2) / ((t_end - t_start)**2)
            elif data["temp"][index] >= t_end:
                data["enthalpy"].at[index] += value
        return data

    @staticmethod
    def include_transition_heat_minus_sqr(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor, counter = 0, -1
        factor_inc = value / (t_end - t_start)
        for index in range(len(data["temp"])):
            if (t_start <= data["temp"][index]) and (t_end >= data["temp"][index]):
                counter += 1
                data["enthalpy"].at[index] += (2 * factor) - value*(counter**2) / ((t_end - t_start)**2)
                factor += factor_inc
            elif data["temp"][index] > t_end:
                data["enthalpy"].at[index] += value
        return data

    @staticmethod
    def include_transition_heat_smooth(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor = -1
        counter = 0
        factor_inc = value / (t_end - t_start)
        for index in range(len(data["temp"])):
            if (t_start < data["temp"][index]) and (((t_end+t_start)/2) >= data["temp"][index]):
                factor += 1
                data["enthalpy"].at[index] += value * (factor ** 2) / ((t_end - t_start) ** 2)
            elif (((t_end+t_start)/2) < data["temp"][index]) and (t_end >= data["temp"][index]):
                counter += 1
                data["enthalpy"].at[index] += (2 * factor) - value * (counter ** 2) / ((t_end - t_start) ** 2)
                factor += factor_inc
            elif data["temp"][index] > t_end:
                data["enthalpy"].at[index] += value
        return data
