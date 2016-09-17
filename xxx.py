import os
import time
import xml.etree.cElementTree as ET
import re
XML_FILE = open('ReportApplicationFeeList.xml','r').readlines()
'''

tree = ET.ElementTree(file=XML_FILE)
root = tree.getroot()


for child in root.iter():
    if len(child.attrib)>0:
        child.set('stage', 'no scann')
       
        if len(re.findall('[A-Z]{4}.?\d{6}.?0002.?\d{2}',child.attrib.get('RefNo','')))>0:
       

        
    
            print 'tag', child.tag
            print 'text',child.text
            print 'tail',child.tail
            print 'attrib',child.attrib
            print "get('textbox8','-----')",child.get('textbox8','-----')
            print ''
            print ''
            print ''
            print ''
            time.sleep(1)
tree.write('output.xml')
'''
