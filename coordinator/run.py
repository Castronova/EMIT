from utilities.threading.threadManager import ThreadManager

__author__ = 'tonycastronova'

import time
from db.dbapi import postgresdb
import sys
from utilities.gui import *
from utilities.mdl import *
from wrappers import odm2_data
from transform.time import *
from transform.space import *
from utilities.status import Status
import update
from coordinator.emitLogging import elog
from odm2api.ODMconnection import dbconnection
import database

import db.dbapi_v2 as dbv2

class dataSaveInfo():
    def __init__(self, simulationName, database_args, user, datasets):
        self.simulationName = simulationName
        self.database_args = database_args
        self.user = user
        self.datasets = datasets

        # self, engine, address, db=None, user=None, password=None, dbtype = 2.0):
        self.session = dbconnection.createConnection(engine=database_args['engine'],
                                                     address=database_args['address'],
                                                     db=database_args['db'],
                                                     user=database_args['user'],
                                                     password=database_args['pwd'])



def run_feed_forward(obj, ds=None):
    # store db sessions
    db_sessions = {}

    # set engine status
    obj.status.set(stdlib.Status.NOTREADY)

    # todo: determine unresolved exchange items (utilities)

    sim_st = time.time()

    activethreads = []

    # determine execution order
    elog.info('Determining execution order... ')
    sPrint('Determining execution order... ', MessageType.INFO)

    exec_order = obj.determine_execution_order()
    for i in range(0, len(exec_order)):
        elog.info('%d.) %s' % (i + 1, obj.get_model_by_id(exec_order[i]).name()))

    links = {}
    spatial_maps = {}

    # todo:  move this into function
    elog.info('Generating spatial maps... ')
    sPrint('Generating spatial maps... ')

    for modelid in exec_order:

        # get links
        l = obj.get_from_links_by_model(modelid)
        links[modelid] = l

        # build spatial maps
        for linkid, link in l.iteritems():
            source = link.source_exchange_item()
            target = link.target_exchange_item()
            key = generate_link_key(link)

            # set default spatial interpolation to ExactMatch
            if link.spatial_interpolation() is None:
                sPrint('Spatial interpolation not provided, using the default mapping approach:  \'Spatial Index\'', MessageType.WARNING)
                link.spatial_interpolation(spatial_index())

            spatial_interp = link.spatial_interpolation()
            source_geoms = source.getGeometries2()
            target_geoms = target.getGeometries2()


            if len(source_geoms) == 0:
                sPrint('Cannot continue simulation, %s -- %s contains 0 geometries' % link.source_component().name(), source.name() )
            if len(target_geoms) == 0:
                sPrint('Cannot continue simulation, %s -- %s contains 0 geometries' % link.target_component().name(), target.name())

            # todo: remove these two lines b/c they use deprecated function calls!
            #if len(source_geoms) == 0: source_geoms = source.get_all_datasets().keys()
            #if len(target_geoms) == 0: target_geoms = target.get_all_datasets().keys()

            # save the spatial mapping based on link key
            spatial_maps[key] = spatial_interp.transform(source_geoms, target_geoms)

    # todo:  move this into function
    # prepare all models
    for modelid in exec_order:
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.instance()
        model_inst.prepare()

        if model_inst.status() != stdlib.Status.READY:
            msg = 'Cannot continue with simulation because model "%s" has a status of "%s" after the preparation' \
                          ' phase.  Status must be "%s" in order to proceed with simulation ' \
                          % (model_inst.name(), model_inst.status(), stdlib.Status.READY)

            elog.critical(msg)
            sPrint(msg, MessageType.ERROR)
            return False

    # update engine status
    obj.status.set(stdlib.Status.READY)

    # loop through models and execute run
    for modelid in exec_order:

        # update engine status
        obj.status.set(stdlib.Status.RUNNING)

        st = time.time()

        # get the current model instance
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.instance()
        sPrint('Executing module: %s \n' % model_inst.name(), MessageType.INFO)

        #  retrieve inputs from database
        sPrint("[1 of 3] Retrieving input data... ")
        input_data = model_inst.inputs()

        # pass these inputs ts to the models' run function
        sPrint("[2 of 3] Performing calculation... ")
        model_inst.run(input_data)

        # update links
        sPrint("[3 of 3] Updating links... ")
        oei = model_inst.outputs()
        update.update_links_feed_forward(obj, links[modelid], oei, spatial_maps)

        model_inst.finish()
        elog.info('..module simulation completed in %3.2f seconds' % (time.time() - st))

    sPrint('------------------------------------------\n' +
              '         Simulation Summary \n' +
              '------------------------------------------\n' +
              'Completed without error :)\n' +
              'Simulation duration: %3.2f seconds\n' % (time.time() - sim_st) +
              '------------------------------------------')


    # update engine status
    obj.status.set(stdlib.Status.FINISHED)

    # save simulation results
    model_ids = exec_order
    if ds is None:
        msg = 'Simulation results will not be stored in database because database connection was not provided prior to simulation.'
        elog.info(msg)
        sPrint(msg, messageType=MessageType.INFO)
    else:
        database.save(obj, ds, model_ids)

    # # save results if ds is provided
    # # todo: move this outside run.py
    # if ds is not None:
    #     elog.info('Saving Simulation Results...')
    #     st = time.time()
    #
    #     try:
    #         # build an instance of dbv22
    #         db = dbv2.connect(ds.session)
    #     except Exception, e:
    #         elog.error('An error was encountered when connecting to the database to save the simulation results: %s' % e)
    #         sPrint('An error was encountered when connecting to the database to save the simulation results.', MessageType.ERROR)
    #         return 0
    #
    #     # insert data!
    #     for modelid in exec_order:
    #
    #         # get the current model instance
    #         model_obj = obj.get_model_by_id(modelid)
    #         model_inst = model_obj.instance()
    #         model_name = model_inst.name()
    #
    #         # get the output exchange items to save for this model
    #         oeis =  ds.datasets[model_name]
    #         items = []
    #         for oei in oeis:
    #             items.append(model_inst.outputs()[oei])
    #
    #         sPrint('..found %d items to save for model %d' % (len(items), model_name), MessageType.INFO)
    #
    #         if len(items) > 0:
    #             # get config parameters
    #             config_params=model_obj.get_config_params()
    #
    #
    #             db.create_simulation(coupledSimulationName=ds.simulationName,
    #                                  user_obj=ds.user,
    #                                  config_params=config_params,
    #                                  ei=items,
    #                                  simulation_start = model_inst.simulation_start(),
    #                                  simulation_end = model_inst.simulation_end(),
    #                                  timestep_value = model_inst.time_step(),
    #                                  timestep_unit = 'seconds',
    #                                  description = model_inst.description(),
    #                                  name = model_inst.name()
    #                                  )
    #
    #     sPrint('Saving Complete, elapsed time = %3.5f' % (time.time() - st), MessageType.INFO)

