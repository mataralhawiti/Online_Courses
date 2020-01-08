'''
Created on Jun 23, 2016

@author: matar
'''

import xlrd

datafile = "/home/matar/GitHub/Data_Wrangling_with_MongoDB/Lesson1/res/2013_ERCOT_Hourly_Load_Data.xls"


def parse_file(datafile):
    # open workbook
    workbood = xlrd.open_workbook(datafile)
    
    # open first sheet
    sheet = workbood.sheet_by_index(0)
    
    data = [[sheet.cell_value(r, c)
             for c in range(sheet.ncols)]
                for r in range(sheet.nrows)]

    
    
    
    print("\nList Comprehension:")
    print("data[3][2] : row 3 , col 2")
    print(data[3][2])
    print("----------------------------------------------------------")
    
    
    print("\nCells in nested loop to print all cols values for specific row")
    for row in range(sheet.nrows):
        for col in range(sheet.ncols) :
            if row == 50:
                # print all cols values
                print(sheet.cell_value(row, col))
                
    print("----------------------------------------------------------")

    print("\nSome useful functions")
    
    print("\nNumber of rows in the sheet")
    print(sheet.nrows)
    
    print("\nNumber of cols in the sheet")
    print(sheet.ncols)

    print("\nData type in cell (row 3, col 2)")
    print(sheet.cell_type(3,2))
    
    print("\ncell value (row 3, col 2)")
    print(sheet.cell_value(3,2))
    
    print("\nGet a slice of values in column 3, from rows 1-3:")
    print(sheet.col_values(3, start_rowx=1, end_rowx=4))
    print(sheet.col_values(3, start_rowx=1))
    print(max(sheet.col_values(3, start_rowx=1)))
    print(max(sheet.col_values(3, start_rowx=1)))
    print(sum(sheet.col_values(3, start_rowx=1)))



    
    
    
    print("\nDATES:")
    print("Type of data in cell (row 1, col 0):")
    print(sheet.cell_type(1, 0)) # type 3 >> date !
    
    exceltime = sheet.cell_value(1, 0)
    print ("Time in Excel format:")
    print (exceltime) # Excel float !!!
    print ("Convert time to a Python datetime tuple, from the Excel float:")
    print (xlrd.xldate_as_tuple(exceltime, 0)) # Jan-1-2013 1:00 clock
    
    return data

    
    
       

parse_file(datafile)

# import sys
# for pth in sys.path:
#     print(pth)