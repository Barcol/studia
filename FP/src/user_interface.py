from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PySide2.QtCore import Slot, Qt

from FP.src.enthalpy_processing import EnthalpyProcessing
from FP.src.file_reader import FileReader
from FP.src.heat_distribution import HeatDistribution


class FPApp(QWidget):
    def __init__(self, file_r: FileReader, entha_pro: EnthalpyProcessing, heat_distributor: HeatDistribution, ploter):
        QWidget.__init__(self)

        self.temp_list, self.cp_list = None, None

        self.file_r = file_r
        self.entha_pro = entha_pro
        self.heat_distributor = heat_distributor
        self.ploter = ploter

        self.button_file = QPushButton("Wybieerz plik wejsciowy")
        self.button_enthalpy = QPushButton("Wygeneruj Entalpię!")
        self.button_plot = QPushButton("Pokaż wykres")
        self.text = QLabel("Wybierz plik")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_file)
        self.layout.addWidget(self.button_enthalpy)
        self.layout.addWidget(self.button_plot)
        self.setLayout(self.layout)

        self.button_file.clicked.connect(self.read_file)
        self.button_enthalpy.clicked.connect(self.prepare_enthalpy)
        self.button_plot.clicked.connect(self.show_plot)

    @Slot()
    def read_file(self):
        self.temp_list, self.cp_list = self.file_r.data_prepare(QFileDialog.getOpenFileName(self, 'Open file',
                                                                                            "./",
                                                                                            "Text files (*.txt)"))
        self.text.setText("Oblicz wykres entalpi")

    @Slot()
    def prepare_enthalpy(self):
        self.entha_pro.create_data(self.temp_list, self.cp_list)
        self.entha_pro.repair_types(self.entha_pro.show_dataframe())
        self.entha_pro.prepare_enthalpy(self.entha_pro.show_dataframe())
        self.entha_pro.enthalpy_data_frame = self.entha_pro.add_phase_transition(self.entha_pro.enthalpy_data_frame,
                                                                                 100, 150, 100, self.heat_distributor)
        self.text.setText("Wykres gotowy do pokazania")

    @Slot()
    def show_plot(self):
        self.ploter.draw_plot(self.entha_pro.enthalpy_data_frame, "enthalpy")
        self.text.setText("Wykres wyswietlony w nowym oknie")
        self.ploter.present_plot()
