__author__ = 'tonycastronova'


from socket import AF_INET, SOCK_DGRAM, socket

# print targets
class PrintTarget:
    CONSOLE = 9271

# message types
class MessageType:
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    INFO = 'INFO'
    CRITICAL = 'CRITICAL'


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

    text = str(text) if type(text) != str else text
    udpsocket.sendto('|'.join([messageType,text]), addr)