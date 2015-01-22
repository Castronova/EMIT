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


def run_feed_forward(obj):
    # store db sessions
    db_sessions = {}


    # todo: determine unresolved exchange items (utilities)


    sim_st = time.time()

    activethreads = []

    # determine execution order
    sys.stdout.write('> Determining execution order... ')
    exec_order = obj.determine_execution_order()
    sys.stdout.write('done\n')
    for i in range(0, len(exec_order)):
        print '> %d.) %s'%(i+1,obj.get_model_by_id(exec_order[i]).get_name())


    # store model db sessions
    for modelid in exec_order:
        session = obj.get_model_by_id(modelid).get_instance().session()
        if session is None:
            session = obj.get_default_db()['session']

        # todo: this should be stored in the model instance
        # model_obj = obj.get_model_by_id(modelid)
        # model_inst = model_obj.get_instance()
        # model_inst.session


        # todo: need to consider other databases too!
        db_sessions[modelid] = postgresdb(session)


    # loop through models and execute run
    for modelid in exec_order:

        # get the database session
        #simulation_dbapi = postgresdb(obj.get_default_db()['session'])
        simulation_dbapi = db_sessions[modelid]

        st = time.time()

        # get the current model instance
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.get_instance()

        # set the default session if it hasn't been specified otherwise
        #if model_inst.session() is None:
        #    model_inst.session(obj.get_default_db()['session'])

        print '> '
        print '> ------------------'+len(model_inst.name())*'-'
        print '> Executing module: %s ' % model_inst.name()
        print '> ------------------'+len(model_inst.name())*'-'

        #  retrieve inputs from database
        sys.stdout.write('> [1 of 4] Retrieving input data... ')
        sys.__stdout__.flush()

        # todo: pass db_sessions instead of simulation_dbapi
        try:
            input_data =  get_ts_from_database_link(simulation_dbapi,db_sessions, obj.DbResults(), obj.Links(), model_inst)
        except Exception as e:
            raise Exception (e)


        sys.stdout.write('done\n')
        sys.__stdout__.flush()

        sys.stdout.write('> [2 of 4] Performing calculation... ')
        sys.__stdout__.flush()
        # pass these inputs ts to the models' run function
        model_inst.run(input_data)
        sys.stdout.write('done\n')
        sys.__stdout__.flush()

        # save these results
        sys.stdout.write('> [3 of 4] Saving calculations to database... ')
        sys.__stdout__.flush()
        exchangeitems = model_inst.save()

        # only insert data if its not already in a database
        if type(model_inst) != odm2_data.odm2:
            pass
            # todo: not saving result b/c it is to slow over wireless!
            # #  set these input data as exchange items in stdlib or wrapper class
            # simulation = simulation_dbapi.create_simulation(preferences_path=obj.preferences,
            #                                config_params=model_obj.get_config_params(),
            #                                output_exchange_items=exchangeitems,
            #                                )
            #
            #
            # # store the database action associated with this simulation
            # obj.DbResults(key=model_inst.name(), value = (simulation.ActionID,model_inst.session(),'action'))

        else:
            obj.DbResults(key=model_inst.name(), value = (model_inst.resultid(), model_inst.session(), 'result'))

        sys.stdout.write('done\n')
        sys.__stdout__.flush()

        # update links
        sys.stdout.write('> [4 of 4] Updating links... ')
        sys.__stdout__.flush()
        obj.update_links(model_inst,exchangeitems)
        sys.stdout.write('done\n')
        sys.__stdout__.flush()

        sys.stdout.write('> module simulation completed in %3.2f seconds' % (time.time() - st))
        sys.__stdout__.flush()


    print '> '
    print '> ------------------------------------------'
    print '>           Simulation Summary '
    print '> ------------------------------------------'
    print '> Completed without error :)'
    print '> Simulation duration: %3.2f seconds' % (time.time()-sim_st)
    print '> ------------------------------------------'


