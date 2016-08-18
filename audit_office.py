"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected office types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the office name.
    The function takes a string with office name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "chennai_india1.osm"
office_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Government", "Administrative", "Company", "Alumni Affairs", "Court", "Transparent Chennai"]


# UPDATE THIS VARIABLE
mapping = { "government": "Government",
            "administrative" : "Administrative",
            "it'": "Information Technology",
            "educational_institution": "Educational Institution",
            'telecommunication' : "Telecommunication Office",
            "estate_agent":"Estate Agent Office",
            "research" : "Research",
            "company":"Company",
            "financial": "Financial Institution",
            "insurance": "Insurance",
            "lawyer": "Law firm",
            "television network":"Television Network Station",
            "iSOFT": "Information Technology",
            "ngo": "NGO",
            }


def audit_office_type(office_types, office_name):
    m = office_type_re.search(office_name)
    if m:
        office_type = m.group()
        if office_type not in expected:
            office_types[office_type].add(office_name)


def is_office_name(elem):
    return (elem.attrib['k'] == "office")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    office_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_office_name(tag):
                    audit_office_type(office_types, tag.attrib['v'])
    osm_file.close()
    #pprint.pprint(dict(office_types))
    return office_types

"""
def update_name(name, mapping, regex):
      m = regex.search(name)
      if m:
          office_type = m.group()
          if office_type in mapping:
              name = re.sub(regex, mapping[office_type], name)
      return name

     

def update_name(name, mapping):
    dict_map = sorted(mapping.keys(), key=len, reverse=True)
    for key in dict_map:
        if name.find(key) != -1:
            name = name.replace(key,mapping[key])
            return name

"""

def update_name(name, mapping):
    # search for the office type (last word in office name)
    m = office_type_re.search(name)
    # if there is a office type:
    if m:
        # if the office type is in the mapping keys:
        if m.group() in mapping.keys():
            # replace the office type with the mapping equivalent
            name = name.replace(m.group(),mapping[m.group()])
    # return name
    return name


def test():
    of_types = audit(OSMFILE)
    print len(of_types) == 3
    pprint.pprint(dict(of_types))

    for of_type, way in of_types.iteritems():
        for name in way:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
                                                                                                                  
    for of_type, node in of_types.iteritems():
        for name in node:
            better_name = update_name(name, mapping)
            print name, "=>", better_name



if __name__ == '__main__':
    test()
