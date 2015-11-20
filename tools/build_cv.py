__author__ = 'tonycastronova'




import cPickle as pickle



# build unit cv archive
units = {}
with open('../data/units_cv.csv','rU') as f:
    lines = f.readlines()
    for line in lines:
        values = line.split(',')
        units[values[0].lower()] = [v.lower() for v in values[1:]]
pickle.dump(units,open('../data/units_cv.dat','wb'),protocol=pickle.HIGHEST_PROTOCOL)


# build variable cv archive
var = {}
with open('../data/variables_cv.csv','rU') as f:
    lines = f.readlines()
    for line in lines:
        values = line.split(',')
        var[values[0].lower()] = values[1]
pickle.dump(var,open('../data/var_cv.dat','wb'),protocol=pickle.HIGHEST_PROTOCOL)