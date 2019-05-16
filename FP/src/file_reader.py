from typing import List
import numpy as np


class FileReader:
    def data_prepare(self, file: str):
        temp = []
        cp = []
        self.txt_reader(file[0], temp, cp)
        return np.array(temp), np.array(cp)

    def txt_reader(self, text_input_path: str, temp: List, cp: List):
        with open(text_input_path, "r") as file:
            for number, line in enumerate(file):
                if number < 5:
                    pass
                else:
                    self.read_line(line, temp, cp)

    @staticmethod
    def read_line(line: str, temp: List, cp: List):
        for sign_number, sign in enumerate(line):
            if sign == " ":
                temp.append(line[0:sign_number])
                cp.append(line[sign_number + 1:-2])
