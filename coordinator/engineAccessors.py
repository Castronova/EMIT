__author__ = 'tonycastronova'

from engineManager import Engine
from threading import Thread

def Close():
    e = Engine()
    task = [(None, {})]
    e.setTasks(task)
    return 1

def addModel(id=None, attrib=None):
    e = Engine()
    kwargs = dict(attrib=attrib, id=id, event='onModelAdded')
    task = [('add_model', kwargs)]
    e.setTasks(task)
    # DO NOT MODIFY THIS CODE!
    ############################
    e.thread = Thread(target=e.check_for_process_results, name='AddModel')
    e.thread.start()
    ############################

def createSQLiteInMemory(dbtextfile=None):
    e = Engine()
    kwargs = dict(filepath=dbtextfile, event='onDatabaseConnected')
    task = [('create_sqlite_in_memory_database',kwargs)]
    e.setTasks(task)

    e.thread = Thread(target = e.check_for_process_results)
    e.thread.start()
    e.thread.join()

def connectToDbFromFile(dbtextfile=None):
    e = Engine()
    kwargs = dict(filepath=dbtextfile, event='onDatabaseConnected')
    task = [('connect_to_db_from_file',kwargs)]
    e.setTasks(task)

    e.thread = Thread(target = e.check_for_process_results, name='connectToDbFromFile')
    e.thread.start()
    e.thread.join()


def connectToDb(title, desc, engine, address, name, user, pwd):
    kwargs = dict(title=title, desc=desc, engine=engine, address=address, name=name, user=user, pwd=pwd)
    e = Engine()
    kwargs['event'] ='onDatabaseConnected'
    task = [('connect_to_db',kwargs)]
    e.setTasks(task)

    e.thread = Thread(target = e.check_for_process_results, name='connectToDb')
    e.thread.start()

    # result = e.processTasks()
    # return result

def addLink(source_id=None, source_item=None, target_id=None, target_item=None, spatial_interpolation=None,
            temporal_interpolation=None,uid=None):
    e = Engine()
    kwargs = dict(from_id=source_id, from_item_id=source_item, to_id=target_id, to_item_id=target_item,
                  spatial_interp=spatial_interpolation, temporal_interp=temporal_interpolation,uid=uid)
    task = [('add_link', kwargs)]
    e.setTasks(task)

    result = e.processTasks()
    return result

    # e.thread = Thread(target = e.check_for_process_results)
    # e.thread.start()

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

def setDefaultDb(database_id=None):
    e = Engine()
    kwargs = dict(db_id=database_id)
    task = [('set_default_database',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def removeModelById(modelid):
    e = Engine()
    kwargs = dict(id=modelid)
    task = [('remove_model_by_id',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def clearAll():
    """
    Clears all the models and links in the configuration
    :return: True on success
    """
    e = Engine()
    kwargs = dict()
    task = [('clear_all',kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getModelById(modelid):
    e = Engine()
    kwargs = dict(id=modelid)
    task = [('get_model_by_id_summary', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getOutputExchangeItems(modelid, returnGeoms=True):
    e = Engine()
    kwargs = dict(id=modelid, returnGeoms=returnGeoms)
    task = [('get_output_exchange_items_summary', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getInputExchangeItems(modelid, returnGeoms=True):
    e = Engine()
    kwargs = dict(id=modelid, returnGeoms=returnGeoms)
    task = [('get_input_exchange_items_summary', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getLinksBtwnModels(from_model_id, to_model_id):
    e = Engine()
    kwargs = dict(from_model_id=from_model_id, to_model_id=to_model_id)
    task = [('get_links_btwn_models', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getLinkById(linkid):
    e = Engine()
    kwargs = dict(id=linkid)
    task = [('get_link_by_id_summary', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def removeLinkById(linkid):
    e = Engine()
    kwargs = dict(id=linkid)
    task = [('remove_link_by_id', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getAllLinks():
    e = Engine()
    kwargs = dict()
    task = [('get_all_links', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def getAllModels():
    e = Engine()
    kwargs = dict()
    task = [('get_all_models', kwargs)]
    e.setTasks(task)
    result = e.processTasks()
    return result

def runSimulation(simulationName=None, dbName=None, user_json=None, datasets=None):
    e = Engine()
    kwargs = dict(simulationName=simulationName, dbName=dbName, user_json=user_json, datasets=datasets, event='onSimulationFinished')
    task = [('run_simulation', kwargs)]
    e.setTasks(task)

    e.thread = Thread(target=e.check_for_process_results)
    e.thread.start()
    e.thread.join()
    return '1'

