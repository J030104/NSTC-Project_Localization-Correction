import csv
import numpy as np

file = 'processed_data_cleaned.csv' # RTK-precision points are cleaned in moderation
NoP = 44; # Number of Points

data = [] # The table to save the content
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    for row in reader:
        data.append(row)

# print(data)

divided_data = [[] for _ in range(1, NoP + 1)] # Initialize a 3D list
# i = point number
# j = jth row
# k = the kth field

# Divide the data into NoP parts
for i in range(1, NoP + 1):
    for row in data: # Efficiency can be improved
        if row and int(row[4]) == i: # row[4] is the p_n
            divided_data[i - 1].append(row)

# print(divided_data)

# def printPrecisionLevel(MPS = 0.75, PS = 0.25):
indicator = 3 # The nth field
MPP_standard = 0.75 # RTK signal should be equal or greater then MPS*100%
MPP = [] # Most precise points
PP_standard = 0.05 # PS
PP = [] # Precise points
RP = [] # The rest
# Evaluate the most precise points 
for idx, p in enumerate(divided_data):
    RTK = 0
    for row in p:
        if float(row[indicator]) == 4:
            RTK += 1
        # print(RTK)
    # if len(p) == 0:
    #     RP.append(idx) 
    if RTK / len(p) >= MPP_standard:
        MPP.append(idx)
    elif RTK / len(p) >= PP_standard:
        PP.append(idx)
    else:
        RP.append(idx)

print("MPP: ", MPP)
print("PP:  ", PP)
print("RP:  ", RP)
print()

# def printPrecisionLevel(0.75, 0.25)

# Yield vector <1, 0> and <0, 1> ---------------------------------------------
# Use pt1~5 to determine <1, 0> and pt23~27 to determine <0, 1>
# vecX the lat difference of 1 unit along x
# vecY the lon difference of 1 unit along y

# Average RTK coordinates
P = MPP + PP
avgdFile = 'Averaged copy.csv'
header = ['Lat', 'Lon', 'indicator', 'p_n'] # Theta field is not included
avgData = []
with open(avgdFile, 'r+', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    
    for index in P: # Each point
        sumLat = 0
        sumLon = 0
        n = 0
        for line in divided_data[index]: # Each line in a point
            if line[3] == '4':
                n += 1
                sumLat += float(line[0])
                sumLon += float(line[1])

        avgLat = round(sumLat / n, 7)
        avgLon = round(sumLon / n, 7)
        idctr = 4
        csv_writer.writerow([avgLat, avgLon, idctr, index + 1])
        avgData.append([avgLat, avgLon, idctr, index + 1])

avgData = np.array(avgData)
# print(avgData)
avgData = avgData[avgData[:, 3].argsort()]
# print(avgData)

# offset all the points
offset = [-avgData[0][1], -avgData[0][0]] # First row is supposed to be the point 0
print(f"offset: {offset}\n")

vecX = []
p = [1, 2, 3, 4, 5]
for i in p:
    r1 = avgData[avgData[:, 3] == i]
    r2 = avgData[avgData[:, 3] == i + 1]
    diffLat = round(r2[0][0] - r1[0][0], 7)
    diffLon = round(r2[0][1] - r1[0][1], 7)
    vecX.append([diffLon, diffLat])
    
# print(f"vecXs: {vecX}\n")

vecY = []
p = [23, 24, 25, 26, 27]
for i in p:
    r1 = avgData[avgData[:, 3] == i]
    r2 = avgData[avgData[:, 3] == i + 1]
    diffLat = round(r2[0][0] - r1[0][0], 7)
    diffLon = round(r2[0][1] - r1[0][1], 7)
    vecY.append([diffLon, diffLat])

# print(f"vecYs: {vecY}\n")

vecX = np.array(vecX)
vecY = np.array(vecY)
vecX = vecX / 5
vecY = vecY / 5
vecX = np.mean(vecX, axis=0)
vecY = np.mean(vecY, axis=0)
print(f"Averaged vecX: {vecX}\n")
print(f"Averaged vecY: {vecY}\n")
print(f"vecX dot vecY: {np.dot(vecX, vecY)}\n")

# Transform - <Lon, Lat> to a linear combination of vecX and vecY
# 1. Only averaged RTK points
basis = np.column_stack((vecX, vecY))
transFile = 'Transformed.csv'
header = ['X', 'Y', 'Lat', 'Lon', 'p_n']
# with open(transFile, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)
#     for row in avgData:
#         x = row[1]
#         y = row[0]
#         v = np.array([x + offset[0], y + offset[1]])
#         c1, c2 = np.linalg.solve(basis, v)
#         c1 = round(c1, 5)
#         c2 = round(c2, 5)
#         # print([c1, c2])
#         csv_writer.writerow([c1, c2, row[0], row[1], row[3]])

# 2. Raw data
# rawFile = 'processed_data_cleaned.csv'
# transFile = 'Transformed_All.csv'
# header = ['X', 'Y', 'Lat', 'Lon', 'HDT', 'indicator', 'p_n', 't_n']
# data = [] # The table to save the content
# with open(rawFile, newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     # Skip the header row
#     next(reader)
#     for row in reader:
#         numeric_row = [float(value) for value in row]
#         data.append(numeric_row)

# with open(transFile, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)
#     for row in data:
#         x = row[1]
#         y = row[0]
#         v = np.array([x + offset[0], y + offset[1]])
#         c1, c2 = np.linalg.solve(basis, v)
#         c1 = round(c1, 5)
#         c2 = round(c2, 5)
#         # print([c1, c2])
#         csv_writer.writerow([c1, c2, row[0], row[1], row[2], row[3], row[4], row[5]])

# 3. CompleteAvgWithXY.csv
# resFile = 'CompleteAvg.csv'
# transFile = 'CompleteAvgWithXY.csv'

# data = [] # The table to save the content
# with open(resFile, newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     # Skip the header row
#     next(reader)
#     for row in reader:
#         data.append(row)

# with open(transFile, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)
#     for row in data:
#         x = float(row[1])
#         y = float(row[0])
#         v = np.array([x + offset[0], y + offset[1]])
#         c1, c2 = np.linalg.solve(basis, v)
#         c1 = round(c1, 5)
#         c2 = round(c2, 5)
#         # print([c1, c2])
#         csv_writer.writerow([c1, c2, row[0], row[1], row[3]])