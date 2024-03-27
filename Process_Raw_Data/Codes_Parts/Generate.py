# This file is to generate faux HDTs
import csv
import numpy as np

# processedFile = 'processed_data_cleaned.csv'
# completeFile = 'complete_processed_data.csv'
# header = 'Lat, Lon, HDT, indicator, p_n, t_n'

processedFile = 'Transformed_All.csv'
completeFile = 'Transformed_All_complete.csv'
header = 'X, Y, Lat, Lon, HDT, indicator, p_n, t_n'

n_p = 44 # Number of points
HDTfield = 4 # Where the HDT is
t_nfield = 7

data = []
with open(processedFile, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)
    for row in csv_reader:
        numeric_row = [float(value) for value in row]
        data.append(numeric_row)

def angleConversion(h):
    # 0 <-> 45, 45 <-> 0, 90 <-> 315, 135 <-> 270, 180 <-> 225 ... 
    return (405 - h) % 360

data = np.array(data)
cnt_M1s = np.count_nonzero(data[:, HDTfield] == -1)

# Generate random values from a uniform distribution within the desired range
def generate_flat_random_numbers(num_samples, range_width):
    flat_values = np.random.uniform(low=-range_width/2, high=range_width/2, size=num_samples)
    flat_values -= np.mean(flat_values) # Adjust the values to have an average of zero
    rounded_values = np.round(flat_values, 3)
    return rounded_values

range_width = 2.6 # +-k -> 2k (+-1.3)
randNums = generate_flat_random_numbers(cnt_M1s, range_width)

n = 0
for row in data:
    if row[HDTfield] == -1:
        # Here the self-defined theta is converted to match HDT orientation
        row[t_nfield] = angleConversion(row[t_nfield])
        fauxHDT = row[t_nfield] + randNums[n]
        if fauxHDT < 0:
            fauxHDT = 360 + fauxHDT
        n += 1
        row[HDTfield] = fauxHDT

# print(data)

np.savetxt(completeFile, data, delimiter=',', header=header, fmt='%.8f', comments='')
print(f'NumPy array has been written to {completeFile}')