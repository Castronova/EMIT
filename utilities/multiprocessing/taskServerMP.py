import logging
import types
from multiprocessing import Process
import sys
import time
from utilities.multiprocessing.dispatcher import Dispatcher
from utilities.logger import LoggerTool
from wx.lib.newevent import NewEvent
from threading import Thread
import os
import copy

# Credit for solution came from Roger Stuckey's example


try:
   import cPickle as pickle
except:
   import pickle

from coordinator import main as cmd

__author__ = 'jmeline'

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)



class TaskServerMP:
    """
    The TaskServerMP class provides a target worker class method for queued processes.
    """

    def __init__(self, numproc=1):
        """
        Initialise the TaskServerMP and create the dispatcher and processes.
        """
        self.numprocesses = numproc
        self.tasks = []

        # Create the dispatcher
        self.dispatcher = Dispatcher()

        self.Processes = []

        # begin processes before entering app.MainLoop()
        # attempting to start them before will crash wxPython. Don't do it
        for n in range(numproc):
            process = Process(target=TaskServerMP.worker, args=(self.dispatcher,))
            process.start()
            self.Processes.append(process)

        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        self.connect_to_databases_from_file(connections_txt)

    def setEngine(self, engine):
        self.engine = engine

    def setTasks(self, taskList):
        """
        Sets the tasks for the TaskServerMP to handle.
        """
        self.tasks.extend(taskList)
        self.numtasks = len(taskList)


    def worker(cls, dispatcher):
        """
        The worker creates a TaskProcessor object to calculate the result.
        """

        while True:
            args = dispatcher.getTask()
            engine = cmd.Coordinator()
            # print "Engine in worker: ", engine
            task_type = args[0]
            task_args = args[1]
            # print "WORKER! ", str(task_args)

            if task_type == 'AddModel':
                eng_type = task_args['type']
                eng_attrib = task_args['attrib']
                eng_id = task_args['id']

                result = engine.add_model(type=eng_type, attrib=eng_attrib,id=eng_id)
                # print "Finished Model in worker: ", result, engine.get_models()
                result['type']='AddModel'
                dispatcher.putResult(result)

            # elif task_type == 'AddDataModel':
            #
            #     result = engine.add_data_model(database_id=task_args['database_id'],
            #                                    name=task_args['name'])
            #     result['type'] = 'AddDataModel'
            #     dispatcher.putResult(result)

            elif task_type == 'AddLink':
                # eng_type = task_args['type']
                # eng_attrib = task_args['attrib']


                link = engine.add_link_by_name(from_id=task_args['source_id'],
                                                 from_item_name=task_args['source_item'],
                                                 to_id=task_args['target_id'],
                                                 to_item_name=task_args['target_item'])
                link.temporal_interpolation(task_args['temporal'])
                link.spatial_interpolation(task_args['spatial'])
                result = {'type':'AddLink',
                          'source_id':task_args['source_id'],
                          'target_id':task_args['target_id']}

                dispatcher.putResult(result)

            elif task_type == 'ConnectToDatabasesFromFile':

                engine.connect_to_db([task_args['filepath']])
                if not engine.get_default_db():
                    engine.set_default_database()
                dispatcher.putResult({'type':'ConnectToDatabasesFromFile'})

            elif task_type == "GetDatabaseConnections":
                connections = engine.get_db_connections()
                result = {}
                for k, v in connections.iteritems():
                    result[k] = {'args':v['args'],'connection_string':v['connection_string'],'description':v['description'], 'name':v['name']}
                    # v.pop('session')
                result['type'] =  'GetDatabaseConnections'

                dispatcher.putResult(result)

    # The multiprocessing worker must not require any existing object for execution!
    worker = classmethod(worker)


    def processTasks(self, resfunc=None):
        """
        Start the execution of tasks by the processes.
        """
        logger.debug("Entering Process Tasks")
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


    def check_for_process_results(self, parent):

        result = self.processTasks()

        if result['type'] == 'AddModel':
            id = result['id']
            name = result['name']
            type = result['model_type']
            parent.draw_box(name=name,id=id,type=type)

        elif result['type'] == 'AddDataModel':
            id = result['id']
            name = result['name']
            parent.draw_box(name=name,id=id)

        elif result['type'] == 'AddLink':
            source_id = result['source_id']
            target_id = result['target_id']
            parent.draw_link(source_id=source_id,target_id=target_id)
            print 'here'

        elif result['type'] == 'GetDatabaseConnections':
            result.pop('type')
            parent.setDatabases(result)

        else:
            pass


    def add_model(self, parent, type=None, id=None, attrib=None, model_class=None):
        #kwargs = dict(type=dtype, attrib={'mdl': filenames[0]})
        kwargs = dict(type=type, attrib=attrib, id=id,model_class=model_class)
        task = [('AddModel', kwargs)]
        self.setTasks(task)

        self.thread = Thread(target = self.check_for_process_results,args=(parent,))
        self.thread.start()
        # self.thread.join()

    # def add_data_model(self, parent, type, database_id=None, resultid=None):
    #
    #     att = {'databaseid':database_id,'resultid':resultid}
    #     kwargs = dict(type=type, attrib=att)
    #     task = [('AddModel', kwargs)]
    #     self.setTasks(task)
    #
    #     self.thread = Thread(target = self.check_for_process_results,args=(parent,))
    #     self.thread.start()


    def add_link(self, parent, source_id=None, source_item=None, target_id=None, target_item=None,spatial=None, temporal=None ):

        kwargs = dict(source_id=source_id, source_item=source_item, target_id=target_id, target_item=target_item,spatial=spatial, temporal=temporal)
        task = [('AddLink',kwargs)]
        self.setTasks(task)

        self.thread = Thread(target = self.check_for_process_results,args=(parent,))
        self.thread.start()

    def get_models(self):
        kwargs = dict()
        task = [('GetModels',kwargs)]
        self.setTasks(task)

    def get_db_connections(self,parent):
        kwargs = dict()
        task = [('GetDatabaseConnections',kwargs)]
        self.setTasks(task)
        #result = self.processTasks()

        self.thread = Thread(target = self.check_for_process_results,args=(parent,))
        self.thread.start()

    def connect_to_databases_from_file(self, filepath):

        kwargs = dict(filepath=filepath)
        task = [('ConnectToDatabasesFromFile',kwargs)]
        self.setTasks(task)

        self.thread = Thread(target = self.check_for_process_results,args=(None, ))
        self.thread.start()

    def get_db_conn(self, parent):
        kwargs = dict()
        task = [('GetDatabaseConnections',kwargs)]
        self.setTasks(task)
        result = self.processTasks()
        return result
