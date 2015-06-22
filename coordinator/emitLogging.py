__author__ = 'tonycastronova'
# import sys
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

            # todo: setup streamhandler to handle std.out
            # todo: https://docs.python.org/2/library/logging.handlers.html
# '''
#             sh_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] --- %(message)s')
#             sh = StreamHandler(sys.stdout)
#             sh.setFormatter(sh_formatter)
#             self.__root.addHandler(sh)
# '''
            # setup rotating log
            rotating_log = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000, backupCount=500)
            rotating_log.setFormatter(formatter)
            self.__root.addHandler(rotating_log)

        else:
            self.__dict__ = _Log.__monostate

    # def _set_stream_handler(self, stream):
    #     sh_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] --- %(message)s')
    #     sh = StreamHandler(stream)
    #     sh.setFormatter(sh_formatter)
    #     self.__root.addHandler(sh)

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

    def get_logger(self):
        return self.__root
log = _Log()
# Undo Tony's changes
# class StreamHandler(logging.StreamHandler):
#     """"""
#
#     def __init__(self, stream):
#
#         logging.StreamHandler.__init__(self)
#         self.stream = stream
#
#
#     def emit(self, record):
#         """Constructor"""
#         msg = self.format(record)
#         lvl = record.levelname
#
#         self.stream.write(msg+'\n')
#         self.flush()
#
#         # # # suppresses debug messages
#         # # if lvl == 'DEBUG':
#         # #     return
#         #
#         # self.stream.SetInsertionPoint(0)
#         # if lvl == 'INFO':
#         #     self.stream.BeginTextColour((0, 0, 0))
#         # elif lvl == 'ERROR':
#         #     self.stream.BeginTextColour((255, 0, 0))
#         # elif lvl == 'WARNING':
#         #     self.stream.BeginTextColour((255, 140, 0))
#         # else:
#         #     self.stream.BeginTextColour((50, 50, 50))
#         #
#         # self.stream.WriteText(msg + '\n')
#         # self.stream.EndTextColour()
#         # self.flush()
#
# class Log(object):
#
#     def __init__(self):
#         '''
#         :param target_control: Target control should be a wx.RichTextBox
#         :return:
#         '''
#         self.log = _Log()
#
#     def debug(self, text):
#         self.log._debug(text)
#
#     def warning(self, text):
#         self.log._warning(text)
#
#     def error(self, text):
#         self.log._error(text)
#
#     def info(self, text):
#         self.log._info(text)
#
#     def critical(self, text):
#         self.log._critical(text)
#
#     def get_logger(self):
#         return self.log._get_logger()
#     #
#     # def set_stream_handler(self, stream):
#     #     self.log._set_stream_handler(stream)
