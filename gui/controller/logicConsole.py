__author__ = 'Francisco'

import os

class logicConsole():
    def __init__(self):

        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/EmitEngine.log'))
        file = self.readFile(connections_txt)
        file.close()

    def readFile(self, filepath):
        file = open(filepath, 'r')
        lineList = file.readlines()  # readlines() returns a list, each line is an element in the list
        print "The last line is: "
        print lineList[-1]
        lastLine = lineList[-1]
        self.parseLine(lastLine)
        return file

    def parseLine(self, line):
        if 'INFO' in line:
            print "Info is in the line"
            print line.find('~')
        else:
            print "info not found"
        pass