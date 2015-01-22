__author__ = 'Mario'
import xml.etree.ElementTree as et
def main():
    path = 'C:\\Users\\Mario\\Documents\\Projects\\EMIT\\tests\\data\\DatabaseSave.sim'
    Load(path)

def Load(path):
    tree = et.parse(path)

    root = tree.getroot()
    model = root._children[0]._children
    dataModel = root._children[1]._children
    link = root._children[2]._children
    DbConnection = root._children[3]._children

    modeldict = {}
    # for i in range(len(model)):
    modelname = model[0].text
    modelid = model[1].text
    xcoor = model[2].text
    ycoor = model[3].text
    modelpath = model[4].text

    # for i in range(len(dataModel)):
    dataModelname = dataModel[0].text
    dataModelid = dataModel[1].text
    dataModelxcoor = dataModel[2].text
    dataModelycoor = dataModel[3].text
    dataModelDBid = dataModel[4].text
    dataModelresultid = dataModel[5].text

    
    print root

if __name__ == '__main__':
    main()