#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")

"""

oms_file = '/home/matar/Desktop/p003/Baltimore_MD.osm'


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if "uid" in element.attrib:
        	users.add(element.attrib["uid"])

    return users


if __name__ == "__main__":
	users = process_map(oms_file)
	print(len(users))
