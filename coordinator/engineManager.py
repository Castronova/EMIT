from coordinator.engine import Coordinator
from multiprocessing import Process
import sys
from multiprocessing import Queue
import events
import wx

class EngineBorg:
    """
    Borg pattern to ensure that all instances of the engine have shared state
    """

    __monostate = None

    def __init__(self):
        if not EngineBorg.__monostate:
            EngineBorg.__monostate = self.__dict__
            self.engine = Coordinator()

        else:
            self.__dict__ = EngineBorg.__monostate

def get_engine():
    """
    gets the shared engine
    :return: engine coordinator object
    """
    e = EngineBorg()
    return e.engine

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

    def putResult(self, result):
        """
        Put a result on the result queue.
        """
        self.resultQueue.put(result)

    def getResult(self):
        """
        Get a result from the result queue.
        """
        return self.resultQueue.get()

class Engine:
    """
    The TaskServer class provides a target worker class method for queued processes.
    """

    __monostate = None

    def __init__(self):
        if not Engine.__monostate:

            Engine.__monostate = self.__dict__

            self.numprocesses = 1
            self.tasks = []

            # Create the dispatcher
            self.dispatcher = Dispatcher()

            self.Processes = []

            # get the engine instance
            self.engine = get_engine()

            for n in range(self.numprocesses):

                ######################################################################
                # the following lines are necessary to solve a multiprocessing crash
                # see: http://stackoverflow.com/a/29893338/886133
                ######################################################################
                if not hasattr(sys.stdin, 'close'):
                    def dummy_close():
                        pass
                    sys.stdin.close = dummy_close
                ######################################################################

                process = Process(target=Engine.worker, args=(self.dispatcher,self.engine))
                process.start()
                self.Processes.append(process)

        else:
            self.__dict__ = Engine.__monostate


    def setTasks(self, taskList):
        """
        Sets the tasks for the TaskServerMP to handle.
        """
        self.tasks.extend(taskList)

    def worker(cls, dispatcher, engine):
        """
        The worker creates a TaskProcessor object to calculate the result.
        """

        while True:
            next_task_name, next_task_args = dispatcher.getTask()

            if next_task_name:
                task = getattr(engine, next_task_name)
                evt = None
                if 'event' in next_task_args:
                    evt = next_task_args.pop('event')

                try:
                    result = task(**next_task_args)
                except Exception, e:
                    # elog.error(e.message)
                    print e.message
                    result = None

                if evt is not None:
                    if result is not None:
                        result['event'] = evt
                dispatcher.putResult(result)
            else:
                break

    # The multiprocessing worker must not require any existing object for execution!
    worker = classmethod(worker)

    def processTasks(self, resfunc=None):
        """
        Start the execution of tasks by the processes.
        """

        # put task in
        for task in self.tasks:

            # remove the task from the global object so that duplicates aren't added to the task queue
            t = self.tasks.pop()

            self.dispatcher.putTask(t)


        # get output
        return self.dispatcher.getResult()

    def check_for_process_results(self):

        result = self.processTasks()
        if result is not None:
            if 'event' in result.keys():
                evt_name= result.pop('event')
                evt = getattr(events, evt_name)

                try:
                    wx.CallAfter(evt.fire, **result)
                except:
                    pass

                # evt.fire(**result)

    def close(self):
        # kill all running processes
        for p in self.Processes:
            p.terminate()