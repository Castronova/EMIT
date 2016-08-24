# -*- mode: python -*-
import os
from os.path import *
block_cipher = None


a = Analysis(['EMIT.py'],
             pathex=['C:\\Users\\Francisco\\Work\\EMIT'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('./app_data/db/.dbload', './app_data/db/.dbload', 'DATA')]
a.datas += [("./app_data/dat/wofsites.json", "./app_data/dat/wofsites.json", "DATA")]
d = Tree(abspath(join(os.getcwd(), 'app_data')), prefix='app_data')
a.datas += d

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='EMIT',
          icon='.\\app_data\\img\\windows_icon.ico',
          debug=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='EMIT')
