import matplotlib.pyplot as plt
import pandas as pd
import sys

from FP.src.enthalpy_processing import EnthalpyProcessing
from FP.src.file_reader import FileReader
from FP.src.heat_distribution import HeatDistribution
from FP.src.ploter import Ploter
from FP.src.user_interface import FPApp
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = FPApp()
    widget.resize(800, 600)
    widget.show()

    file_r = FileReader()
    entha_pro = EnthalpyProcessing()
    heat_distributor = HeatDistribution()

    temp_list, cp_list = file_r.data_prepare("Specific_Heat.txt")
    enthalpy_data_frame = pd.DataFrame({"temp": temp_list, "cp": cp_list})
    entha_pro.repair_types(enthalpy_data_frame)
    enthalpy_data_frame = entha_pro.prepare_enthalpy(enthalpy_data_frame)

    ploter = Ploter()

    # ploter.draw_plot(enthalpy_data_frame, "enthalpy")
    # enthalpy_data_frame = entha_pro.add_phase_transition(enthalpy_data_frame, 100, 150, 100, heat_distributor)
    # ploter.draw_plot(enthalpy_data_frame, "enthalpy")
    # plt.show()
    sys.exit(app.exec_())
