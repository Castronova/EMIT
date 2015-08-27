__author__ = 'tonycastronova'
import sys
import logging
import logging.handlers
import os
import json
from environment import env_vars
import ConfigParser


class _Log:
    __monostate = None

    def __init__(self):
        if not _Log.__monostate:
            _Log.__monostate = self.__dict__

            current_dir = os.path.dirname(__file__)
            LOG_FILENAME = os.path.abspath(os.path.join(current_dir, '../log/EmitEngine.log'))
            CONSOLE_FILENAME = os.path.abspath(os.path.join(current_dir, '../log/temp_console_log.log'))

            # remove the temp console log
            if os.path.exists(CONSOLE_FILENAME):
                os.remove(CONSOLE_FILENAME)

            self.__root = logging.getLogger('EMIT ENGINE')
            self.__root.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # todo: setup streamhandler to handle std.out
            # todo: https://docs.python.org/2/library/logging.handlers.html

            sh_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] --- %(message)s')
            sh = StreamHandler(sys.stdout)
            sh.setFormatter(sh_formatter)
            self.__root.addHandler(sh)

            # setup rotating log
            rotating_log = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=50000, backupCount=500)
            rotating_log.setFormatter(formatter)
            self.__root.addHandler(rotating_log)


            # console log
            console_log = PickleHandler(CONSOLE_FILENAME)
            console_log.setFormatter(formatter)
            self.__root.addHandler(console_log)

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

    def _get_logger(self):
        return self.__root

class PickleHandler(logging.FileHandler):

    def __init__(self, filename, mode='a+b', encoding=None, delay=0):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)


    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()

        # create dictionary to store record info
        d = dict(message=record.message,
                 levelname=record.levelname,
                 asctime=record.asctime,
        )

        # dump record as json
        self.stream.write('\n'+json.dumps(d))
        self.flush()


class StreamHandler(logging.StreamHandler):
    """"""

    def __init__(self, stream):

        logging.StreamHandler.__init__(self)
        self.stream = stream


    def emit(self, record):
        """Constructor"""
        msg = self.format(record)
        lvl = record.levelname

        self.stream.write(msg+'\n')
        self.flush()


class Log(object):

    def __init__(self):
        '''
        :param target_control: Target control should be a wx.RichTextBox
        :return:
        '''
        self.settingspath = os.getcwd() + "/app_data/config/.settings.ini"
        self.config = ConfigParser.ConfigParser()

        self.log = _Log()
        self.verbosity()

    def debug(self, text):
        self.verbosity()
        if self.showdebug:
            self.log._debug(text)

    def warning(self, text):
        self.verbosity()
        if self.showwarning:
            self.log._warning(text)

    def error(self, text):
        self.verbosity()
        if self.showerror:
            self.log._error(text)

    def info(self, text):
        self.verbosity()
        if self.showinfo:
            self.log._info(text)

    def critical(self, text):
        self.verbosity()
        if self.showcritical:
            self.log._critical(text)

    def get_logger(self):
        return self.log._get_logger()

    def verbosity(self):
        #  Before every print, this method will check if it is allowed.
        self.showinfo = env_vars.LOGGING_SHOWINFO
        self.showwarning = env_vars.LOGGING_SHOWWARNING
        self.showcritical = env_vars.LOGGING_SHOWCRITICAL
        self.showerror = env_vars.LOGGING_SHOWERROR
        self.showdebug = env_vars.LOGGING_SHOWDEBUG

elog = Log()