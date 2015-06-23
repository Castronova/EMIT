__author__ = 'Mario'

import sys
import wx
import wx.xrc
import wx.aui
from gui.controller.logicEMIT import LogicEMIT
from coordinator import engineManager
import pickle
import time

from logging import FileHandler
import coordinator.emitLogging as l
logging = l.Log()

import threading

class EMITApp(wx.App):
    def OnInit(self):
        # Don't delete this line, instantiating the Borg Engine main thread here
        engine = engineManager.Engine()

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        self.logicEmit = LogicEMIT(None)

        # t = threading.Thread(target=self.follow,args=(logging, self.logicEmit.Output.log))
        # t.start()

        # logging.debug('THIS IS A TEST FROM EMIT.py!!!')

        return True



    # # TODO: threading is not working!!!
    # def follow(self, logging, target):
    #     path = None
    #     handlers = logging.get_logger().handlers
    #     for handler in handlers:
    #         if type(handler) == l.FileHandler:
    #             path = handler.stream.name
    #             break
    #
    #     if path:
    #
    #         thefile = open(path, 'r')
    #         last_processed = None
    #         while True:
    #             line = self.tail(thefile, lines=1)
    #             if line == '' or line == last_processed:
    #                 time.sleep(0.2)
    #             else:
    #                 last_processed = line
    #                 record = pickle.loads(line.replace('~~','\n').replace('!~!~','\r'))
    #                 target.WriteText(record.message+'\n')
    #                 target.Refresh()
    #
    # def tail(self, f, lines=20 ):
    #     total_lines_wanted = lines
    #
    #     BLOCK_SIZE = 1024
    #     f.seek(0, 2)
    #     block_end_byte = f.tell()
    #     lines_to_go = total_lines_wanted
    #     block_number = -1
    #     blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
    #                 # from the end of the file
    #     while lines_to_go > 0 and block_end_byte > 0:
    #         if (block_end_byte - BLOCK_SIZE > 0):
    #             # read the last block we haven't yet read
    #             f.seek(block_number*BLOCK_SIZE, 2)
    #             blocks.append(f.read(BLOCK_SIZE))
    #         else:
    #             # file too small, start from begining
    #             f.seek(0,0)
    #             # only read what was not read
    #             blocks.append(f.read(block_end_byte))
    #         lines_found = blocks[-1].count('\n')
    #         lines_to_go -= lines_found
    #         block_end_byte -= BLOCK_SIZE
    #         block_number -= 1
    #     all_read_text = ''.join(reversed(blocks))
    #     return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])


if __name__ == '__main__':
    app = EMITApp()
    app.MainLoop()
