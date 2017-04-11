#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET

'''
SAX parser/ iterative pasrsing .. Lesson 3

'''

oms_file = '/home/matar/Desktop/p003/Baltimore_MD.osm'

def count_tags(filename):
	tags = {}
	iterparse = ET.iterparse(filename)
	for event, elemet in iterparse:
		if elemet.tag in tags :
			tags[elemet.tag] += 1
		else :
			tags[elemet.tag] = 1
	return tags

if __name__ == "__main__":
    tags = count_tags(oms_file)
    print(tags)

'''
{'bounds': 1, 'way': 250595, 'osm': 1, 'relation': 851, 'nd': 2346656, 'node': 1800900, 'tag': 1598118, 'member': 17730}

'''


'''
https://docs.python.org/3.4/library/xml.etree.elementtree.html
http://stackoverflow.com/questions/12792998/elementtree-iterparse-strategy
http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
https://sqlite.org/cli.html

'''