import threading

import networkx as net
import sqlalchemy
import stdlib
import run
from api_old.ODM2.Core.services import *
from emitLogging import elog
from sprint import *
from transform import space_base
from transform import time_base
import utilities.gui as gui
from utilities.mdl import *
from wrappers import feed_forward
from wrappers import odm2_data
from wrappers import time_step
import wrappers
from utilities.models import *
from . import terminal

"""
Purpose: This file contains the logic used to run coupled model simulations
"""


class EngineStatus(object):
    """
    Defines the current status of the Engine.  Status is defined using the
    stdlib.Status class
    """

    def __init__(self):
        self.__engineStatus = stdlib.Status.UNDEFINED

    def set(self, status=stdlib.Status.UNDEFINED):
        if status in dir(stdlib.Status):
            self.__engineStatus = status
        else:
            sPrint('Failed to set engine status.  '
                   'Status must by instance of stdlib.Status')

    def get(self):
        return self.__engineStatus

    def __str__(self):
        return 'The Engine status is currently set to: %s' % \
               self.__engineStatus


class Link(object):
    def __init__(self, id, from_linkable_component, to_linkable_component,
                 from_item, to_item):
        """
        defines the link object.  Links are used to pass data between models
        during simulation runtime. This class captures the information that is
        necessary to define a unique linkage between model components.

        Args:
            id: unique id for the link object (type:string)
            from_linkable_component: the component object that is providing
                                     output (type:Engine.Model)
            to_linkable_component: the component object that is accepting input
                                   (type:Engine.Model)
            from_item: The exchange item that is passed as output
                       (type: stdlib.ExchangeItem)
            to_item: the exchange item that is accepted as input
                     (type: stdlib.ExchangeItem)

        Returns: Link

        """
        self.__from_lc = from_linkable_component
        self.__from_item = from_item

        self.__to_lc = to_linkable_component
        self.__to_item = to_item

        self.__id = id

        self.__spatial_interpolation = None
        self.__temporal_interpolation = None

    def get_link(self):
        """
        Gets the Engine.Model and Stdlib.ExchangeItem objects that comprise
        the link object
        Returns: tuple( [from model, from exchange item],
                        [to model, to exchange item] )

        """

        return [self.__from_lc, self.__from_item], \
               [self.__to_lc, self.__to_item]

    def source_exchange_item(self):
        """
        Gets the source exchange item on the link
        Returns: stdlib.ExchangeItem

        """
        return self.__from_item

    def target_exchange_item(self):
        """
        Gets the target exchange item on the link
        Returns: stdlib.ExchangeItem

        """

        return self.__to_item

    def source_component(self):
        """
        Gets the source model component item on the link
        Returns: engine.Model

        """
        return self.__from_lc

    def target_component(self):
        """
        Gets the target model on the link
        Returns: engine.Model

        """
        return self.__to_lc

    def get_id(self):
        """
        Gets the link id
        Returns: str(id)

        """
        return self.__id

    def spatial_interpolation(self, value=None):
        """
        Gets/Sets the spatial interpolation method used during data transfer
        Args:
            value: spatial transformation object (transform.Space)

        Returns: spatial transformation object (transform.Space)

        """
        if value is not None:
            if isinstance(value, space_base.Space):
                self.__spatial_interpolation = value
        return self.__spatial_interpolation

    def temporal_interpolation(self, value=None):
        """
        Gets/Sets the temporal interpolation method used durin data transfer
        Args:
            value: temporal transformation object (transform.Time)

        Returns: temporal transformation object (transform.Time)

        """
        if value is not None:
            if isinstance(value, time_base.Time):
                self.__temporal_interpolation = value
        return self.__temporal_interpolation


