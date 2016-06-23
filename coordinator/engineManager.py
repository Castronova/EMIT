from coordinator.engine import Coordinator, Serializable
from multiprocessing import Process
import sys
from multiprocessing import Queue
import events
import wx
from sprint import *

class EngineBorg:
    """
    Borg pattern to ensure that all instances of the engine have shared state
    """

    __monostate = None

    def __init__(self):
        if not EngineBorg.__monostate:
            EngineBorg.__monostate = self.__dict__
            # self.engine = Coordinator()
            self.engine = Serializable()

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

                # get the success and failure event handlers
                evt_success = None
                evt_fail = None

                if 'event_success' in next_task_args:
                    evt_success = next_task_args.pop('event_success')

                if 'event_fail' in next_task_args:
                    evt_fail = next_task_args.pop('event_fail')

                try:

                    # run the task
                    result = task(**next_task_args)

                    # if the function fails, set the result to None
                    # This expects all functions to return a dictionary with a 'success' key in it
                    if not isinstance(result, dict):
                        sPrint('%s should return a dictionary as a result, otherwise expect errors in engineManager' % str(next_task_name), MessageType.ERROR)
                        result = {}
                    else:
                        task_successful = result.pop('success')


                except Exception, e:

                    msg = e.message
                    sPrint(msg, MessageType.ERROR)

                    # if the function raises an exception, set the result to None
                    result = {}

                # set the success and fail events
                if isinstance(result, dict):
                    if evt_success is not None and task_successful:
                        result['event'] = evt_success
                    elif evt_fail is not None and not task_successful:
                        result['event'] = evt_fail

                    # send the result to the check_for_process_results only if a dictionary is returned
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
        if 'event' in result.keys():
            # This assumes that result has an "event" key and a "result" key
            evt_name = result.pop('event')
            evt = getattr(events, evt_name)
            res = result.pop('result')

            try:
                wx.CallAfter(evt.fire, **res)
            except Exception as e:
                print e


    def close(self):
        # kill all running processes
        for p in self.Processes:
            p.terminate()