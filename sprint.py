__author__ = 'tonycastronova'

from os.path import *
import inspect
from socket import AF_INET, SOCK_DGRAM, socket


def get_open_port():
    """
    Resolves an available port for socket messages
    Returns: available port number
    """

    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(("localhost",0))
    port = s.getsockname()[1]
    s.close()
    return port


class SocketBinding:
    """
    Borg pattern to make sure that ports are only bound once per instance of the application
    """
    __monostate = None
    def __init__(self):
        if not SocketBinding.__monostate:
            SocketBinding.__monostate = self.__dict__

            # resolve the bindings ( This should be extended to include all print targets)
            self.sockets = {'CONSOLE':get_open_port()}

        else:
            self.__dict__ = SocketBinding.__monostate

# try to bind to this CONSOLE address.  This will happen at first import
sbindings = SocketBinding()

class PrintTarget:
    """
    Enum for the socket ports for each print method
    """
    CONSOLE = sbindings.sockets['CONSOLE']

class MessageType:
    """
    Enum for the types of messages that are recognized
    """
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    INFO = 'INFO'
    CRITICAL = 'CRITICAL'

def getStackTrace():
    """
    Gets the function caller via stack tracing
    Returns: "(caller, line #)"
    """
    stack = inspect.stack()
    return '(%s, line %s)' % (basename(stack[2][1]), stack[2][2])

def sPrint(text,  messageType=MessageType.INFO, printTarget=PrintTarget.CONSOLE):
    '''
    Sends text to a socket
    :param text: the message to send
    :param messageType: the type of message (MessageType)
    :param printTarget: the target port (PrintTarget)
    :return: None
    '''

    host = 'localhost'
    port = printTarget
    addr = (host, port)
    udpsocket = socket(AF_INET, SOCK_DGRAM)

    # add a stack trace if this a debug message
    caller = ''
    if messageType == MessageType.DEBUG:
        caller = getStackTrace()

    text = str(text) if type(text) != str else text
    text = '%s %s' % (text, caller)
    udpsocket.sendto('|'.join([messageType,text]), addr)

class dBlock():
    def __init__(self, title, port=PrintTarget.CONSOLE):

        self.addr = ('localhost', port)
        self.udpsocket = socket(AF_INET, SOCK_DGRAM)
        self.title_length = 42 + len(title)

        # print header
        header_msg = '%s %s %s' % (20*'-', title, 20 * '-')
        self.udpsocket.sendto('|'.join([MessageType.DEBUG,header_msg]), self.addr)

    def sPrint(self, text):

        # get the calling file so that it can be appended to the message
        caller = getStackTrace()

        # parse the text
        text = str(text) if type(text) != str else text
        text = '-> %s %s' % (text, caller)
        # send the message
        self.udpsocket.sendto('|'.join([MessageType.DEBUG,text]), self.addr)

    def close(self):
        footer_msg = self.title_length * '-'
        self.udpsocket.sendto('|'.join([MessageType.DEBUG, footer_msg]), self.addr)
        del self
