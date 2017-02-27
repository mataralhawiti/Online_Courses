# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/2013_ERCOT_Hourly_Load_Data.xls"
outfile = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    tem = None
    #print(sheet.ncols-1)
    ncols = 

    for i in range(sheet.ncols):
        if i == 0:
            pass
        else:
            Station = sheet.cell_value(0,i)
            #print(Station)
            cv = sheet.col_values(i, start_rowx=1, end_rowx=None)

            maxval = max(cv)
            #print(maxval)
            maxpos = cv.index(maxval) + 1
            maxtime = sheet.cell_value(maxpos, 0)
            realmaxtime = xlrd.xldate_as_tuple(maxtime, 0)

            #print(Station, maxval, maxtime, realmaxtime)
            list(data)
            tem = { 'Station' : Station, 
                    'Max Load': maxval,
                    'Year': realmaxtime[0],
                    'Month': realmaxtime[1],
                    'Day': realmaxtime[2],
                    'Hour': realmaxtime[3]}

            data.append(tem)
        # for i in data:
        #     print(i)

    #print(data[0].keys())
    
    fieldnames = ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']
    print(fieldnames)
    with open(outfile, 'w') as f:
        writer = csv.DictWriter(f,fieldnames, delimiter="|")
        writer.writeheader()
        for i in data:
            writer.writerow(i)


    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    # return data
parse_file(datafile)




"""


Station|Year|Month|Day|Hour|Max Load
COAST|2013|01|01|10|12345.6
EAST|2013|01|01|10|12345.6
FAR_WEST|2013|01|01|10|12345.6
NORTH|2013|01|01|10|12345.6
NORTH_C|2013|01|01|10|12345.6
SOUTHERN|2013|01|01|10|12345.6
SOUTH_C|2013|01|01|10|12345.6
WEST|2013|01|01|10|12345.6

"""








# def save_file(data, filename):
#     # YOUR CODE HERE

    
# def test():
#     open_zip(datafile)
#     data = parse_file(datafile)
#     save_file(data, outfile)

#     number_of_rows = 0
#     stations = []

#     ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
#                         'Year': '2013',
#                         'Month': '6',
#                         'Day': '26',
#                         'Hour': '17'}}
#     correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
#                         'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
#     fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

#     with open(outfile) as of:
#         csvfile = csv.DictReader(of, delimiter="|")
#         for line in csvfile:
#             station = line['Station']
#             if station == 'FAR_WEST':
#                 for field in fields:
#                     # Check if 'Max Load' is within .1 of answer
#                     if field == 'Max Load':
#                         max_answer = round(float(ans[station][field]), 1)
#                         max_line = round(float(line[field]), 1)
#                         assert max_answer == max_line

#                     # Otherwise check for equality
#                     else:
#                         assert ans[station][field] == line[field]

#             number_of_rows += 1
#             stations.append(station)

#         # Output should be 8 lines not including header
#         assert number_of_rows == 8

#         # Check Station Names
#         assert set(stations) == set(correct_stations)

        
# if __name__ == "__main__":
#     test()
