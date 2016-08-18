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

OSMFILE = "chennai_india1.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]


# UPDATE THIS VARIABLE
mapping = { "St.": "Street",
            "St" : "Street",
            "Strret'": "Street",
            "Rd": "Road",
            'Rd' : "Road",
            "Ave.":"Avenue",
            "Ave" : "Avenue",
            "avenue":"Avenue",
            "street": "Street",
            "road": "Road",
            "nagar": "Nagar",
            "veedhi":"Street"
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
    #pprint.pprint(dict(street_types))
    return street_types


def update_name(name, mapping):
    # search for the street type (last word in street name)
    m = street_type_re.search(name)
    # if there is a street type:
    if m:
        # if the street type is in the mapping keys:
        if m.group() in mapping.keys():
            # replace the street type with the mapping equivalent
            name = name.replace(m.group(), mapping[m.group()])
    # return name
    return name


def test():
    st_types = audit(OSMFILE)
    print len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, way in st_types.iteritems():
        for name in way:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
                                                                                                                  
    for st_type, node in st_types.iteritems():
        for name in node:
            better_name = update_name(name, mapping)
            print name, "=>", better_name



if __name__ == '__main__':
    test()

print "############################################"   
print "055_data_v4.py"
print "############################################"  

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit_street import test, is_street_name
from audit_street import update_name





lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def is_address(elem):
    if elem.attrib['k'][:5] == "addr:":
        return True


def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way":
        address_info = {}
        nd_info = []
        pprint.pprint(element.attrib)
        node["type"] = element.tag
        node["id"] = element.attrib["id"]
        if "visible" in element.attrib.keys():
            node["visible"] = element.attrib["visible"]
        if "lat" in element.attrib.keys():
            node["pos"] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        node["created"] = {"version": element.attrib['version'],
                            "changeset": element.attrib['changeset'],
                            "timestamp": element.attrib['timestamp'],
                            "uid": element.attrib['uid'],
                            "user": element.attrib['user']}

        if address_info != {}:
            node['address'] = address_info
        for tag2 in element.iter("nd"):
            nd_info.append(tag2.attrib['ref'])
            print tag2.attrib['ref']
        if nd_info != []:
            node['node_refs'] = nd_info

        if 'address' not in node.keys():b 
            node['address'] = {}
        #Iterate the content of the tag
        for stag in element.iter('tag'):
            #Init the dictionry

            k = stag.attrib['k']
            v = stag.attrib['v']
            #Checking if indeed prefix with 'addr' and no ':' afterwards
            if k.startswith('addr:'):
                if len(k.split(':')) == 2:
                    content = addresschars.search(k)
                    if content:
                        node['address'][content.group(1)] = v
            else:
                node[k]=v
        if not node['address']:
            node.pop('address',None)
        #Special case when the tag == way,  scrap all the nd key
        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])
#         if  'address' in node.keys():
#             pprint.pprint(node['address'])

        return node
        
    else:
        return None


        

def process_map(file_in, pretty = False):
    """
    Process the osm file to json file to be prepared for input file to monggo
    """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('chennai_india1.osm', True)
    #pprint.pprint(data)

if __name__ == "__main__":
    test()