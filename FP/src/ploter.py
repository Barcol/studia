import matplotlib.pyplot as plt
import pandas as pd


class Ploter:
    def draw_plot(self, enthalpy_data_frame: pd.DataFrame, column: str):
        return plt.plot(enthalpy_data_frame["temp"], enthalpy_data_frame[column])
