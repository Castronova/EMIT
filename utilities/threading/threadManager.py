from utilities.threading.communicatorThread import CommunicatorThread
from utilities.threading.dispatcher import Dispatcher
from utilities.threading.workerThread import WorkerThread

__author__ = 'jmeline'

class ThreadManager:
    """
    Handles the thread operations
    """
    def __init__(self, controller):
        self.dispatcher = Dispatcher()
        self.controller = controller
        self.start(1)

    def start(self, size):
        """
        Start all threads
        :param: Number of threads to build
        """
        for i in range(size):
            ct = CommunicatorThread(self.dispatcher)
            wt = WorkerThread(self.controller, self.dispatcher)
            ct.start()
            wt.start()

    def stop(self):
        """
        Stop all threads
        """
        pass
        #print "Stopping worker"
        #self.workerThread.stop()
        #print "Stopping communicator"
        #self.communicatorThread.stop()

    def get_dispatcher(self):
        """
        Get Dispatcher object
        """
        return self.dispatcher

