import matplotlib.pyplot as plt
import pandas as pd
import random
import sys

from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt

from FP.src.enthalpy_processing import EnthalpyProcessing
from FP.src.file_reader import FileReader
from FP.src.heat_distribution import HeatDistribution
from FP.src.ploter import Ploter


class FPApp(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.button = QPushButton("Wybieerz plik wejsciowy")
        self.button2 = QPushButton("Wygeneruj Entalpię!")
        self.button3 = QPushButton("Pokaż wykres")
        self.text = QLabel("Jakis TEXT")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self, entha_pro, enthalpy_data_frame, heat_distributor):
        enthalpy_data_frame = entha_pro.add_phase_transition(enthalpy_data_frame, 100, 150, 100, heat_distributor)
        self.ploter.draw_plot(enthalpy_data_frame, "enthalpy")
        plt.show()
