'''
Created on Jun 25, 2016

@author: matar
'''


#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
datafile = "/home/matar/GitHub/Data_Wrangling_with_MongoDB/Lesson1/res/2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    # get colmn 1 values in a list
    cv = sheet.col_values(1, start_rowx=1, end_rowx=None)

    maxval = max(cv)
    minval = min(cv)
    
    maxpos = cv.index(maxval)+1 # be aware of +1
    minpos = cv.index(minval)+1
    
    maxtime = sheet.cell_value(maxpos, 0)
    realmaxtime = xlrd.xldate_as_tuple(maxtime, 0)
    mintime = sheet.cell_value(minpos, 0)
    realmintime = xlrd.xldate_as_tuple(mintime, 0)
#----- my answer : it's correct but kinda complex    
#     maxtime = None
#     maxvalue= max(sheet.col_values(1, start_rowx=1))
#     mintime=None
#     minvalue=min(sheet.col_values(1, start_rowx=1))
#     avgcoast=sum((sheet.col_values(1, start_rowx=1))) / (sheet.nrows-1)
#     
#     for row in range(sheet.nrows):
#         for col in range(sheet.ncols):
#             if col == 1 and sheet.cell_value(row,col) == maxvalue :
#                 #print(row,col)
#                 #print(sheet.cell_value(row,col-1))
#                 #print(xlrd.xldate_as_tuple(sheet.cell_value(row,col-1), 0))
#                 maxtime = xlrd.xldate_as_tuple(sheet.cell_value(row,col-1), 0)
#                 break
#     
#     for row in range(sheet.nrows):
#         for col in range(sheet.ncols):
#             if col == 1 and sheet.cell_value(row,col) == maxvalue :
#                 #print(row,col)
#                 #print(sheet.cell_value(row,col-1))
#                 #print(xlrd.xldate_as_tuple(sheet.cell_value(row,col-1), 0))
#                 mintime = xlrd.xldate_as_tuple(sheet.cell_value(row,col-1), 0)
#                 break
            

    
    
    data = {
            'maxtime': realmaxtime,
            'maxvalue': maxval,
            'mintime': realmintime,
            'minvalue': minval,
            'avgcoast': sum(cv) / float(len(cv))
    }
    return data

#parse_file(datafile)

def test():
    #open_zip(datafile)
    import pprint as p
    data = parse_file(datafile)
    p.pprint(data)
 
    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)
 

test()