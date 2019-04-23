import numpy as np
import matplotlib.pyplot as plt


def calculate_d(d0, q, r, t):
    D = d0*np.exp(-q/(r*t))*10000000000
    D = D * time_step / (dx**2)
    if D <= 0.5:
        return D
    else:
        return False


def create_array(length, value_one, value_two):
    array = []
    half_length = int(length / 2)
    for number in range(length):
        if number < half_length:
            array.append(value_one)
        else:
            array.append(value_two)
    return array


dx = 0.1
heat_rate = 2
time_step = 0.01
iteration = 3000

temp = 727
temp_K = temp + 273
Q = 140000
R = 8.3144
d0 = 0.000041
D = calculate_d(d0, Q, R, temp_K)
array = create_array(100, 6.67, 0.025)
old_array = array.copy()

for number in range(iteration):
    D = calculate_d(d0, Q, R, temp_K)
    if not D:
        break
    for cell in range(len(array) - 1):
        array[cell] = ((old_array[cell] * (1 - 2 * D)) + (D * (old_array[cell - 1] + old_array[cell + 1])))

    temp_K += time_step * heat_rate
    old_array = array

plt.plot(array)
plt.show()
