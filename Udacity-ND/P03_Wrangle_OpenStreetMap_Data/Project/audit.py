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


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Highway", "Alley", "Terrace", "Broadway", "Pass", "Plaza", 
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


def audit(osmfile):
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
    else:
        pass

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name)
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    streets = audit(oms_file)
    for st_type, street in streets.items():
        for st_name in street :
            better_name = update_name(st_name, mapping)
            print(st_name, "=>", better_name)
        # print(st_type, street)





'''
https://www.wikiwand.com/en/Types_of_road
'''

'''

Alameda {'The Alameda'}
Northway {'Northway', 'Loyola Northway'}
Mall {'Oldtown Mall'}
Hwy {'Broening Hwy'}
Southway {'Loyola Southway', 'Southway', 'Homeland Southway'}
Crossing {'Saint Clair Crossing Crossing', 'Saint Clair Crossing'}
Sisson {'28th & Sisson'}
Fallsway {'Fallsway'}
Eastway {'Eastway'}
Freeway {'Freeway'}
st. {'W. Pratt st.'}
Kerneway {'Kerneway'}
Ave {'Maryland Ave', 'Guilford Ave', 'Eastern Ave'}
Townway {'Townway'}
Center {'Freeport Center'}
East {'Lighthouse Point East'}
Westway {'Westway'}
Seamon-alley-potee {'Seamon-alley-potee'}
Kinsway {'Kinsway'}
Run {'Friar Field Run'}
Strand {'The Strand'}
Landing {'Pilgrim Landing'}
Gardens {'Goodwood Gardens'}
Mews {'Balmar Mews', 'Station North Mews', 'Foundry Mews'}
Nelway {'Nelway'}
Juneway {'Juneway'}
735 {'Guilford Avenue # 735'}
Washington-carroll {'Washington-carroll'}
Off {"O'Donnell Street Cut Off"}
st {'north kresson st'}
Green {'Linden Green'}
St. {'N. Charles St.'}
Point {'East Lighthouse Point'}
Greenway {'Greenway'}

------------

Seamon-alley-potee {'Seamon-alley-potee'}
St. {'N. Charles St.'}
Landing {'Pilgrim Landing'}
st. {'W. Pratt st.'}
st {'north kresson st'}
Eastway {'Eastway'}
735 {'Guilford Avenue # 735'}
Nelway {'Nelway'}
Green {'Linden Green'}
Mews {'Foundry Mews', 'Balmar Mews', 'Station North Mews'}
Crossing {'Saint Clair Crossing', 'Saint Clair Crossing Crossing'}
Point {'East Lighthouse Point'}
Townway {'Townway'}
Mall {'Oldtown Mall'}
Ave {'Guilford Ave', 'Eastern Ave', 'Maryland Ave'}
Washington-carroll {'Washington-carroll'}
Hwy {'Broening Hwy'}
Sisson {'28th & Sisson'}
Southway {'Homeland Southway', 'Loyola Southway', 'Southway'}


--------

Townway {'Townway'}
Sisson {'28th & Sisson'}
st {'north kresson st'}
Crossing {'Saint Clair Crossing', 'Saint Clair Crossing Crossing'}
735 {'Guilford Avenue # 735'}
Point {'East Lighthouse Point'}
Seamon-alley-potee {'Seamon-alley-potee'}
Washington-carroll {'Washington-carroll'}
Mall {'Oldtown Mall'}
Green {'Linden Green'}
Nelway {'Nelway'}
Hwy {'Broening Hwy'}
Landing {'Pilgrim Landing'}
Ave {'Eastern Ave', 'Guilford Ave', 'Maryland Ave'}
St. {'N. Charles St.'}
st. {'W. Pratt st.'}




'''