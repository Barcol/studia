from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QSlider
from PySide2.QtCore import Slot, Qt

import csv
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

        self.button_file = QPushButton("Wybierz plik wejsciowy")
        self.button_enthalpy = QPushButton("Wygeneruj Entalpię")
        self.button_plot = QPushButton("Pokaż wykres")
        self.button_save_csv = QPushButton("Zapisz wykres pod postacią pliku csv")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(19)
        self.slider.setMaximum(21)
        self.slider.setValue(20)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        self.text = QLabel("Wybierz plik typu tekstowego.\nPlik powinien zawierać pomiary temperatury i ciepła właściw"
                           "ego.\n\nPierwsze 5 linijek pliku powinien stanowić nagłówek, o przykładowej postaci: \nNAME"
                           " Specific Heat\nXLABEL X-axis\nYLABEL Y-axis\nSCALE 1.000000 1.000000\nOFFSET 0.000000 "
                           "0.000000")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_file)
        self.layout.addWidget(self.button_enthalpy)
        self.layout.addWidget(self.button_plot)
        self.layout.addWidget(self.button_save_csv)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

        self.button_enthalpy.setDisabled(True)
        self.button_plot.setDisabled(True)
        self.button_save_csv.setDisabled(True)

        self.setWindowTitle("TurboEntalpolizator 6000")

        self.button_file.clicked.connect(self.read_file)
        self.button_enthalpy.clicked.connect(self.prepare_enthalpy)
        self.button_plot.clicked.connect(self.show_plot)
        self.button_plot.clicked.connect(self.save_plot)

    @Slot()
    def read_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', "./", "Text files (*.txt)")[0]
        self.temp_list, self.cp_list = self.file_r.data_prepare(filename)
        self.text.setText(f"Wybrano plik {filename}.\nOblicz wykres entalpi")
        self.button_enthalpy.setDisabled(False)

    @Slot()
    def prepare_enthalpy(self):
        self.entha_pro.create_data(self.temp_list, self.cp_list)
        self.entha_pro.repair_types(self.entha_pro.show_dataframe())
        self.entha_pro.prepare_enthalpy(self.entha_pro.show_dataframe())
        t_start, ok = QInputDialog.getInt(self, "Temperatura", "Wpisz wartość temperatury startu przemiany", value=100,)
        t_end, ok = QInputDialog.getInt(self, "Temperatura", "Wpisz wartość temperatury końca przemiany", value=200)
        enthalpy, ok = QInputDialog.getInt(self, "Entalpia", "Wpisz wartość entalpi przemiany", value=400)
        self.entha_pro.enthalpy_data_frame = self.entha_pro.add_phase_transition(self.entha_pro.enthalpy_data_frame,
                                                                                 t_start, t_end, enthalpy,
                                                                                 self.heat_distributor)

        self.text.setText("Wykres gotowy do pokazania")
        self.button_plot.setDisabled(False)
        self.button_save_csv.setDisabled(False)


    @Slot()
    def save_plot(self):
        data = self.entha_pro.show_dataframe()
        data.to_csv(r"results.csv")


    @Slot()
    def show_plot(self):
        self.ploter.draw_plot(self.entha_pro.enthalpy_data_frame, "enthalpy")
        self.text.setText("Wykres został wyswietlony w nowym oknie")
        self.ploter.present_plot()
        self.text.setText("Wykres gotowy do pokazania")
