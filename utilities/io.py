'''
Functions to perform I/O operations that support dev and installed environments
'''

import sys
from os.path import *

def getAppDataDir():
    
    # attempt to get the path using the development folder hierarchy
    utils_dir = dirname(abspath(__file__))
    app_path = abspath(join(utils_dir, '../app_data'))
    
    # if path doesn't exist, try installed directory
    if not exists(app_path):
        if getattr(sys, 'frozen', False):
            app_path = abspath(join(sys._MEIPASS, 'app_data'))
        else:
            raise Exception('Could Not Find app_data Path')
    
    return app_path

def getRelativeToAppData(relative_path):

    app_data = getAppDataDir()

    return abspath(join(app_data, relative_path))