def run_time_step(obj, ds=None):
    # store db sessions
    db_sessions = {}

    # ThreadManager
    dispatcher = ThreadManager().get_dispatcher()

    sim_st = time.time()

    # todo:  move this into function
    # determine execution order
    msg = '> Determining execution order... '
    dispatcher.putOutput(msg)
    exec_order = obj.determine_execution_order()

    msg = 'done'
    dispatcher.putOutput(msg)
    for i in range(0, len(exec_order)):
        msg = '> %d.) %s' % (i + 1, obj.get_model_by_id(exec_order[i]).name())
        dispatcher.putOutput(msg)

    links = {}
    spatial_maps = {}
    simulation_status = {}

    # todo:  move this into function
    msg = '> [PRE-RUN] Performing spatial mapping... '
    dispatcher.putOutput(msg)
    for modelid in exec_order:
        # get links
        l = obj.get_from_links_by_model(modelid)
        links[modelid] = l

        for linkid, link in l.iteritems():
            # build spatial maps
            source = link.source_exchange_item()
            target = link.target_exchange_item()

            # source = link[0][1]
            #target = link[1][1]
            #spatial = spatial_closest_object()


            key = generate_link_key(link)
            #spatial_maps[key] = spatial.transform(source.get_all_datasets().keys(), target.get_all_datasets().keys())

            spatial_interp = link.spatial_interpolation()
            if spatial_interp:
                spatial_maps[key] = spatial_interp.transform(source.get_all_datasets().keys(),
                                                             target.get_all_datasets().keys())

        # set model status to RUNNING
        obj.get_model_by_id(modelid).instance().status(Status.Running)

        # initialize the simulation_status dictionary
        simulation_status[modelid] = obj.get_model_by_id(modelid).instance().status()

        # store model db sessions
        session = obj.get_model_by_id(modelid).instance().session()
        if session is None:
            try:  # this is necessary if no db connection exists
                session = obj.get_default_db()['session']
            except:
                pass

        # todo: need to consider other databases too!
        db_sessions[modelid] = postgresdb(session)

    msg = 'done'
    dispatcher.putOutput(msg)

    # todo: move this into a time-horizon checking function.
    # this should check that the time-horizon is valid.
    # determine minimum overlapping timespan to set start and end times
    msg = '> [PRE-RUN] Validating simulation time-horizon... '
    dispatcher.putOutput(msg)
    global_simulation_start = datetime.datetime(3000, 1, 1)
    global_simulation_end = datetime.datetime(1800, 1, 1)
    for modelid in exec_order:
        inst = obj.get_model_by_id(modelid).instance()
        global_simulation_start = inst.simulation_start() if inst.simulation_start() < global_simulation_start else global_simulation_start
        global_simulation_end = inst.simulation_end() if inst.simulation_end() > global_simulation_end else global_simulation_end

    if global_simulation_start >= global_simulation_end:
        raise Exception("Invalid start and end times!\nstart:%s\nend:%s" % (
        str(global_simulation_start), str(global_simulation_end)))

    msg = 'done'
    dispatcher.putOutput(msg)

    # todo:  move this into function
    # prepare all models
    for modelid in exec_order:
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.instance()
        if model_inst.status() != Status.Ready:
            model_inst.prepare()

    iter_count = 1
    # run simulation until all models reach a FINISHED state
    while not all(stat == Status.Finished for stat in simulation_status.values()):

        # TODO:  This needs to be modified to operate under loop control!  For instance if the simulation reaches a point where the current model doesnt reach or exceed the target model, the loop should be broken and restart from the beginning.  This will also allow multithreading of multiple loops during a composition that might be helpful for calibrations.

        msg = 'Executing Loop %d' % iter_count
        dispatcher.putOutput(msg)
        # print '\nExecuting Loop %d' % iter_count

        # loop through models and execute run
        for modelid in exec_order:

            # get the current model instance
            model_obj = obj.get_model_by_id(modelid)
            model_inst = model_obj.instance()

            # get the target simulation times from the model links (including its own endtime)
            target_times = []

            if len(links[modelid]) > 0:
                # add the target current time
                for linkid, link in links[modelid].iteritems():
                    #target_model  = target[0]
                    target_model = link.target_component()
                    target_times.append(target_model.instance().current_time())


            else:
                # add the current time for the source model (this will force the model to step only once)
                target_times.append(model_inst.current_time())




            # time the model until it reaches or surpasses all target times (requested time)
            current_time = model_inst.current_time()
            while current_time <= max(target_times):


                # update simulation status

                simulation_status[modelid] = model_inst.status()
                if model_inst.status() != Status.Running and \
                                model_inst.status() != Status.Ready:
                    # exit without calling run_timestep
                    msg = '> %s  ' % (datetime.datetime.strftime(current_time, "%m-%d-%Y %H:%M:%S"))
                    dispatcher.putOutput(msg)

                    msg = '> %s | %s \n' % (model_inst.name(), model_inst.status())
                    dispatcher.putOutput(msg)


                    break


                # get model input data
                input_data = model_inst.inputs()

                msg = '> %s  ' % (datetime.datetime.strftime(current_time, "%m-%d-%Y %H:%M:%S"))
                dispatcher.putOutput(msg)

                msg = '> %s | %s \n' % (model_inst.name(), model_inst.status())
                dispatcher.putOutput(msg)

                # run model timestep
                model_inst.run_timestep(input_data, current_time)

                # get the new current time
                current_time = model_inst.current_time()

                sys.stdout.write('\n')

            # get all outputs
            output_exchange_items = model_inst.outputs()



            # update the outgoing links for this component
            update.update_links(obj, links[modelid], output_exchange_items, spatial_maps)


            # ### TODO: Currently moving the update functionality into update.py
            #
            # #for source, target, linkid in links[modelid]:
            # for linkid, link in links[modelid].iteritems():
            #
            #
            #
            #     #target_model  = target[0]
            #     target_model = link.target_component()
            #
            #     source_item_name = link.source_exchange_item().name()
            #
            #     # get the auto generated key for this link
            #     #link_key = generate_link_key(obj.get_link_by_id(linkid).get_link())
            #     link_key = generate_link_key(link)
            #
            #     # get the target interpolation time based on the current time of the target model
            #     target_time = target_model.get_instance().current_time()
            #
            #     # get all the datasets of the output exchange item.  These will be used to temporally map the data
            #     #datasets = output_exchange_items[model_inst.name()].get_all_datasets()
            #     datasets = output_exchange_items[source_item_name].get_all_datasets()
            #
            #     # Temporal data mapping
            #     mapped = {}
            #     for geom, datavalues in datasets.iteritems():
            #
            #         # get the dates and values from the geometry
            #         dates,values = datavalues.get_dates_values()
            #
            #         # temporal mapping
            #         temporal = temporal_nearest_neighbor()
            #         if temporal and values:
            #             mapped_dates,mapped_values = temporal.transform(dates,values,target_time)
            #
            #             if mapped_dates is not None:
            #                 # save the temporally mapped data by output geometry
            #                 mapped[geom] = (zip(mapped_dates,mapped_values))
            #
            #
            #     # update links
            #     #if len(mapped.values()) > 0:
            #     if len(mapped.keys()) > 0:
            #         obj.update_link(linkid, mapped, spatial_maps[link_key])
            #     #else:
            #     #    obj.update_link(linkid, None, None)
            #             # reset geometry values to None

        iter_count += 1

    for modelid in exec_order:

        # get the current model instance
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.instance()

        # save results
        items = model_inst.save()

        # todo: save outputs to database!
        if len(items) > 0:
            simulation_dbapi = db_sessions[modelid]
            #  set these input data as exchange items in stdlib or wrapper class
            simulation = simulation_dbapi.create_simulation(preferences_path=obj.preferences,
                                                            config_params=model_obj.get_config_params(),
                                                            output_exchange_items=items,
            )

            # store the database action associated with this simulation
            #obj.DbResults(key=model_inst.name(), value = (simulation.ActionID,model_inst.session(),'action'))





            # if db_sessions[modelid] is not None:
            #       # save results

    msg = '> \n' + \
        '> ------------------------------------------\n' + \
        '>           Simulation Summary \n'               + \
        '> ------------------------------------------\n' + \
        '> Completed without error :)\n' + \
        '> Simulation duration: %3.2f seconds\n' % (time.time()-sim_st) + \
        '> ------------------------------------------'
    dispatcher.putOutput(msg)
