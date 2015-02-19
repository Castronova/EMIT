from Queue import Queue
import threading

__author__ = 'tonycastronova'

import wx
from threading import Thread
from functools import wraps

from wx.lib.newevent import NewEvent
wxCreateBox, EVT_CREATE_BOX = NewEvent()

def runAsync(func):
    '''Decorates a method to run in a separate thread'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    return wrapper


def wxCallafter(target):
    '''Decorates a method to be called as a wxCallafter'''
    @wraps(target)
    def wrapper(*args, **kwargs):
        wx.CallAfter(target, *args, **kwargs)
    return wrapper


def threaded(f, daemon=False):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = Queue.Queue()

        t = Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap


class WorkerThread(threading.Thread):
    def __init__(self, controller, dispatcher):
        threading.Thread.__init__(self)
        self.dispatcher = dispatcher
        self.controller = controller
        self.cmd = controller.cmd
        self.keepRunning = True

    def StartThread(self):
        print "Starting Thread"
        self.start()
        print "Joining Thread"
        self.join()
        print "Done joining Thread"

    # TODO look into threadpools concurrent.futures
    def run(self):
        while self.keepRunning:
            print "Waiting for task"
            task_type, task = self.dispatcher.getTask()
            result = None
            if task_type == "addmodel":
                result = self.addModel(**task)
            if task_type == 'kill':
                self.keepRunning = False
            self.dispatcher.getTaskQueue().task_done()
            self.dispatcher.putResult(result)
            #self.join()
            print "Done with task"


    def addModel(self, **task):

        x = task.pop('x')
        y = task.pop('y')

        model = self.cmd.add_model(**task)
        name = model.get_name()
        modelId = model.get_id()

        # post event
        evt = wxCreateBox()
        evt.name = name
        evt.id = modelId
        evt.xCoord = x
        evt.yCoord = y
        #wx.PostEvent(wx.GetApp().frame, evt)

        #return model

class Dispatcher:
    """
    The Dispatcher class manages the task and result queues.
    """

    def __init__(self):
        """
        Initialise the Dispatcher.
        """
        self.taskQueue = Queue()
        self.resultQueue = Queue()

    def getTaskQueue(self):
        return self.taskQueue

    def getResultQueue(self):
        return self.resultQueue

    def putTask(self, task):
        """
        Put a task on the task queue.
        """
        self.taskQueue.put(task)

    def getTask(self):
        """
        Get a task from the task queue.
        """
        return self.taskQueue.get()

    def putResult(self, output):
        """
        Put a result on the result queue.
        """
        self.resultQueue.put(output)

    def getResult(self):
        """
        Get a result from the result queue.
        """
        return self.resultQueue.get()

# def worker():
#     print "Worker started!"
#     model = self.cmd.add_model(dtype,attrib={'mdl':filenames[0]})
#     name = model.get_name()
#     modelid = model.get_id()
#     self.controller.createBox(name=name, id=modelid, xCoord=x, yCoord=y)
#     print "worker Finished"
#
# t = threading.Thread(target=worker, args=(,))
# t.start()
