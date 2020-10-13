import csv
import numpy as np

dir_files = "../Dataset/"

def readFiles():
    part = dict()
    for i in range(1):
        part[i] = None
        for d in range(1,6):
            file_name = dir_files + "part" + str(i) + "/part" + str(i) + "dev" + str(d) + ".csv"
            csv_file = open(file_name)
            csv_reader = csv.reader(csv_file, delimiter=',')
            rows = np.array(list(csv_reader)).astype(np.float)
            if(part[i] == None):
                part[i] = np.array(rows)
            else:
                np.append(part[i],rows)

        print(part[i].shape)


readFiles()