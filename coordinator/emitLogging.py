import inspect
import logging
import logging.handlers
import os
import sys
from os.path import *

from utilities import io


class _Log:
    __monostate = None

    def __init__(self):
        if not _Log.__monostate:
            _Log.__monostate = self.__dict__

            app_data = io.getAppDataDir()
            LOG_FILENAME = abspath(join(app_data, 'log/engine.log'))

            # make sure this path exists
            if not exists(dirname(LOG_FILENAME)):
                os.mkdir(dirname(LOG_FILENAME))

            self.__root = logging.getLogger('EMIT ENGINE')
            self.__root.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)s --- %(message)s')
            sh_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] --- %(message)s')
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(sh_formatter)
            self.__root.addHandler(sh)

            # setup rotating log
            rotating_log = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=50000000, backupCount=500)
            rotating_log.setFormatter(formatter)
            self.__root.addHandler(rotating_log)

        else:
            self.__dict__ = _Log.__monostate

    def _debug(self, text):
        self.__root.debug(text)

    def _warning(self, text):
        self.__root.warning(text)

    def _error(self, text):
        self.__root.error(text)

    def _info(self, text):
        self.__root.info(text)

    def _critical(self, text):
        self.__root.critical(text)

class Log(object):

    def __init__(self):
        '''
        :param target_control: Target control should be a wx.RichTextBox
        :return:
        '''

        self.log = _Log()

    def debug(self, text):
        if os.environ['LOGGING_SHOWDEBUG']:
            self.log._debug(text)

    def warning(self, text):
        if os.environ['LOGGING_SHOWWARNING']:
            self.log._warning(text)

    def error(self, text):
        f = inspect.getouterframes(inspect.currentframe(),2)
        detailed_text = " [%s, %s (line %d)] --- %s " % (f[1][1].split('/')[-1], f[1][3], f[1][2], text)
        if os.environ['LOGGING_SHOWERROR']:
            self.log._error(detailed_text)

    def info(self, text, overwrite=False):
        if os.environ['LOGGING_SHOWINFO']:
            text = 'OVERWRITE:%s'%text if overwrite else text
            self.log._info(text)

    def critical(self, text):
        if os.environ['LOGGING_SHOWCRITICAL']:
            self.log._critical(text)


elog = Log()