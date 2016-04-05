from coordinator.emitLogging import elog
from sprint import *
import time
from odm2api.ODMconnection import dbconnection
import db.dbapi_v2 as dbv2

def save(obj, datasave, modelids):

    if datasave.session is not None:
        session = datasave.session
    else:
        msg = 'Could not connect to database for results saving: %s' % datasave.database_args['address']
        elog.error(msg)
        sPrint(msg, MessageType.ERROR)
        return 0

    db = dbv2.connect(sessionFactory=session)

    sPrint('Saving Simulation Results...')
    st = time.time()

    # insert data!
    for modelid in modelids:

        # get the current model instance
        model_obj = obj.get_model_by_id(modelid)
        model_inst = model_obj.instance()
        model_name = model_inst.name()

        # get the output exchange items to save for this model
        oeis =  datasave.datasets[model_name]
        items = []
        for oei in oeis:
            items.append(model_inst.outputs()[oei])

        sPrint('..found %d items to save for model %s' % (len(items), model_name), MessageType.INFO)

        if len(items) > 0:
            # get config parameters
            config_params=model_obj.get_config_params()


            id = db.create_simulation(coupledSimulationName=datasave.simulationName,
                             user_obj=datasave.user,
                             config_params=config_params,
                             ei=items,
                             simulation_start = model_inst.simulation_start(),
                             simulation_end = model_inst.simulation_end(),
                             timestep_value = model_inst.time_step(),
                             timestep_unit = 'seconds',
                             description = model_inst.description(),
                             name = model_inst.name()
                             )
            if id is None:
                sPrint('Failed to save results for: %s ' % (model_name), MessageType.ERROR)

    sPrint('Saving Complete, elapsed time = %3.5f seconds' % (time.time() - st), MessageType.INFO)