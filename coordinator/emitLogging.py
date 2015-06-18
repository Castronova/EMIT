__author__ = 'tonycastronova'
import logging
import logging.handlers

class _Log:
    __monostate = None

    def __init__(self):
        if not _Log.__monostate:
            _Log.__monostate = self.__dict__

            LOG_FILENAME = './Log/EmitEngine.log'

            self.__root = logging.getLogger('EMIT ENGINE')
            self.__root.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # setup file handler
            # fh = logging.FileHandler(LOG_FILENAME)
            # fh.setFormatter(formatter)
            # self.__root.addHandler(fh)

            # todo: setup streamhandler to handle std.out
            # todo: https://docs.python.org/2/library/logging.handlers.html
            # todo:

            # setup rotating log
            rotating_log = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000, backupCount=500)
            rotating_log.setFormatter(formatter)
            self.__root.addHandler(rotating_log)


        else:
            self.__dict__ = _Log.__monostate

    def debug(self, text):
        self.__root.debug(text)

    def warning(self, text):
        self.__root.warning(text)

    def error(self, text):
        self.__root.error(text)

    def info(self, text):
        self.__root.info(text)

    def critical(self, text):
        self.__root.critical(text)

log = _Log()

