from multiprocessing import Queue

__author__ = 'jmeline'

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