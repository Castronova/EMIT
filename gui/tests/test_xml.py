__author__ = 'tonycastronova'


import xml.etree.ElementTree as et
from xml.dom import minidom


def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

tree = et.Element('Simulation')

attributes = {'Name':'mymodel','path':'/some/path1','x':'10','y':'100'}
et.SubElement(tree,'Model',attributes)

attributes = {'Name':'mymodel2','path':'/some/path2','x':'20','y':'200'}
et.SubElement(tree,'Model',attributes)

attributes = {'From':'mymodel','To':'mymodel2','FromItem':'variable1','ToItem':'variable2'}
et.SubElement(tree,'Link',attributes)

prettyxml = prettify(tree)

with open('/Users/tonycastronova/Documents/projects/iUtah/EMIT/gui/tests/test.xml','w') as f:
    f.write(prettyxml)

print 'done'