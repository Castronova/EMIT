__author__ = 'tonycastronova'


import numpy as np
from numpy import genfromtxt

def trim(ti):

    with open(ti,'r') as f:
        ncols = int(f.readline().rstrip().split(' ')[-1])
        nrows = int(f.readline().rstrip().split(' ')[-1])
        xll = float(f.readline().rstrip().split(' ')[-1])
        yll = float(f.readline().rstrip().split(' ')[-1])
        cellsize = float(f.readline().rstrip().split(' ')[-1])
        nodata = int(f.readline().rstrip().split(' ')[-1])

    # read data
    my_data = genfromtxt(ti, delimiter=' ', skiprows=6)

    # trim top rows:
    rm_top = 0
    while 1:
        if max(my_data[0,:]) == nodata:
            my_data = np.delete(my_data,0,0)
            rm_top += 1
        else:
            break
    print 'trimmed %d lines from top of file'%rm_top

    # trim bottom rows:
    rm_bot = 0
    while 1:
        if max(my_data[-1,:]) == nodata:
            my_data = np.delete(my_data,-1,0)
            rm_bot += 1
        else:
            break
    print 'trimmed %d lines from bottom of file'%rm_bot

    # trim left cols
    rm_left = 0
    while 1:
        if max(my_data[:,0]) == nodata:
            my_data = np.delete(my_data,0,1)
            rm_left += 1
        else:
            break
    print 'trimmed %d lines from the left of file'%rm_left

    # trim right cols
    rm_right = 0
    while 1:
        if max(my_data[:,-1]) == nodata:
            my_data = np.delete(my_data,-1,1)
            rm_right += 1
        else:
            break
    print 'trimmed %d lines from the right of file'%rm_right

    print 'done'


    # recalculate xll and yll
    xll += cellsize*rm_left
    yll += cellsize*rm_bot
    ncols -= (rm_left + rm_right)
    nrows -= (rm_top+rm_bot)

    print 'recalculated header: '
    print 'ncols %d'%ncols
    print 'nrows %d'%nrows
    print 'xll %3.8f'%xll
    print 'yll %3.8f'%yll

    with open(ti.split('.')[0]+'_trim.txt','w') as f:
        f.write('ncols %d\n'%ncols)
        f.write('nrows %d\n'%nrows)
        f.write('xllcorner %3.8f\n'%xll)
        f.write('yllcorner %3.8f\n'%yll)
        f.write('cellsize %3.8f\n'%cellsize)
        f.write('nodata %3.3f\n'%nodata)

        np.savetxt(f, my_data, delimiter=" ", fmt="%3.3f")

trim('right_hand_fork_ti.txt')
trim('fac.txt')