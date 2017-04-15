"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#OSMFILE = "example.osm"
oms_file = '/home/matar/Desktop/p003/Baltimore_MD.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
post_code_re = re.compile(r'^[0-9]{5}(?:-[0-9]{4})?$')



expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Highway", "Alley", "Terrace", "Broadway", "Pass", "Plaza", 
            "Circle", "Way", "Walk", "Alameda", "Northway", "Fallsway", "Freeway", "Kerneway", "Center",
            "East", "Westway", "Kinsway", "Run", "Strand", "Gardens", "Juneway", "Off", "Greenway", 
            "Southway", "Eastway", "Mews", "Townway"]


# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "st" : "Street",
            "St.": "Street",
            "st.": "Street",
            "Ave" : "Avenue",
            "Hwy" : "Highway"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    # handle incorrect street names
    if name == "Saint Clair Crossing Crossing" or name == "Saint Clair Crossing":
        return "Saint Clair Crossing"
    elif name == "Oldtown Mall" :
        return "Oldtown Mall"
    elif name == "East Lighthouse Point" :
        return "Lighthouse Point East"
    elif name == "28th & Sisson" :
        return "W 28th Street & Sisson Street"
    elif name == "Nelway" :
        return "Nelway Avenue"
    elif name == "Pilgrim Landing" :
        return "Pilgrim Road"
    elif name == "Guilford Avenue # 735" :
        return "735 Guilford Avenue"
    elif name == "Linden Green" :
        return "Linden Green"
    elif name == "Seamon-alley-potee" or name == "Washington-carroll" :
        return "Unkown street name"
    else :
        pass

    # handle correct street names with inaccurate prefex
    name = name.split(' ')
    st_type = name[-1]

    if st_type in mapping:
        name[-1] = mapping[st_type]
        name = ' '.join(name)
        return name
    else:
        return  ' '.join(name)


# postcode audting 
def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    post_codes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode":
                    if (not post_code_re.match(tag.attrib['v'])) or (int(tag.attrib['v']) not in range(21201, 21299)) : #< 21201 or int(tag.attrib['v']) > 21298:
                        post_codes.add(str(tag.attrib['v']))
    osm_file.close()
    return post_codes


def update_postcode(post_code):
    if post_code in ('21090', '20002', '01239','21209;21230') :
        return '00000'



if __name__ == '__main__':

    # test street audit
    # streets = audit_street(oms_file)
    # for st_type, street in streets.items():
    #     print(st_type, street)

    # test update street name
    # streets = audit_street(oms_file)
    # for st_type, street in streets.items():
    #     for st_name in street :
    #         better_name = update_name(st_name, mapping)
    #         print(st_name, "=>", better_name)


    # test audit postcode
    # postcodes = audit_postcode(oms_file)
    # for pc in postcodes :
    #     print(pc)

    # test update postcode
    # postcodes = audit_postcode(oms_file)
    # for pc in postcodes :
    #     new_pc = update_postcode(pc)
    #     print(new_pc)


