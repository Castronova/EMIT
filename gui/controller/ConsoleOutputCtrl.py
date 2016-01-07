__author__ = 'Tony'

import time
import coordinator.emitLogging as l
import wx
import json
import wx.lib.newevent
from socket import AF_INET, SOCK_DGRAM, socket
from gui.views.ConsoleView import ConsoleView
import threading

class consoleCtrl(ConsoleView):

    def __init__(self, parent):
        ConsoleView.__init__(self, parent=parent)

        # todo: get the port number from the environment variables so that the user can change as necessary
        self.buf = 1024
        self.port = 9271  # random port number
        self.host = ''
        self.addr = (self.host, self.port)

        # start the message server
        self.thread = threading.Thread(target=self.messageServer)
        self.thread.start()

    def Print(self, text, type):

        wx.CallAfter(self.log.SetInsertionPoint, 0)
        if type == 'INFO':
                wx.CallAfter(self.log.BeginTextColour, (42, 78, 110))
        elif type == 'WARNING':
            wx.CallAfter(self.log.BeginTextColour, (255, 140, 0))
        elif type =='ERROR':
            wx.CallAfter(self.log.BeginTextColour, (255, 0, 0))
        elif type == 'DEBUG':
            wx.CallAfter(self.log.BeginTextColour, (0, 0, 0))
        elif type == 'CRITICAL':
            wx.CallAfter(self.log.BeginTextColour, (170, 57, 57))
        wx.CallAfter(self.log.WriteText, text + '\n')
        wx.CallAfter(self.log.EndTextColour, )
        wx.CallAfter(self.log.Refresh, )

    def messageServer(self):

        udpsocket = socket(AF_INET, SOCK_DGRAM)
        udpsocket.bind(self.addr)

        while True:

            # receive the message from the socket
            (data, addr) = udpsocket.recvfrom(self.buf)
            type, text = data.split('|')

            # print the message
            self.Print(text, type)


# todo: remove this function (deprecated)
def follow(logging, target):
    path = None
    handlers = logging.get_logger().handlers
    for handler in handlers:
        if type(handler) == l.PickleHandler:
            path = handler.stream.name
            break

    # save the length of the previous message for overwriting via progress
    last_message_length = 0

    if path:

        thefile = open(path, 'r')
        last_processed = []
        last_lines = None
        while True:
            lines = tail(thefile, lines=5)

            # need to include this sleep timer to ensure that CPU does not go to 100%
            if lines == last_lines:
                time.sleep(.5)
            else:
                last_lines = lines
                line_list = lines.split('\n')
                line_list = filter(lambda a: a != '', line_list) # remove blank entries

                for line in line_list:
                    if line not in last_processed:

                        # load record from json
                        record = json.loads(line)

                        # todo: this is a hack
                        overwrite = False
                        if 'OVERWRITE:' in record['message']:
                            overwrite = True
                            message = record['message'].replace('OVERWRITE:','')
                        else:
                            message = record['message']

                        # target is the rich text box
                        wx.CallAfter(target.SetInsertionPoint, 0)
                        if record['levelname'] == 'WARNING':
                            wx.CallAfter(target.BeginTextColour, (255, 140, 0))
                        elif record['levelname'] =='ERROR':
                            wx.CallAfter(target.BeginTextColour, (255, 0, 0))
                        elif record['levelname'] == 'DEBUG':
                            wx.CallAfter(target.BeginTextColour, (0, 0, 0))
                        elif record['levelname'] == 'INFO':
                            wx.CallAfter(target.BeginTextColour, (42, 78, 110))
                        elif record['levelname'] == 'CRITICAL':
                            wx.CallAfter(target.BeginTextColour, (170, 57, 57))

                        if record['levelname'] != 'INFO':
                            message = ''.join([record['levelname'], ": ", message])


                        if not overwrite:
                            wx.CallAfter(target.WriteText, message+'\n')
                        else:
                            wx.CallAfter(target.Remove, 0, last_message_length)
                            wx.CallAfter(target.WriteText, message)

                        wx.CallAfter(target.EndTextColour, )
                        wx.CallAfter(target.Refresh, )

                    # store the last message length
                    last_message_length = len(message)

                last_processed = line_list

# todo: remove this function (deprecated)
def tail(f, lines=20):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from beginning
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])