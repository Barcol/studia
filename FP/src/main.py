from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def data_prepare():
    temp = []
    cp = []
    txt_reader("Specific_Heat.txt", temp, cp)
    return np.array(temp), np.array(cp)


def txt_reader(text_input_path: str, temp: List, cp: List):
    with open(text_input_path, "r") as file:
        for number, line in enumerate(file):
            if number < 5:
                pass
            else:
                read_line(line, temp, cp)


def read_line(line: str, temp: List, cp: List):
    for sign_number, sign in enumerate(line):
        if sign == " ":
            temp.append(line[0:sign_number])
            cp.append(line[sign_number+1:-2])


def repair_types(data: pd.DataFrame):
    for index, value in enumerate(data["temp"]):
        data["temp"][index] = int(float(value))
    for index, value in enumerate(data["cp"]):
        data["cp"][index] = float(value)


def prepare_enthalpy(data):
    enthalpy = []
    for index in range(len(data["temp"])):
        index = int(index)
        if index == 0:
            enthalpy.append(0)
        else:
            enthalpy.append(enthalpy[index - 1] + (data["temp"][index]-data["temp"][index-1])
                            * (data["cp"][index]+data["cp"][index-1]) * (1/2))
    data["enthalpy"] = np.array(enthalpy)
    return data


def interpolate(data: pd.DataFrame, value: int):
    for index in range(len(data["temp"])):
        if value > data["temp"][index]:
            continue
        else:
            return (((value-data["temp"][index - 1])
                     * ((data["cp"][index] - data["cp"][index - 1])
                        / (data["temp"][index] - data["temp"][index - 1]))) + data["cp"][index - 1])


def thicken_list(thin_table: pd.DataFrame, start_point: int, end_point: int):
    for temp in range(int(start_point), int(end_point)):
        if temp not in thin_table["temp"]:
            pass
            # add new row that thickenes the empty space
    return thin_table


def add_phase_transition(data: pd.DataFrame, t_start: int, t_end: int, function: int):
    value_list = thicken_list(data, t_start, t_end)
    # b bla bla add function to list bla bla
    return value_list


if __name__ == "__main__":
    temp_list, cp_list = data_prepare()
    enthalpy_data_frame = pd.DataFrame({"temp": temp_list, "cp": cp_list})
    repair_types(enthalpy_data_frame)
    enthalpy_data_frame = prepare_enthalpy(enthalpy_data_frame)
    print(enthalpy_data_frame)
    plt.plot(enthalpy_data_frame["enthalpy"], enthalpy_data_frame["temp"])
    plt.show()
    thickened_list = add_phase_transition(enthalpy_data_frame, 100, 200, 1)
    # plt.show()
