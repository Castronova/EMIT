__author__ = 'tonycastronova'

from coordinator.engine import Coordinator
import types
from multiprocessing import Process
import sys
import time
from threading import Thread
import os
from multiprocessing import Queue
import events

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
        self.numtasks = len(taskList)

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

                result = task(**next_task_args)

                if evt is not None:
                    if result is not None:
                        result['event'] = evt
                dispatcher.putResult(result)

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

        #print "In ProcessTasks: ", pickle.loads(model)

    def processStop(self, resfunc=None):
        """
        Stop the execution of tasks by the processes.
        """
        self.keepgoing = False

        while (self.j < self.i):
            # Get and print any results remining in the done queue
            output = self.getOutput()
            if (isinstance(resfunc, (types.FunctionType, types.MethodType))):
                resfunc(output)

    def processTerminate(self):
        """
        Stop the execution of tasks by the processes.
        """
        for n in range(self.numprocesses):
            # Terminate any running processes
            self.Processes[n].terminate()

        # Wait for all processes to stop
        while (self.anyAlive()):
            time.sleep(0.5)

    def anyAlive(self):
        """
        Check if any processes are alive.
        """
        isalive = False
        for n in range(self.numprocesses):
            isalive = (isalive or self.Processes[n].is_alive())
        return isalive

    def getOutput(self):
        """
        Get the output from one completed task.
        """
        self.j += 1

        if (self.numprocesses == 0):
            # Use the single-process method
            self.worker_sp()

        output = self.dispatcher.getResult()
        # Calculate the time remaining
        self.timeRemaining(self.j + 1, self.numtasks, output['process']['pid'])

        return output

    def timeRemaining(self, tasknum, numtasks, pid):
        """
        Calculate the time remaining for the processes to complete N tasks.
        """
        timeNow = time.time()
        self.timeElapsed = timeNow - self.timeStart

        pid_str = '%d' % pid
        self.processTime[pid_str] = self.timeElapsed

        # Calculate the average time elapsed for all of the processes
        timeElapsedAvg = 0.0
        numprocesses = self.numprocesses
        if (numprocesses == 0): numprocesses = 1
        for pid_str in self.processTime.keys():
            timeElapsedAvg += self.processTime[pid_str] / numprocesses
        self.timeRemain = timeElapsedAvg * (float(numtasks) / float(tasknum) - 1.0)

    def update(self, output):
        """
        Get and print the results from one completed task.
        """
        # sys.stdout.write('%s [%d] calculate(%d) = %.2f' % ( output['process']['name'], output['process']['pid'], output['result'][0], output['result'][1] ))
        sys.stdout.write('  [Complete: %2d / %2d  Time Elapsed: %s  Remaining: %s]' % (
        self.j + 1, self.numtasks, time.strftime('%M:%S', time.gmtime(self.timeElapsed)),
        time.strftime('%M:%S', time.gmtime(self.timeRemain))))
        sys.stdout.write('\n')

    def check_for_process_results(self):

        result = self.processTasks()
        if result is not None:
            if 'event' in result.keys():
                evt_name= result.pop('event')
                evt = getattr(events, evt_name)
                evt.fire(**result)
