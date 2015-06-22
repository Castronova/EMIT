__author__ = 'Mario'

import sys
import wx
import wx.xrc
import wx.aui
from gui.controller.logicEMIT import LogicEMIT
from coordinator import engineManager
import coordinator.emitLogging as logging



class EMITApp(wx.App):
    def OnInit(self):
        # Don't delete this line, instantiating the Borg Engine main thread here
        engine = engineManager.Engine()

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        logging.log.debug('THIS IS A TEST FROM EMIT.py!!!')

        self.logicEmit = LogicEMIT(None)

        return True

# class SysOutListener:
#     def write(self, string):
#         try:
#             sys.__stdout__.write(string)
#             evt = wxStdOut(text=string)
#             wx.PostEvent(wx.GetApp().frame.output, evt)
#         except:
#             pass

    def follow(self, logging, target):
            path = logging.get_logger().handlers[-1].stream.name
            thefile = open(logging.get_logger().handlers[-1].stream.name,'r')
            num_files = len(logging.get_logger().handlers)

            # get the last position in the file
            # f.seek(last_pos)
            # line = f.readline()  # no 's' at the end of `readline()`
            # last_pos = f.tell()
            # f.close()

            thefile.seek(0,2)
            while True:
                line = thefile.readline()
                if not line:
                    if len(logging.get_logger().handlers) != num_files:
                        thefile.close()
                        thefile = open(logging.get_logger().handlers[-1].stream.name,'r')

                    time.sleep(0.5)
                    continue
                # yield line

                target.WriteText(line)
                target.Refresh()

            return True



# class SysOutListener:
#     def write(self, string):
#         try:
#             sys.__stdout__.write(string)
#             evt = wxStdOut(text=string)
#             wx.PostEvent(wx.GetApp().frame.output, evt)
#         except:
#             pass


if __name__ == '__main__':
    app = EMITApp()
    app.MainLoop()




