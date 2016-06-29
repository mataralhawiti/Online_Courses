'''
Created on Jun 29, 2016

@author: matar
'''

"""
Your task is to process the supplied file and use the csv module to extract data from it.
The data comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. You should extract the name of the station from it.

The data should be returned as a list of lists (not dictionaries).
You can use the csv modules "reader" method to get data in such format.
Another useful method is next() - to get the next line from the iterator.
You should only change the parse_file function.
"""


# import csv
# import os
# 
# 
# DATADIR = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/"
# DATAFILE = "745090.csv"
# 
# 
# def parse_file(datafile):
#     name = ""
#     data = []
#     
#     with open(datafile, 'rt') as f:
#         reader = csv.reader(f)
#         for r in reader:
#             if reader.line_num == 1 :
#                 name = r[1]
#             elif reader.line_num == 2:
#                 pass
#             else:
#                 data.append(r)
#     return (name, data)
# 
# 
# def test():
#     datafile = os.path.join(DATADIR, DATAFILE)
#     name, data = pasre_file(datafile)
#      
#     assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
#     assert data[0][1] == "01:00"
#     assert data[2][0] == "01/01/2005"
#     assert data[2][5] == "2"
#     
# 
# if __name__ == '__main__':
#     test()
    #pasre_file("/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/745090.csv")
    
    
    
    
    
    
    
    
    
    
    
    
    
import csv
import os

DATADIR = "/home/matar/GitHub/Online_Courses/Data_Wrangling_with_MongoDB/Lesson1/res/"
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    
    with open(datafile, 'rt') as f:
        reader = csv.reader(f)
        for r in reader:
            if reader.line_num == 1 :
                name = r[1]
            elif reader.line_num == 2:
                pass
            else:
                data.append(r)
                
#     with open(datafile,'rb') as f:
#         r = csv.reader(f)
#         name = r.next()[1]
#         header = r.next()
#         data = [row for row in r]

    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()