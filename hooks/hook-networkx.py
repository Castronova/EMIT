import os, sys
from glob import glob
from PyInstaller.utils.hooks import collect_data_files


# Add NetworkX data files
datas = collect_data_files('networkx')

nx_datas = glob(os.path.join(os.path.dirname(sys.executable), '../lib/python2.7/lib2to3/*.txt'))
for p in nx_datas:
    datas += [(p, './lib2to3')]