class Model(object):
    def __init__(self, id, name, instance, desc=None, input_exchange_items=[],
                 output_exchange_items=[], params=None):
        """
        Defines a linkable model that can be loaded into a configuration
        Args:
            id: unique id for the model (type: string)
            name: name of the model (type: string)
            instance: instantiated model object
            desc: description of the model (type: string)
            input_exchange_items: list of input exchange items
                                  (type: list[stdlib.ExchangeItem] )
            output_exchange_items: list of output exchange items
                                   (type: list[stdlib.ExchangeItem] )
            params: model loading parameters (e.g. *.mdl params)
                    (type: list[ dict{  )

        Returns: Model

        """
        self.__description = desc
        self.__iei = {}
        self.__oei = {}
        self.__id = id
        self.__params = params
        self.__attrib = {}

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance
        self.__params_path = None

    def type(self):
        """
        Gets the type of model
        Returns: wrappers.Types

        """
        return self.instance().type()

    def attrib(self, value=None):
        """
        Provides a method for storing model specific attributes
        Args:
            value: #todo

        Returns: #todo
        """
        if value is not None:
            self.__attrib = value
        return self.__attrib

    def get_input_exchange_items(self):
        """
        Gets model input exchange items
        Returns: list of exchange item objects
                 (type: list[stdlib.ExchangeItem])

        """
        if len(self.__iei.keys()) > 0:
            return [j for i, j in self.__iei.items()]
        else:
            return []

    def get_output_exchange_items(self):
        """
        Gets model output exchange items
        Returns: list of exchange item objects
                 (type: list[stdlib.ExchangeItem])

        """
        if len(self.__oei.keys()) > 0:
            return [j for i, j in self.__oei.items()]
        else:
            return []

    def get_input_exchange_item_by_name(self, value):
        """
        Gets an input exchange item by name
        Args:
            value: name associated with exchange item

        Returns: exchange item of None (type: stdlib.ExchangeItem or None)

        """

        i = self.instance()
        if value in i.inputs():
            return i.inputs()[value]
        else:
            elog.error('Could not find Input Exchange Item: '+value)
            return None

    def get_output_exchange_item_by_name(self, value):
        """
        Gets an output exchange item by name
        Args:
            value: name associated with exchange item

        Returns: exchange item of None (type: stdlib.ExchangeItem or None)

        """

        i = self.instance()
        if value in i.outputs():
            return i.outputs()[value]
        else:
            elog.error('Could not find Output Exchange Item: ' + value)
            return None

    def description(self):
        """
        Gets the description of the model
        Returns: description (type: string)

        """
        return self.__description

    def name(self):
        """
        Gets the name of the model
        Returns: name (type:string)

        """
        return self.instance().name()

    def id(self):
        """
        Gets the id of the model
        Returns: id (type:string)

        """
        return self.__id

    def instance(self):
        """
        Gets the instance of the model
        Returns: instance

        """
        return self.__inst

    def get_config_params(self):
        """
        Gets the configuration parameters of the model
        Returns: parameters

        """
        return self.__params

    def params_path(self, value=None):
        """
        Get/Set the path to the model parameter file
        Args:
            value: path to the parameter file

        Returns: path to the parameter file (type:string)

        """
        if value is not None:
            self.__params_path = value
        return self.__params_path


