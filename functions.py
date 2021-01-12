import csv
import numpy as np

def parse(n,length):
    with open('Crimes_History.csv') as file:
        csv_reader = csv.reader(file, delimiter = ",")
        result_count = 0
        line_count = 0
        lat = []
        long = []
        for row in csv_reader:
            if result_count > length:
                break
            if line_count == 0:
                line_count += 1
                continue
            if line_count > 0:
                if row[19] not in (None, ""):
                    lat.append(float(row[19]))
                    long.append(float(row[20]))
#                    print(f'\t{row[19]},{row[20]}')
                    line_count += 1
                    result_count += 1
    if n == 19:
        return(lat)
    elif n == 20:
        return(long)

def write(n):
	result = {}
	for i in range(1,n+1):
		if i%3 == 1:
			result[i] = 'r'
		elif i%3 == 2:
			result[i] = 'g'
		elif i%3 == 0:
			result[i] = 'b'
	return(result)
