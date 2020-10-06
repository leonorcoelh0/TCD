import csv
import numpy as np

dir_files = "../Dataset/"

def readFiles():
    part = dict()
    for i in range(1):
        print("Ler individuo",i)
        part[i] = np.empty([1,1])
        for d in range(1,6):
            file_name = dir_files + "part" + str(i) + "/part" + str(i) + "dev" + str(d) + ".csv"
            print("Ler dev",d)
            csv_file = open(file_name)
            csv_reader = csv.reader(csv_file, delimiter=',')
            # print (csv_reader)
            rows = np.array(list(csv_reader))
            print(rows.shape)


readFiles()