# -​*- mode: python -*​-
import sys
from glob import glob
import os
from os.path import *

#from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs



"""
NOTES:

exclude PyQt4, PyQt4.QtCore, PyQt4.QtGui.  these are optional libraries that matplotlib will include, but we are not developing with PyQt so they are not needed.
"""

block_cipher = None

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

a = Analysis(['./EMIT.py'],
            pathex=['./Mac'],
            binaries=None,
            datas=None,
            hiddenimports=[],
            hookspath=['./hooks'], 
            runtime_hooks=None,
            excludes=['PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui'],
            win_no_prefer_redirects=None,
            win_private_assemblies=None,
            cipher=block_cipher)

dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

# add app_data directory
d = Tree(abspath(join(os.getcwd(), 'app_data')), prefix='app_data')
a.datas += d

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
         a.scripts,
         exclude_binaries=True,
         name='emit',
         debug=False,
         strip=None,
         upx=True,
         console=False , version="0.1.5")

coll = COLLECT(exe,
              a.binaries,
              a.zipfiles,
              a.datas,
              strip=None,
              upx=True,
              name='emit')
app = BUNDLE(coll,
            name='emit.app',
            icon=None,
            bundle_identifier=None)
