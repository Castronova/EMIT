#!/usr/bin/env python2
import sys
from multiprocessing import freeze_support, cpu_count
from utilities.multiprocessing import TaskServerMP
from utilities.logger import LoggerTool


__author__ = 'Mario'

import os
import wx
from coordinator import main as cmd
from gui.mainGui import MainGui, wxStdOut
from gui.CanvasController import CanvasController

# sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../odm2/src')))

# ##########################################################################
# # Class MainFrame
# ##########################################################################
class MyApp(wx.App):
    def __init__(self, eng=None, redirect=False, filename=None, useBestVisual=False, clearSigInt=True, taskserver=None):
        """
        Initialize the application
        """
        self.taskserver = taskserver
        self.engine = eng

        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):

        # connect to databases and set default
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, './data/connections'))

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        # Build GUI components to be passed into the CanvasController
        self.frame = MainGui(None, self.engine)

        sys.stdout = SysOutListener()

        CanvasController(self.frame, self.taskserver)

        self.engine.connect_to_db([connections_txt])
        if not self.engine.get_default_db():
            self.engine.set_default_database()

        self.frame.Show(True)
        self.frame.Center()


        return True


class SysOutListener:
    def write(self, string):
        sys.__stdout__.write(string)
        evt = wxStdOut(text=string)
        wx.PostEvent(wx.GetApp().frame.output, evt)


if __name__ == '__main__':
    # https://docs.python.org/2/library/multiprocessing.html#miscellaneous

    # Add support for when a program which uses multiprocessing has been frozen to produce a Windows executable.
    # (Has been tested with py2exe, PyInstaller and cx_Freeze.)
    # One needs to call this function straight after the if __name__ == '__main__' line of the main module.

    # If the freeze_support() line is omitted then trying to run the frozen executable will raise RuntimeError.
    # If the module is being run normally by the Python interpreter then freeze_support() has no effect.
    freeze_support()

    # Determine the number of CPU's available
    # numproc = cpu_count()
    numproc = 1

    # create and instance of the coordinator engine
    engine = cmd.Coordinator()

    # Initialize TaskServer
    # This class starts the processes before starting wxpython and is a required step
    tsmp = TaskServerMP(numproc=numproc, engine=engine)

    app = MyApp(taskserver=tsmp, eng=engine)
    app.MainLoop()




