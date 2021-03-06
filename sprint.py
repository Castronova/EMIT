__author__ = 'tonycastronova'

import os
from os.path import *
import inspect
from socket import AF_INET, SOCK_DGRAM, socket
import environment

def get_open_port():
    """
    Resolves an available port for socket messages
    Returns: available port number
    """


    environment.getEnvironmentVars()
    try:
        # get the port number from the settings file
        port = int(os.environ['APP_CONSOLE_SOCKET'])
    except KeyError:
        # set the port to 0 if it is not found in the settings file.  This will make the socket library find an open port.
        port = 0

    try:
        s = socket(AF_INET, SOCK_DGRAM)

        # attempt to bind to the port
        s.bind(("localhost", port))

        # get the port number from the socket
        port = s.getsockname()[1]

        # always close the socket.  This allows the gui console to bind to it later (see caveat below)
        s.close()

        # save this port back to the environment vars
        environment.setEnvironmentVar('APP','CONSOLE_SOCKET',port)
    except:
        # an error is raised if the gui has bound to this address before the engine tries to.
        # ignore this error for now, however we should wait until sprint has resolved socket
        # ports before allowing the gui to bind to it.
        pass

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
    Returns: "(caller, line #, depth)"
    """
    stack = inspect.stack()

    # filter stack trace element that do not contain EMIT
    filtered = [i[1] for i in stack if 'EMIT' in i[1]]
    depth = len(filtered) - 2

    return (basename(stack[2][1]), stack[2][2], depth)

def sPrint(text,  messageType=MessageType.INFO, printTarget=PrintTarget.CONSOLE):
    '''
    Sends text to a socket
    :param text: the message to send
    :param messageType: the type of message (MessageType)
    :param printTarget: the target port (PrintTarget)
    :return: None
    '''

    # reload(os)
    logs = [v for k,v in os.environ.iteritems() if 'LOGGING' in k]

    host = 'localhost'
    port = printTarget
    addr = (host, port)
    udpsocket = socket(AF_INET, SOCK_DGRAM)

    # add a stack trace if this a debug message
    debug_text = ''
    indent = ''

    # format DEBUG messages i.e. "--> my message (file.py, line 1003)
    if messageType == MessageType.DEBUG:
        caller = getStackTrace()
        indent = '-'*caller[2] + '> '
        debug_text = ' (%s, line %s)' % (caller[0], caller[1])

    # format ERROR and CRITICAL messages i.e. "my message (file.py, line 1003)
    elif messageType == MessageType.ERROR or messageType == MessageType.CRITICAL:
        caller = getStackTrace()
        debug_text = ' (%s, line %s)' % (caller[0], caller[1])

    # format text
    text = str(text) if type(text) != str else text
    text = '%s%s%s' % (indent, text, debug_text )

    # broadcast message
    udpsocket.sendto('|'.join([messageType,text]), addr)

# print initial message to each target port
targets = [attr for attr in dir(PrintTarget()) if not callable(attr) and not attr.startswith("__")]
for t in targets:
    print 'Broadcasting %s messages to port %d ' % (t, getattr(PrintTarget, t))
print 50*'- '


class DebugListener(object):
    def __init__(self, port=PrintTarget.CONSOLE):

        import threading
        self.buf = 1024
        self.port = port
        self.host = ''
        self.addr = (self.host, self.port)

        # start the message server
        self.thread = threading.Thread(target=self.messageServer, name='MessageServer')
        self.thread.daemon = True
        self.thread.start()

        print 'DebugListener listening on port %d' %port

    def messageServer(self):

        udpsocket = socket(AF_INET, SOCK_DGRAM)
        udpsocket.bind(self.addr)

        while True:

            # receive the message from the socket
            (data, addr) = udpsocket.recvfrom(self.buf)
            type, text = data.split('|')

            # print the message
            print text

    def __del__(self):
        del self