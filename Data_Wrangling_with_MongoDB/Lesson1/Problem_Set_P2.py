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

# datafile = "2013_ERCOT_Hourly_Load_Data.xls"
# outfile = "2013_Max_Loads.csv"


datafile = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/2013_ERCOT_Hourly_Load_Data.xls"
outfile = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []

    # ncols = sheet.ncols
    # for i in range(ncols):
    # if i in (0, 9):
    #     pass

    # pass columns 0 & 9    
    for i in range(1,9): # start at 1, and finish at 8
        Station = sheet.cell_value(0,i)
        cv = sheet.col_values(i, start_rowx=1, end_rowx=None)

        maxval = max(cv)
        maxpos = cv.index(maxval) + 1
        maxtime = sheet.cell_value(maxpos, 0)
        realmaxtime = xlrd.xldate_as_tuple(maxtime, 0)

        tem = { 'Station' : Station, 
                'Max Load': maxval,
                'Year': realmaxtime[0],
                'Month': realmaxtime[1],
                'Day': realmaxtime[2],
                'Hour': realmaxtime[3]}

        data.append(tem)
    return data

def save_file(data, filename):
    print("data is ", repr(data))
    fieldnames = ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f,fieldnames, delimiter="|")
        #writer = csv.Writer(f,fieldnames, delimiter="|")
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)


    
def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()

# ------------------ solution from Udacity
# def parse_file(datafile):
#     workbook = xlrd.open_workbook(datafile)
#     sheet = workbook.sheet_by_index(0)
#     data = {}
#     # process all rows that contain station data
#     for n in range (1, 9):
#         station = sheet.cell_value(0, n)
#         cv = sheet.col_values(n, start_rowx=1, end_rowx=None)

#         maxval = max(cv)
#         maxpos = cv.index(maxval) + 1
#         maxtime = sheet.cell_value(maxpos, 0)
#         realtime = xlrd.xldate_as_tuple(maxtime, 0)
#         data[station] = {"maxval": maxval,
#                          "maxtime": realtime}

#     print data
#     return data

# def save_file(data, filename):
#     with open(filename, "w") as f:
#         w = csv.writer(f, delimiter='|')
#         w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
#         for s in data:
#             year, month, day, hour, _ , _= data[s]["maxtime"]
#             w.writerow([s, year, month, day, hour, data[s]["maxval"]])



