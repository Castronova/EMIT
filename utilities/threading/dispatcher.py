from Queue import Queue

__author__ = 'jmeline'

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Dispatcher:
    """
    The Dispatcher class manages the task and result queues.
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        Initialise the Dispatcher.
        """
        self.taskQueue = Queue()
        self.resultQueue = Queue()
        self.outputQueue = Queue()

    def getTaskQueue(self):

        return self.taskQueue

    def getResultQueue(self):

        return self.resultQueue

    def getOutputQueue(self):

        return self.outputQueue

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

    def putOutput(self, out):
        """
        Put output into a queue
        """
        self.outputQueue.put(out)

    def getOutput(self):
        """
        Get an output from the output queue
        """
        return self.outputQueue.get()
