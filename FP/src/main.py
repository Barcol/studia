import sys

from FP.src.enthalpy_processing import EnthalpyProcessing
from FP.src.file_reader import FileReader
from FP.src.heat_distribution import HeatDistribution
from FP.src.ploter import Ploter
from FP.src.user_interface import FPApp
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_r = FileReader()
    entha_pro = EnthalpyProcessing()
    heat_distributor = HeatDistribution()
    ploter = Ploter()

    widget = FPApp(file_r, entha_pro, heat_distributor, ploter)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