def run_time_step(obj):

    # store db sessions
    db_sessions = {}

    sim_st = time.time()

    # determine execution order
    sys.stdout.write('> [PRE-RUN] Determining execution order... ')
    exec_order = obj.determine_execution_order()
    sys.stdout.write('done\n')
    for i in range(0, len(exec_order)):
        print '>           %d.) %s'%(i+1,obj.get_model_by_id(exec_order[i]).get_name())

    links = {}
    spatial_maps = {}
    simulation_status = {}
    sys.stdout.write('> [PRE-RUN] Performing spatial mapping... ')
    for modelid in exec_order:
        # get links
        l = obj.get_from_links_by_model(modelid)
        links[modelid] = l

        for linkid, link in l.iteritems():
            # build spatial maps
            source = link.source_exchange_item()
            target = link.target_exchange_item()

            #source = link[0][1]
            #target = link[1][1]
            #spatial = spatial_closest_object()


            key = generate_link_key(link)
            #spatial_maps[key] = spatial.transform(source.get_all_datasets().keys(), target.get_all_datasets().keys())

            spatial_interp = link.spatial_interpolation()
            spatial_maps[key] = spatial_interp.transform(source.get_all_datasets().keys(),
                                                         target.get_all_datasets().keys())

        # set model status to RUNNING
        obj.get_model_by_id(modelid).get_instance().status(Status.Running)

        # initialize the simulation_status dictionary
        simulation_status[modelid] = obj.get_model_by_id(modelid).get_instance().status()

        # store model db sessions
        session = obj.get_model_by_id(modelid).get_instance().session()
        if session is None:
            session = obj.get_default_db()['session']

        # todo: need to consider other databases too!
        db_sessions[modelid] = postgresdb(session)
    sys.stdout.write('done\n')


    # todo: move this into a time-horizon checking function.
    #       this should check that the time-horizon is valid.
    # determine minimum overlapping timespan to set start and end times
    sys.stdout.write('> [PRE-RUN] Validating simulation time-horizon... ')
    global_simulation_start = datetime.datetime(3000,1,1)
    global_simulation_end = datetime.datetime(1800,1,1)
    for modelid in exec_order:
        inst = obj.get_model_by_id(modelid).get_instance()
        global_simulation_start = inst.simulation_start() if inst.simulation_start() < global_simulation_start else global_simulation_start
        global_simulation_end = inst.simulation_end() if inst.simulation_end() > global_simulation_end else global_simulation_end

    if global_simulation_start >= global_simulation_end:
        raise Exception("Invalid start and end times!\nstart:%s\nend:%s" % (str(global_simulation_start), str(global_simulation_end)))
    sys.stdout.write('done\n')


    # run simulation until all models reach a FINISHED state
    while not all(stat == Status.Finished for stat in simulation_status.values()):

        print ''

        # loop through models and execute run
        for modelid in exec_order:

            # get the current model instance
            model_obj = obj.get_model_by_id(modelid)
            model_inst = model_obj.get_instance()

            # get the target simulation times from the model links (including its own endtime)
            target_times = []

            if len(links[modelid]) > 0:
                # add the target current time
                for linkid, link in links[modelid].iteritems():

                    #target_model  = target[0]
                    target_model = link.target_component()
                    target_times.append(target_model.get_instance().current_time())


            else:
                # add the current time for the source model (this will force the model to step only once)
                target_times.append(model_inst.current_time())

            #target_times.append(model_inst.simulation_end())



            # time the model until it reaches or surpasses all target times (requested time)
            current_time = model_inst.current_time()
            while current_time <= max(target_times):

                print '> %s | ' % (datetime.datetime.strftime(current_time,"%m-%d-%Y %H:%M:%S")),

                # update simulation status
                simulation_status[modelid] = model_inst.status()
                if model_inst.status() != Status.Running:
                    # exit without calling run_timestep
                    break


                # get model input data
                input_data = model_inst.inputs()

                # run model timestep
                model_inst.run_timestep(input_data, current_time)

                # get the new current time
                current_time = model_inst.current_time()



            # get all outputs
            output_exchange_items = model_inst.outputs()



            #for source, target, linkid in links[modelid]:
            for linkid, link in links[modelid].iteritems():



                #target_model  = target[0]
                target_model = link.target_component()

                # get the auto generated key for this link
                #link_key = generate_link_key(obj.get_link_by_id(linkid).get_link())
                link_key = generate_link_key(link)

                # get the target interpolation time based on the current time of the target model
                target_time = target_model.get_instance().current_time()

                # get all the datasets of the output exchange item.  These will be used to temporally map the data
                datasets = output_exchange_items[model_inst.name()].get_all_datasets()

                # Temporal data mapping
                mapped = {}
                for geom, datavalues in datasets.iteritems():

                    # get the dates and values from the geometry
                    dates,values = datavalues.get_dates_values()

                    # temporal mapping
                    temporal = temporal_nearest_neighbor()
                    mapped_dates,mapped_values = temporal.transform(dates,values,target_time)

                    if mapped_dates is not None:
                        # save the temporally mapped data by output geometry
                        mapped[geom] = (zip(mapped_dates,mapped_values))


                # update links
                #if len(mapped.values()) > 0:
                obj.update_link(linkid, mapped, spatial_maps[link_key])
                #else:
                #    obj.update_link(linkid, None, None)
                        # reset geometry values to None



    print '> '
    print '> ------------------------------------------'
    print '>           Simulation Summary '
    print '> ------------------------------------------'
    print '> Completed without error :)'
    print '> Simulation duration: %3.2f seconds' % (time.time()-sim_st)
    print '> ------------------------------------------'