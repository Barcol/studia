import pandas as pd


class HeatDistribution:
    def distribution_choser(self, data: pd.DataFrame, t_start: int, t_end: int, value: float):
        # return self.include_transition_heat_minus_sqr(data, t_start, t_end, value)
        return self.include_transition_heat_sqr(data, t_start, t_end, value)  # BANGLA
        # return self.include_transition_heat_rect(data, t_start, t_end, value) # BANGLA

    @staticmethod
    def include_transition_heat_rect(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor = 0
        factor_inc = value / (t_end - t_start)
        for index in range(len(data["temp"])):
            if (t_start <= data["temp"][index]) and (t_end >= data["temp"][index]):
                data["enthalpy"].at[index] += factor
                factor += factor_inc
            elif data["temp"][index] > t_end:
                print(factor)
                data["enthalpy"].at[index] += factor
        return data

    @staticmethod
    def include_transition_heat_sqr(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        counter = -1
        for index in range(len(data["temp"])):
            if (t_start < data["temp"][index]) and (t_end > data["temp"][index]):
                counter += 1
                data["enthalpy"].at[index] += value*(counter**2)/((t_end-t_start)**2)
            elif data["temp"][index] > t_end:
                data["enthalpy"].at[index] += value
        return data

    @staticmethod
    def include_transition_heat_minus_sqr(data: pd.DataFrame, t_start: int, t_end: int, value: float):
        factor = 0
        for index in range(len(data["temp"])):
            factor_inc = (value / (t_end - t_start)) * (index / (t_end - t_start))
            if (t_start <= data["temp"][index]) and (t_end >= data["temp"][index]):
                # print(value, (t_end-t_start), index, "\n\n")
                data["enthalpy"].at[index] += factor
                factor += factor_inc
            elif data["temp"][index] > t_end:
                print(factor)
                data["enthalpy"].at[index] += factor
        return data

