import matplotlib.pyplot as plt
import pandas as pd


class Ploter:
    def __init__(self):
        pass

    def draw_plot(self, enthalpy_data_frame: pd.DataFrame, column: str):
        return plt.plot(enthalpy_data_frame["temp"], enthalpy_data_frame[column])

    def present_plot(self):
        plt.show()

    def draw_plots(self, data, name, iteration):
        self.draw_plot(data, name)
        for index in range(iteration):
            self.draw_plot(data, name + "_backup" + str(index))
