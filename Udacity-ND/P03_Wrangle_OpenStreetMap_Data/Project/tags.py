#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""

oms_file = '/home/matar/Desktop/p003/Baltimore_MD.osm'


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')



def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            if lower.search(element.attrib['k']):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.search(element.attrib['k']):
                keys['problemchars'] = keys['problemchars'] + 1
            else:
                keys['other'] = keys['other'] + 1
    
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



# def test():
#     # You can use another testfile 'map.osm' to look at your solution
#     # Note that the assertion below will be incorrect then.
#     # Note as well that the test function here is only used in the Test Run;
#     # when you submit, your code will be checked against a different dataset.
#     keys = process_map('example.osm')
#     pprint.pprint(keys)
#     assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    keys = process_map(oms_file)
    print(keys)

    ''' {'other': 3581, 'lower': 336127, 'lower_colon': 1258410, 'problemchars': 0} '''
    '''{'lower_colon': 1258410, 'lower': 336127, 'other': 3579, 'problemchars': 2}'''
