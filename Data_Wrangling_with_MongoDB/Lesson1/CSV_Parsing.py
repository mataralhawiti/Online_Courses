'''
Created on Jun 23, 2016

@author: matar
'''

import os
import csv
import pprint


DATADIR = "/home/matar/GitHub/Data_Wrangling_with_MongoDB/Lesson1/res"
DATAFILE = "beatles-diskography.csv"

def parse_csv(datafile):
    data = []
    with open(datafile, 'rt') as f:
        reader = csv.DictReader(f)
        for line in reader:
            data.append(line)
        return data
    

if __name__ == '__main__' :
    path = os.path.join(DATADIR, DATAFILE)
    parse = parse_csv(path)
    pprint.pprint(parse)
    exit()


class Matar():
    def __init__(self):
        pass
    