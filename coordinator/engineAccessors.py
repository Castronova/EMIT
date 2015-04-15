__author__ = 'tonycastronova'

from engineManager import Engine
from threading import Thread


def addModel(id=None, attrib=None):
    e = Engine()
    kwargs = dict(attrib=attrib, id=id, event='onModelAdded')
    task = [('add_model', kwargs)]
    e.setTasks(task)

    e.thread = Thread(target=e.check_for_process_results)
    e.thread.start()


def addLink(source_id=None, source_item=None, target_id=None, target_item=None,spatial=None, temporal=None ):
    e = Engine()
    kwargs = dict(source_id=source_id, source_item=source_item, target_id=target_id, target_item=target_item,spatial=spatial, temporal=temporal, event='onLinkAdded')
    task = [('add_link',kwargs)]
    e.setTasks(task)

    e.thread = Thread(target = e.check_for_process_results)
    e.thread.start()

def getDbConnections():
    e = Engine()
    kwargs = dict()
    task = [('get_db_connections',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getDefaultDb():
    e = Engine()
    kwargs = dict()
    task = [('get_default_db',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result


def GetLinkById():
    e = Engine()
    kwargs = dict()
    task = [('get_link_by_id',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def RemoveModelById(modelid):
    e = Engine()
    kwargs = dict(id=modelid)
    task = [('remove_model_by_id',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result


# getLinkById (id)
# get_links_btwn_models


# def connectToDbFromFile(filepath):
#     e = Engine()
#     kwargs = dict(filepath=filepath)
#     task = [('connect_to_db_from_file',kwargs)]
#     e.setTasks(task)
#
#     e.thread = Thread(target = e.check_for_process_results)
#     e.thread.start()