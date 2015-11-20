__author__ = 'jmeline'

from utilities.threading.baseThread import BaseThread

class ResultThread(BaseThread):
    def __init__(self, dispatcher):
        BaseThread.__init__(self)
        self.dispatcher = dispatcher

    def run(self):
        while self.signal:
            output = self.dispatcher.getResult()
            print self.name, "> result: ", output
            self.dispatcher.getResultQueue().task_done()

    def stop(self):
        self.onStop()

        if self.isAlive():
            self.join(.5)