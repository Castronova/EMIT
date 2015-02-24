__author__ = 'tonycastronova'


from utilities.multiprocessing import TaskServerMP



class task_server (object):
    def __init__(self):
        self.taskserver = TaskServerMP()


def add_model(taskserver, type=None, id=None, attrib=None, model_class=None):

    kwargs = dict(type, attrib)
    task = [('AddModels', kwargs)]
    taskserver.setTasks(task)
