from utilities.threading import wxCreateBox

__author__ = 'jmeline'

# import wx
from baseThread import BaseThread


class WorkerThread(BaseThread):
    def __init__(self, controller, dispatcher):
        BaseThread.__init__(self)
        self.dispatcher = dispatcher
        self.controller = controller
        # self.cmd = controller.cmd

    # TODO look into threadpools concurrent.futures
    def run(self):
        while self.signal:
            task_type, task = self.dispatcher.getTask()
            # self.dispatcher.putOutput("Got a task (%s, %s)" % (task_type, task))
            if task_type == "addmodel":
                self.addModel(**task)
            # self.dispatcher.putOutput("Done with task (%s, %s)" % (task_type, task))

            self.dispatcher.getTaskQueue().task_done()


    # def addModel(self, **task):
    #
    #     x = task.pop('x')
    #     y = task.pop('y')
    #
    #     model = self.cmd.add_model(**task)
    #     name = model.get_name()
    #     model_id = model.get_id()
    #
    #     # post event
    #     evt = wxCreateBox()
    #     evt.name = name
    #     evt.id = model_id
    #     evt.xCoord = x
    #     evt.yCoord = y
    #     wx.PostEvent(wx.GetApp().logicEmit, evt)

    def stop(self):
        if self.isAlive():
            self.join(.5)