class Coordinator(object):
    def __init__(self):
        """
        The simulation coordinator.

        Returns: Coordinator

        """
        self.__models = {}
        self.__links = {}
        self._db = {}
        self.__default_db = None
        self.status = EngineStatus()

    def remove_all_models_and_links(self):
        """
        Clears all the model and link objects from the controller

        Returns: True
        """
    
        self.__links = {}
        self.__models = {}
        return True

    def remove_link_by_id(self, linkid):
        """
        Removes a link using the link id
        Args:
            linkid: id of the link to remove

        Returns: 1 if successful, otherwise 0

        """
        if id in self.__links:
            self.__links.pop(linkid, None)
            return 1
        return 0

    def get_status(self):
        """
        Returns: the current status of the Engine.
        """
        return self.status.get()

    def Models(self, model=None):
        """
        Gets/Sets coordinator models

        Args:
            model: model object (type:engine.Model)

        Returns: list of models (type:list[engine.Model])

        """
        if model is not None:
            self.__models[model.name()] = model
        return self.__models

    def add_db_connection(self, value):
        """
        Adds a database connection to the Coordinator

        Args:
            value: database connection

        Returns: dictionary of database connections

        """
        self._db.update(value)
        return self._db

    def get_db_connections(self):
        """
        Gets all database connections that have been loaded in the Coordinator

        Returns: dictionary of database connections (type:dict)

        """

        return self._db

    def get_db_args_by_name(self, db_name):
        """
        Gets database arguments for a specific database name

        Args:
            db_name: name of the database to retrieve arguments for

        Returns: dictionary of database arguments or None
                 (type:dict or type:None)

        """
        # return the database args dictionary for a given name
        for db_id in self._db.iterkeys():
            database = self._db[db_id]
            if database['name'] == db_name:
                return database['args']
        return None

    def set_default_database(self, db_id=None):
        """
        Sets the default database for results saving

        Args:
            db_id: id of the database to assign as the default

        Returns: None

        """

        if db_id is not None:
            try:
                self.__default_db = self._db[db_id]
                self.__default_db['id'] = db_id
                sPrint('Default database : %s' %
                       self._db[db_id]['connection_string'], MessageType.INFO)
            except Exception, e:
                msg = 'Encountered and error when setting default ' \
                      'database: %s' % e
                elog.error(msg)
                sPrint(msg, MessageType.ERROR)
        else:
            sPrint('Could not set the default database', MessageType.ERROR)

    def get_default_db(self):
        """
        Gets the database that has been assigned as the default

        Returns: the default database

        """
        if self.__default_db is None:
            return None
        else:
            return self.__default_db

    def add_model(self, **params):
        """
        Adds a model to the engine
        Args:
            **params:  id: modelid
                       config_params

        Returns:  on success returns dict(id:?, name:?, model_type:?). on
                  failure returns 0
        """
        if 'model_type' in params:
            model_type = params['model_type']
        else:
            sPrint('Cannot add model, missing model_type parameter',
                   MessageType.ERROR)

        sPrint('Loading Model', MessageType.DEBUG)
        try:
            if params['id'] is None:
                model_id = 'M' + uuid.uuid4().hex
            else:
                model_id = params['id']

            if model_type.lower() == 'mdl':
                # load model
                name, inst = gui.load_model(params)


                # make sure this model doesnt already exist
                if name in self.__models:
                    msg = 'Model named %s already exists in configuration' %\
                          name
                    elog.warning(msg)
                    sPrint(msg, MessageType.WARNING)
                    return None
            else:
                try:
                    # check to make sure a wrapper for this datatype exists
                    getattr(wrappers, model_type)
                except:
                    msg = 'Could not locate wrapper of type %s.  Make sure ' \
                          'the wrapper is specified in wrappers.__init__.' % model_type
                    elog.error(msg)
                    sPrint(msg, MessageType.ERROR)

                # instantiate the component wrapper
                inst = getattr(wrappers, model_type).Wrapper(params)

            # get the input and output exchange items from the instance
            oei = inst.outputs().values()
            iei = inst.inputs().values()

            # create a model instance
            this_model = Model(id=model_id,
                               name=inst.name(),
                               instance=inst,
                               desc=inst.description(),
                               input_exchange_items= iei,
                               output_exchange_items=  oei,
                               params=params)

        except Exception, e:
            sPrint('Encountered an error while loading model: %s' %
                   e, MessageType.ERROR)
            elog.error('Encountered an error while loading model: %s' % e)
            this_model = None

        if this_model is not None:
            # save the model
            sPrint('Finished Loading', MessageType.DEBUG)
            self.__models[this_model.name()] = this_model
            return this_model
        else:
            elog.error('Failed to load model.')
            sPrint('Failed to load model.', MessageType.ERROR)
            return None

    def remove_model(self, model_id):
        """
        Removes a model from the Coordinator by id

        Args:
            model_id: id of the model to remove (type:string)

        Returns: the id of the model that was removed or None
                 (type:string or None)

        """
        for m in self.__models:
            if self.__models[m].id() == model_id:

                # remove the model
                self.__models.pop(m, None)

                # find all links associated with the model
                remove_these_links = []
                for l in self.__links:
                    from_model, to_model = self.__links[l].get_link()
                    if from_model[0].id() == model_id or \
                       to_model[0].id() == model_id:
                        remove_these_links.append(l)

                # remove all links associated with the model
                for link in remove_these_links:
                    self.__links.pop(link, None)

                return model_id
        return None

    def get_model(self, model_id):
        """
        Gets a model within the Coordinator by id

        Args:
            model_id: id of the model to return (type:string)

        Returns: model or None (type:engine.Model or None)

        """
        for m in self.__models:
            if self.__models[m].id() == model_id:
                return self.__models[m]
        return None

    def get_model_object(self, model_id):
        return self.get_model(model_id=model_id)

    def add_link(self, from_id, from_item_id, to_id, to_item_id,
                 spatial_interp=None, temporal_interp=None, uid=None):
        """
        Creates a new link in the Coordinator 

        Args:
            from_id: id of the source model (type:string)
            from_item_id: id of the source exchange item (type:string)
            to_id: id of the target model (type:string)
            to_item_id: id of the target exchange item (type:string)
            spatial_interp: spatial_interpolation
            temporal_interp: temporal_interpolation
            uid: unique id for the link

        Returns: id of the link that was created or 0 

        """

        # check that from and to models exist in composition
        from_model = self.get_model(from_id)
        to_model = self.get_model(to_id)

        try:

            if from_model is None:
                raise Exception('> '+from_id +
                                ' does not exist in configuration')
            if to_model is None:
                raise Exception('> ' + to_id +
                                ' does not exist in configuration')

        except Exception, e:
            elog.error(e)
            return None

        # check that input and output exchange items exist
        ii = to_model.get_input_exchange_item_by_name(to_item_id)
        oi = from_model.get_output_exchange_item_by_name(from_item_id)

        if ii is not None and oi is not None:
            # generate a unique id
            if uid is None:
                lid = 'L'+uuid.uuid4().hex
            else:
                lid = uid

            # create link
            link = Link(lid, from_model, to_model, oi, ii)

            # add spatial and temporal interpolations
            if spatial_interp is not None:
                link.spatial_interpolation(spatial_interp)
            if temporal_interp is not None:
                link.temporal_interpolation(temporal_interp)

            # save the link
            self.__links[lid] = link

            return link

        else:

            msg = 'Failed to create link'
            elog.error(msg)
            sPrint(msg, MessageType.ERROR)
            return None

    def add_link_by_name(self, from_id, from_item_name, to_id, to_item_name):
        """
        Creates a new link in the Coordinator

        Args:
            from_id: id of the source model (type:string)
            from_item_name: name of the source exchange item (type:string)
            to_id: id of the target model (type:string)
            to_item_name: name of the target exchange item (type:string)

        Returns: the link object that is created or None
                 (type:engine.Link or None)

        """

        # check that from and to models exist in composition
        from_model = self.get_model(from_id)
        to_model = self.get_model(to_id)
        try:

            if self.get_model(from_id) is None:
                raise Exception(from_id+' does not exist in configuration')
            if self.get_model(to_id) is None:
                raise Exception(to_id+' does not exist in configuration')
        except Exception, e:
            elog.error(e)
            return None

        # check that input and output exchange items exist
        ii = to_model.get_input_exchange_item_by_name(to_item_name)
        oi = from_model.get_output_exchange_item_by_name(from_item_name)

        if ii is not None and oi is not None:
            # generate a unique model id
            linkid = 'L'+uuid.uuid4().hex[:5]

            # create link
            link = Link(linkid, from_model, to_model, oi, ii)
            self.__links[linkid] = link

            return link
        else:
            elog.warning('Could Not Create Link :(')
            return None

    def get_from_links_by_model(self, model_id):
        """
        Gets links corresponding to a specific model id in which the model is
        the source component. This is useful for determining where data will
        pass (direction)

        Args:
            model_id: id of the model to retrieve links for (type:string)

        Returns: dictionary of link objects (type: dict{engine.Link})

        """

        links = {}
        for linkid, link in self.__links.iteritems():
            # get the from/to link info

            if link.source_component().id() == model_id:
                links[linkid] = link

        return links

    def get_all_links(self):
        """
        Gets all links that have been created/loaded in the Coordinator

        Returns: all links (type:dict)

        """

        return self.__links

    def get_all_models(self):
        """
        Gets all the models that have been loaded into the Coordinator

        Returns: dictionary of summarized models that have been loaded
                 (type:dict)

        """

        return self.__models

    def get_links_btwn_models(self, from_model_id, to_model_id):
        """
        Gets all information related to a link between the specified models
        Args:
            from_model_id: id of the source model (type:string)
            to_model_id: id of the target model (type:string)

        Returns: list of link dictionary objects (one for each exchange item
                 on the link)

        """

        links = []
        for linkid, link in self.__links.iteritems():
            source_id = link.source_component().id()
            target_id = link.target_component().id()
            if source_id == from_model_id and target_id == to_model_id:
                links.append(link)
        return links

    def get_exchange_items(self, modelid,
                           exchange_item_type=stdlib.ExchangeItemType.INPUT):
        """
        Gets all information related to input or output exchange items for a
        specific model
        Args:
            modelid: id of the model for which the exchange item will be
                     retrieved (type:string)
            exchange_item_type: the type of exchange item to retrieve
                                (type: stdlib.ExchangeItemType)

        Returns: exchange items based on model id

        """

        # get model by id
        model = self.get_model(modelid)

        # get input or output exchange items
        if exchange_item_type == stdlib.ExchangeItemType.INPUT:
            items = model.get_input_exchange_items()
        elif exchange_item_type == stdlib.ExchangeItemType.OUTPUT:
            items = model.get_output_exchange_items()
        else:
            sPrint('Invalid exchange item type provided', MessageType.ERROR)
            return None

        return items

    def update_link(self, link_id, from_geom_dict, from_to_spatial_map):

        link = self.__links[link_id]
        t_item = link.target_exchange_item()

        # loop through each of the from geoms
        for t_geom in t_item.geometries():

            # get this list index of the to-geom
            mapped = next((g for g in from_to_spatial_map if g[1] == t_geom),
                          0)

            # if mapping was found
            if mapped:

                f_geom, t_geom = mapped

                # update the datavalues with the mapped dates and values
                t_geom.datavalues().set_timeseries(from_geom_dict[f_geom])

        # todo:
        # loop through spatial map array
        for f, t in from_to_spatial_map:
            if t is not None:
                pass

    def update_links(self, model, exchangeitems):
        """
        Updates the model associated with the link.  This is necessary after
        the run phase to update the data values stored on the link object
        Args:
            model: model object that will be updated (type:engine.Model)
            exchangeitems: list of exchange item to be updated
                           (type:stdlib.ExchangeItem)

        Returns: None

        """

        name = model.name()
        for id, link_inst in self.__links.iteritems():
            f, t = link_inst.get_link()

            if t[0].name() == name:
                for item in exchangeitems:
                    if t[1].name() == item.name():
                        self.__links[id] = Link(id, f[0], t[0], f[1], item)

            elif f[0].name() == name:
                for item in exchangeitems:
                    if f[1].name() == item.name():
                        self.__links[id] = Link(id, f[0], t[0], item, t[1])

    def determine_execution_order(self):
        """
        Determines the order in which models will be executed.
        
        Returns: a list of ordered model ids 

        """

        g = net.DiGraph()

        # create links between these nodes
        for id, link in self.__links.iteritems():

            from_node = link.source_component().id()
            to_node = link.target_component().id()
            g.add_edge(from_node, to_node)

        # determine cycles
        cycles = net.recursive_simple_cycles(g)
        for cycle in cycles:
            # remove edges that form cycles
            g.remove_edge(cycle[0], cycle[1])

        # perform toposort
        order = net.topological_sort(g)

        # re-add bidirectional dependencies (i.e. cycles)
        for cycle in cycles:
            # find index of inverse link
            for i in xrange(0,len(order)-1):
                if order[i] == cycle[1] and order[i+1] == cycle[0]:
                    order.insert(i+2, cycle[1])
                    order.insert(i+3, cycle[0])
                    break


        # return single model if one model and no links
        if len(order) == 0:
            if len(self.__models) == 1:
                order = [self.__models.values()[0].id()]

        # return execution order
        return order

    def run_simulation(self, simulationName=None, dbName=None, user_info=None,
                       datasets=None):
        """
        Executes a model simulation.

        Args:
            simulationName: Name of the simulation
            dbName: name of the database to save results
            user_info: user's information 
            datasets: datasets to save

        Returns: dict(success=True, message='') or 0

        """

        # create data info instance if all the necessary info is provided
        ds = None
        if None not in [simulationName, dbName, user_info, datasets]:
            db = self.get_db_args_by_name(dbName)
            ds = run.dataSaveInfo(simulationName, db, user_info, datasets)

        # determine if the simulation is feed-forward or time-step
        models = self.Models()
        types = []
        for model in models.itervalues() :
            types.extend(inspect.getmro(model.instance().__class__))

        # make sure that feed forward and time-step models are not mixed
        if (feed_forward.Wrapper in types) and \
                (time_step.time_step_wrapper in types):
            return dict(success=False,
                        message='Cannot mix feed-forward and '
                                'time-step models')

        else:
            # threadManager = ThreadManager()
            t = None
            if feed_forward.Wrapper in types:
                t = threading.Thread(target=run.run_feed_forward,
                                     args=(self, ds),
                                     name='Engine_RunFeedForward')
                t.start()

            elif time_step.time_step_wrapper in types:

                t = threading.Thread(target=run.run_time_step,
                                     args=(self, ds),
                                     name='Engine_RunTimeStep')
                t.start()

            if t is not None:
                t.join()

                # check the status of each model to determine of
                # simulation was successful
                for m in models.itervalues():
                    if m.instance().status() != stdlib.Status.SUCCESS:
                        return dict(success=False,
                                    event='onSimulationFail',
                                    result={'msg':'Error occurred during simulation '
                                        'in model: {%s}' % m.name()})

                return dict(success=True, event='onSimulationSuccess',
                            result={'msg': 'Simulation Completed Successfully'})

    def connect_to_db(self, title, desc, engine, address, dbname, user, pwd,
                      default=False):
        """
        Establishes a connection with a database for saving simulation results

        Args:
            title: title to give database (local use only)
            desc: database description
            engine: the engine that should be used to connect to the data
                    base (e.g. postgres)
            address: address of the database
            dbname: name of the database to connect with (server name)
            user: user name, required to establish a connection
            pwd:  password for connecting to the database
            default: designates if this database should be used as the default
                     for saving simulation results

        Returns: returns database id 

        """

        connection = gui.connect_to_db(title, desc, engine, address, dbname,
                                       user, pwd)

        if connection:
            dbs = self.add_db_connection(connection)

            if default:
                self.set_default_database(connection.keys()[0])

            return connection.keys()
        return None

    def load_simulation(self, simulation_file):
        """
        loads an existing simulation into the coordinator
        Args:
            simulation_file: file that defines the simulation (*.sim)

        Returns: None

        """

        if simulation_file is list:
            abspath = os.path.abspath(simulation_file[0])
        else:
            abspath = os.path.abspath(simulation_file)

        link_objs = []
        if os.path.isfile(abspath):
            with open(abspath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    command = line.strip()
                    if len(command) > 0:
                        if command[0] != '#':
                            # print '%s'%command
                            terminal.parse_args(command.split(' '))

                            if 'link' in command:
                                link_objs.append(command.split(' ')[1:])

            # return the models and links created
            return self.__models.values(), self.__links.values(), link_objs

        else:
            elog.error('Could not find path %s' % simulation_file)

    def show_db_results(self, args):
        """
        displays the results that were saved to the database

        Args:
            args: database args

        Returns: None

        """

        # get database id
        db_id = args[0]

        if db_id not in self._db:
            elog.error('could not find database id: %s' % db_id)
            return

        # get all result entries
        self.coreread = readCore(self._db[db_id]['session'])

        results = self.coreread.getAllResult()

        if results:
            elog.info('Id   Type     Variable    Unit    ValueCount')
            for result in results:
                elog('%s    %s   %s  %s  %s ' %
                     (result.ResultID,
                      result.ResultTypeCV,
                      result.VariableObj.VariableCode,
                      result.UnitObj.UnitsName,
                      result.ValueCount))
        else:
            elog.info('No results found')


class Serializable(Coordinator):
    """
    This class returns serializable objects for Engine functions, ideally for
    multiprocessing.
    """
    def __init__(self):
        super(Serializable, self).__init__()

    @staticmethod
    def __summarize_exhange_item(item):
        """
        Summarizes exchange item information into a serializable object

        Args:
            item: the exchange item to summarize (type:stdlib.ExchangeItem)

        Returns: summarized exchange item (type:dict)

        """

        # get data that is common for all geometries
        geom_srs = item.srs().ExportToPrettyWkt()
        geom_count = len(item.getGeometries2())
        geom_type = item.getGeometries2()[0].GetGeometryType()
        geom_extent = 'Not Implemented Yet'

        # initialize the geometry dictionary
        geom_dict = dict(srs=geom_srs,
                         type=geom_type,
                         count=geom_count,
                         extent=geom_extent,
                         wkb=[],
                         hash=[])

        # get the geometries and hashes
        geometries = item.getGeometries2()
        geoms = [g.ExportToWkb() for g in geometries]
        hashs = [g.hash for g in geometries]

        geom_dict['wkb'] = geoms
        geom_dict['hash'] = hashs

        return dict(name=item.name(),
                    description=item.description(),
                    id=item.id(),
                    unit=item.unit(),
                    variable=item.variable(),
                    type=item.type(),
                    geometry=geom_dict)

    def connect_to_db(self, title, desc, engine, address, dbname, user, pwd,
                      default=False):
        """
        Establishes a connection with a database for saving simulation results
        and returns the connection id

        Args:
            title: title to give database (local use only)
            desc: database description
            engine: the engine that should be used to connect to the data base
                    (e.g. postgres)
            address: address of the database
            dbname: name of the database to connect with (server name)
            user: user name, required to establish a connection
            pwd:  password for connecting to the database
            default: designates if this database should be used as the default
                     for saving simulation results

        Returns: dict(success:True or False, result{ids:[connection id] or
                                                                         None})

        """

        db_ids = super(Serializable, self).connect_to_db(title, desc, engine,
                                                         address, dbname, user,
                                                         pwd)

        if db_ids is None:
            return {'success': False, 'result': None}
        else:
            return {'success': True, 'result': {'ids': db_ids}}

    def get_db_connections(self):
        """
        Gets all database connections that have been loaded in the Coordinator
        in a serializable dictionary

        Returns: dictionary of database connection information (type:dict)

        """

        res = super(Serializable, self).get_db_connections()

        db = {}
        for db_id in res.iterkeys():
            args = self._db[db_id]['args']
            if isinstance(args['address'], sqlalchemy.engine.url.URL):
                args['address'] = self._db[db_id]['connection_string'].database

            db[db_id] = {'name': self._db[db_id]['name'],
                         'description': self._db[db_id]['description'],
                         'connection_string':
                             self._db[db_id]['connection_string'],
                         'id': db_id, 'args': args}

        return {'success': True, 'result': db}

    def add_model(self, **params):
        """
        Adds a model to the engine
        Args:
            **params:  id: modelid
                       config_params

        Returns:  dict(success:True or False, result:{id:id, name:model name,
                  model_type:simulation type} or None)

        """

        res = super(Serializable, self).add_model(**params)

        if res is None:
            return {'success': False, 'result': None}
        else:
            result = dict(id=res.id(), name=res.name(), model_type=res.type())
            return {'success': True, 'result': result}

    def get_all_models(self):
        """
        gets all the models that are loaded in the coordinator
        Returns: serializable dictionary of all models

        """
        models = super(Serializable, self).get_all_models()

        model_list = []
        for m in models:

            model_list.append(
                {'params': models[m].get_config_params(),
                    'name':models[m].name(),
                    'id': models[m].id(),
                    'description': models[m].description(),
                    'type': models[m].type(),
                    'attrib': models[m].attrib()
                 }
            )
        return {'success': True, 'result': models}

    def get_exchange_items(self, modelid,
                           eitype=stdlib.ExchangeItemType.INPUT):

        eis = super(Serializable, self).get_exchange_items(modelid, eitype)

        if eis is None:
            return {'success': False, 'result': None}
        else:
            res = []
            for ei in eis:
                res.append(self.__summarize_exhange_item(ei))
            return {'success': 'True', 'result': res}

    def get_model_by_id(self, modelid):
        """
        Gets a summarized version of the model by id

        Args:
            modelid: id of the model to return (type:string)

        Returns: dictionary of summarized metadata (type:dict)

        """

        model = super(Serializable, self).get_model(modelid)

        if model is not None:
            res = {'params': model.get_config_params(),
                   'name': model.name(),
                   'id': model.id(),
                   'description': model.description(),
                   'type': model.type(),
                   'attrib': model.attrib()
                   }
            return {'success': True, 'result': res}

        return {'success': False, 'result': None}

    def remove_all_models_and_links(self):
        res = super(Serializable, self).remove_all_models_and_links()
        return {'success': True, 'result': res}

    def remove_model(self, modelid):
        """
        Removes a model from the Coordinator by id

        Args:
            model_id: id of the model to remove (type:string)

        Returns: the id of the model that was removed or None
                 (type:string or None)

        """

        res = super(Serializable, self).remove_model(modelid)

        if res is not None:
            return {'success': True, 'result': res}
        else:
            return {'success': False, 'result': None}

    def get_links_btwn_models(self, from_model_id, to_model_id):
        """
        Gets all information related to a link between the specified models
        Args:
            from_model_id: id of the source model (type:string)
            to_model_id: id of the target model (type:string)

        Returns: list of link dictionary objects (one for each exchange item on
                 the link)

        """

        links = super(Serializable, self).get_links_btwn_models(from_model_id,
                                                                to_model_id)

        serialized_links = []

        for link in links:
            source_id = link.source_component().id()
            target_id = link.target_component().id()

            # links.append(link)
            spatial = link.spatial_interpolation().name() \
                if link.spatial_interpolation() is not None else 'None'
            temporal = link.temporal_interpolation().name() \
                if link.temporal_interpolation() is not None else 'None'

            d = dict(id=link.get_id(),
                     source_id=source_id,
                     target_id=target_id,
                     source_name=link.source_component().name(),
                     target_name=link.target_component().name(),
                     source_item=link.source_exchange_item().name(),
                     target_item=link.target_exchange_item().name(),
                     spatial_interpolation=spatial,
                     temporal_interpolation=temporal)
            serialized_links.append(d)

        return {'success': True, 'result': serialized_links}

    def remove_link_by_id(self, linkid):

        res = super(Serializable, self).remove_link_by_id(linkid)
        if res:
            return {'success': True, 'result': res}
        else:
            return {'success': False, 'result': res}

    def add_link(self, from_id, from_item_id, to_id, to_item_id,
                 spatial_interp=None, temporal_interp=None, uid=None):
        """
        Creates a new link in the Coordinator

        Args:
            from_id: id of the source model (type:string)
            from_item_id: id of the source exchange item (type:string)
            to_id: id of the target model (type:string)
            to_item_id: id of the target exchange item (type:string)
            spatial_interp: spatial_interpolation
            temporal_interp: temporal_interpolation
            uid: unique id for the link

        Returns: id of the link that was created or 0

        """

        res = super(Serializable, self).add_link(from_id, from_item_id, to_id,
                                                 to_item_id, spatial_interp,
                                                 temporal_interp, uid)

        if res is not None:
            return {'success': True, 'result': {'id': res.get_id()}}
        else:
            return {'success': False, 'result': None}

    def get_all_links(self):
        """
        Gets all links that have been created/loaded in the Coordinator

        Returns: dictionary of summarized link information (type:dict)

        """

        link_dict = super(Serializable, self).get_all_links()

        links = []
        for l in link_dict.iterkeys():
            spatial = 'None'
            temporal = 'None'

            # set spatial and temporal values, if they exist
            if link_dict[l].spatial_interpolation() is not None:
                spatial = link_dict[l].spatial_interpolation().name()

            if link_dict[l].temporal_interpolation() is not None:
                temporal = link_dict[l].temporal_interpolation().name()

            # build serializable dictionary
            links.append(dict(
                        id=l,
                        output_name=link_dict[l].source_exchange_item().name(),
                        output_id=link_dict[l].source_exchange_item().id(),
                        input_name=link_dict[l].target_exchange_item().name(),
                        input_id=link_dict[l].target_exchange_item().id(),
                        spatial_interpolation=spatial,
                        temporal_interpolation=temporal,
                        source_component_name=link_dict[l].source_component().name(),
                        target_component_name=link_dict[l].target_component().name(),
                        source_component_id=link_dict[l].source_component().id(),
                        target_component_id=link_dict[l].target_component().id()
                        )
                    )
        return {'success': True, 'result': links}
