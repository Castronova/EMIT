__author__ = 'tonycastronova'

import time
from db.dbapi import postgresdb
import sys
from utilities.gui import *
from utilities.mdl import *
from wrappers import odm2_data

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

        # todo: pass db_sessions instead of simulation_dbapi
        input_data =  get_ts_from_link(simulation_dbapi,db_sessions, obj.DbResults(), obj.Links(), model_inst)
        sys.stdout.write('done\n')

        sys.stdout.write('> [2 of 4] Performing calculation... ')
        # pass these inputs ts to the models' run function
        model_inst.run(input_data)
        sys.stdout.write('done\n')

        # save these results
        sys.stdout.write('> [3 of 4] Saving calculations to database... ')
        exchangeitems = model_inst.save()

        # only insert data if its not already in a database
        if type(model_inst) != odm2_data.odm2:

            #  set these input data as exchange items in stdlib or wrapper class
            simulation = simulation_dbapi.create_simulation(preferences_path=obj.preferences,
                                           config_params=model_obj.get_config_params(),
                                           output_exchange_items=exchangeitems,
                                           )


            # store the database action associated with this simulation
            obj.DbResults(key=model_inst.name(), value = (simulation.ActionID,model_inst.session(),'action'))
            #obj._dbresults[model_inst.name()] = (simulation.ActionID,model_inst.session(),'action')

        else:
            #obj._dbresults[model_inst.name()] = (model_inst.resultid(), model_inst.session(), 'result')
            obj.DbResults(key=model_inst.name(), value = (model_inst.resultid(), model_inst.session(), 'result'))
        sys.stdout.write('done\n')

        # update links
        sys.stdout.write('> [4 of 4] Updating links... ')
        obj.update_links(model_inst,exchangeitems)
        sys.stdout.write('done\n')

        print '> module simulation completed in %3.2f seconds' % (time.time() - st)


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

        # todo: need to consider other databases too!
        db_sessions[modelid] = postgresdb(session)

    # loop through models and execute run
    for modelid in exec_order:

        st = time.time()

        # get the current model instance
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.get_instance()

        current_time = datetime.datetime.strftime(model_inst.current_time(),'%m-%d-%Y %H:%M:%S')
        print '> %s : %s' % (model_inst.name(), current_time)

        # todo: data is not being returned here!
        # get inputs from link
        input_data =  get_data_from_link(obj.Links(), model_inst)

        output = model_inst.run_timestep(input_data, current_time)


        # pass these inputs ts to the models' run function
        #model_inst.run(input_data)
        # sys.stdout.write('done\n')

        # get all outputs
        output_exchange_items = model_inst.outputs()

        if type(output_exchange_items) != type([]):
            output_exchange_items = [model_inst.outputs()]
        if type(model_inst) == odm2_data.odm2:

            # get the value for the current time
            #utput_exchange_items

            # todo: interpolate data at to the target timestep
            # todo: use source_time and target_time
            #data = output_exchange_items.get_all_datasets().values()[0].timeseries()
            pass

        # update output data in links
        obj.update_links(model_inst,output_exchange_items)

        # save these results
        # sys.stdout.write('> [3 of 4] Saving calculations to database... ')
        #exchangeitems = model_inst.save()


        # # only insert data if its not already in a database
        # if type(model_inst) != odm2_data.odm2:
        #
        #     #  set these input data as exchange items in stdlib or wrapper class
        #     simulation = simulation_dbapi.create_simulation(preferences_path=obj.preferences,
        #                                    config_params=model_obj.get_config_params(),
        #                                    output_exchange_items=exchangeitems,
        #                                    )
        #
        #     sys.stdout.write('done\n')
        #
        #     # store the database action associated with this simulation
        #     obj.DbResults(key=model_inst.name(), value = (simulation.ActionID,model_inst.session(),'action'))
        #
        # else:
        #     obj.DbResults(key=model_inst.name(), value = (model_inst.resultid(), model_inst.session(), 'result'))
        #
        # # update links
        # sys.stdout.write('> [4 of 4] Updating links... ')
        #
        # sys.stdout.write('done\n')
        #
        # print '> module simulation completed in %3.2f seconds' % (time.time() - st)


    print '> '
    print '> ------------------------------------------'
    print '>           Simulation Summary '
    print '> ------------------------------------------'
    print '> Completed without error :)'
    print '> Simulation duration: %3.2f seconds' % (time.time()-sim_st)
    print '> ------------------------------------------'