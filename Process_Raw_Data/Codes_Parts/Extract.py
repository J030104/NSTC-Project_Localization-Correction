import os
import csv

dir_path = "0627_Log"
data_array = []

def extract_number_from_folder(folder_name):
    start = folder_name.find("(") + 1
    end = folder_name.find(")", start)
    return int(folder_name[start:end])

subdirectories = os.listdir(dir_path)
subdirectories = sorted(subdirectories, key=extract_number_from_folder)

for sub_dir in subdirectories: # Iterate through each subdirs
    sub_dir_path = os.path.join(dir_path, sub_dir)
    # print(sub_dir_path)
    sub_dir_data = []
    text_files = [f for f in os.listdir(sub_dir_path) if f.endswith('.txt')]
    
    for text_file in text_files: # Iterate through the text files
        file_path = os.path.join(sub_dir_path, text_file)
        
        with open(file_path, 'r') as file:
            file_content = file.readlines()
            sub_dir_data.append(file_content)

    data_array.append(sub_dir_data)

# Now, data_array contains a 2D array with the content of text files
# The number of subdirectories and text files is determined dynamically

def viewRaw(i, j):
    subdirectory_index = i
    text_file_index = j
    if subdirectory_index < len(data_array) and text_file_index < len(data_array[subdirectory_index]):
        print("Content of the selected text file:")
        print("".join(data_array[subdirectory_index][text_file_index]))
    else:
        print("Invalid indices chosen.")
        
# Iterate through the data_array
for i in range(len(data_array)):
    for j in range(len(data_array[i])):
        file_content = data_array[i][j]
        
        # Remove the last line
        file_content.pop()
        
        # Extract lines starting with $GNGGA or $GPHDT
        extracted_lines = [line for line in file_content if line.startswith('$GNGGA') or line.startswith('$GPHDT')]
        
        # Ensure the first line starts with $GNGGA and the last line with $GPHDT
        if not extracted_lines or not extracted_lines[0].startswith('$GNGGA'):
            extracted_lines.pop(0);
        if not extracted_lines or not extracted_lines[-1].startswith('$GPHDT'):
            extracted_lines.pop();
        
        # Ensure there are an even number of extracted lines
        if len(extracted_lines) % 2 != 0:
            print(f"Odd number of extracted lines in data_array[{i}][{j}].")
        # else:
        #     print("Success.")
        
        # Replace the element in data_array with the extracted lines
        data_array[i][j] = extracted_lines

# Convert dd.mmmmmmmmm... to dd.dddddddd
def ddm2ddd(n):
    d = int(n)
    m_in_d = (n - d) * 5 / 3 # *(100/60)
    return round(d + m_in_d, 8)

# Initialize a list to store the processed data
processed_data = []

# Iterate through data_array
for i in range(len(data_array)):
    
    for j in range(len(data_array[i])):
        file_content = data_array[i][j]
        n = len(file_content) 
        
        # Process pairs of lines starting with "$GNGGA" and "$GPHDT"
        for k in range(0, n, 2):
            if k + 1 < n and file_content[k].startswith('$GNGGA') and file_content[k + 1].startswith('$GPHDT'):
                gngga_line = file_content[k].split(',')
                gphdt_line = file_content[k + 1].split(',')
                
                # Extract the desired fields from $GNGGA and $GPHDT lines
                if len(gngga_line) >= 5 and len(gphdt_line) >= 3:
                    Lat = ddm2ddd(float(gngga_line[2]) / 100)
                    Lon = ddm2ddd(float(gngga_line[4]) / 100)
                    indicator = float(gngga_line[6])
                    HDT = float(gphdt_line[1]) if gphdt_line[1] else -1
                    
                    # Create a new line in the processed data
                    # point_no = i theta_no = j
                    processed_data.append([Lat, Lon, HDT, indicator, i + 1, j * 45])


output_csv_file = 'processed_data.csv'

with open(output_csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Lat', 'Lon', 'HDT', 'indicator', 'p_n', 't_n'])  # Add header , 't_x', 't_y', 't_t'
    csv_writer.writerows(processed_data)

print(f"The processed data has been saved to {output_csv_file}.")
