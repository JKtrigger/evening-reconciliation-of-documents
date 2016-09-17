import os

import xml.etree.cElementTree as ET

XML_FILE = open('ReportApplicationFeeList.xml','r')


tree = ET.ElementTree(file=XML_FILE)
root = tree.getroot()
#print tree.getroot().tag
#print tree.getroot().attrib


'''for child_of_root in root:
    print child_of_root.tag
    print child_of_root.attrib
    print child_of_root.keys()
    print child_of_root.items()
    print child_of_root.get('textbox9')'''

for child_of_root in root.iter():
    print '-----------------'
    print child_of_root.tag
    print child_of_root.keys()
    print child_of_root.items()
print dir(child_of_root)