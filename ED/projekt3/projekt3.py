import csv
import numpy as np

with open("day.csv") as csvfile:
    bikeset = csv.reader(csvfile)
    print(np.array(bikeset))
#        print(line)
