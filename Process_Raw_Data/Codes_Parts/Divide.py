# This file is to separate the data
import csv
import numpy as np
import os
# import sys

# X, Y, Lat, Lon, HDT, indicator, p_n, t_n
unprocessedFile = 'Transformed_All_complete.csv'

NoP = 44
p_n = 6
t_n = 7
HDT = 4
vecX = [6.136e-06, 7.260e-06]
vecY = [6.544e-06, -6.840e-06]
vecX = np.array(vecX)
vecY = np.array(vecY)
vec = (vecX + vecY) / 2

# splitDataDir = '\\Users\\happy\\OneDrive\\Documents\\Studies\\NSTC project\\DataCleaning&Generation\\Data'
splitDataDir = '\\Users\\happy\\OneDrive\\Documents\\Studies\\NSTC project\\DataCleaning&Generation\\Data0'

unprocData = []
with open(unprocessedFile, 'r') as csvFile:
    csv_reader = csv.reader(csvFile)
    next(csv_reader, None)
    for row in csv_reader:
        numeric_row = [float(value) for value in row]
        unprocData.append(numeric_row)

# print(unprocData)
divided_data = [[[] for _ in range(8)] for _ in range(1, NoP + 1)] # Initialize a 4D list
#                ^ A 2D list in there
# i = point number
# j = theta number
# k = kth row
# m = the mth field

# Divide the data into NoP parts
# for i in range(1, NoP + 1):
#     for row in unprocData: # Efficiency can be improved
#         if row and int(row[p_n]) == i: # row[6] is the p_n
#             divided_data[i - 1].append(row)

for i in range(1, NoP + 1): # 1~44
    for j in range(8): # 0~7 (0~315)
        # For a set of x y t
        for row in unprocData: # Efficiency is supposed to be improved...
            if row and int(row[p_n]) == i: # row[6] is the p_n
                if int(row[t_n]) == j * 45:
                    divided_data[i - 1][j].append(row)

# Despite many problems with the "truth", we use the assumption we made
# 1st way
# two [0, 75]s will have problems
truth = [[0, 0], [5, 0], [10, 0], [15, 0], [20, 0], [25, 0], [30, 0], [35, 0]
         , [40, 0], [45, 0], [50, 0], [55, 0], [60, 0], [63, 0], [63, 5], [63, 10]
         , [63, 15], [63, 20], [63, 25], [63, 30], [63, 35], [63, 40], [63, 45], [63, 50]
         , [63, 55], [63, 60], [63, 65], [63, 70], [63, 75], [53, 75], [43, 75], [33, 75]
         , [23, 75], [13, 75], [3, 75], [0, 75], [0, 72], [0, 70], [0, 60], [0, 50]
         , [0, 40], [0, 30], [0, 20], [0, 10]
         ] # x y t
# 2nd way
# truth = []
# truth_path = '.\\Truth_All\\truth.csv'
# with open(truth_path, newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     # Skip the header row
#     next(reader)
#     for row in reader:
#         truth.append([row[0], row[1]])

# print(truth)
# sys.exit(0)

angle = [45, 0, 315, 270, 225, 180, 135, 90]

def angleConversion(h):
    # 0 <-> 45, 45 <-> 0, 90 <-> 315, 135 <-> 270, 180 <-> 225 ... 
    return (405 - h) % 360

# Create the directory if it doesn't exist
if not os.path.exists(splitDataDir):
    os.makedirs(splitDataDir)

fileNames = []
# Create many txt files
for tuple in truth:
    for a in angle:
        fileName = ''
        fileName += str(tuple[0])
        fileName += '_'
        fileName += str(tuple[1])
        fileName += '_'
        fileName += str(a)
        fileName += '.csv'
        fileNames.append(fileName)

# print(fileNames)

cnt = 0
for fn in fileNames: # For each p_n t_n
    filePath = os.path.join(splitDataDir, fn)
    with open(filePath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write truth -> x y t as file name
        # Write est. -> x' y' t' as content of the file
        for row in divided_data[cnt // 8][cnt % 8]:
            theta = angleConversion(row[HDT]) # Unify angle calculation
            # thetaP45 = theta + 45
            # row.append([theta, thetaP45])
            # newRow = [[] for _ in range()]
            csv_writer.writerow([row[0], row[1], row[4]])

    cnt += 1