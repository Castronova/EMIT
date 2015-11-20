import cPickle as pickle
import sys

d = {}
with open('epsg_codes.csv','rU') as f:
    lines = f.readlines()
    for line in lines:
        values = line.split(',')
    
        if values[0] == '_':
            d[values[1].split(':')[1]] = values[2]
        else:
            d[values[0].split(':')[1]] = values[1]
            

        
pickle.dump(d, open('epsg_codes.dat','wb'))


print 'done'
