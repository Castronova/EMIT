import threading
import sqlalchemy
import networkx as net
from coordinator import help as h
from utilities.gui import *
from utilities.mdl import *
from transform import space_base
from transform import time_base
from wrappers import odm2_data
from wrappers import feed_forward
from wrappers import time_step
import run
from api_old.ODM2.Core.services import *
from coordinator.emitLogging import elog
from datetime import datetime
import users as Users
import wrappers
from sprint import *

"""
Purpose: This file contains the logic used to run coupled model simulations
"""


class EngineStatus(object):

    def __init__(self):
        self.__engineStatus = stdlib.Status.UNDEFINED
    def set(self, status=stdlib.Status.UNDEFINED):
        if status in dir(stdlib.Status):
            self.__engineStatus = status
        else:
            sPrint('Failed to set engine status.  Status must by instance of stdlib.Status')
    def get(self):
        return self.__engineStatus
    def __str__(self):
        return 'The Engine status is currently set to: %s' % self.__engineStatus

class Link(object):
    """
    stores info about the linkage between two components
    """
    def __init__(self, id, from_linkable_component, to_linkable_component, from_item, to_item):
        # TODO: this is not finished, just mocked up
        self.__from_lc = from_linkable_component
        self.__from_item = from_item

        self.__to_lc = to_linkable_component
        self.__to_item = to_item

        self.__id = id

        self.__spatial_interpolation = None
        self.__temporal_interpolation = None

    # todo: this should be replaced by accessors for each of the from_lc,to_lc,from_item,to_item
    def get_link(self):
        elog.error('[Deprecated] This function has been deprecated...do not use! ')
        elog.error('[Deprecated] main.py -> get_link()')

        return [self.__from_lc,self.__from_item], [self.__to_lc,self.__to_item]

    def source_exchange_item(self):
        return self.__from_item

    def target_exchange_item(self):
        return self.__to_item

    def source_component(self):
        return self.__from_lc

    def target_component(self):
        return self.__to_lc

    def get_id(self):
        return self.__id

    def spatial_interpolation(self, value=None):
        if value is not None:
            if isinstance(value, space_base.Space):
                self.__spatial_interpolation = value
        return self.__spatial_interpolation

    def temporal_interpolation(self, value=None):
        if value is not None:
            if isinstance(value, time_base.Time):
                self.__temporal_interpolation = value
        return self.__temporal_interpolation

class Model(object):
    """
    defines a model that has been loaded into a configuration
    """
    def __init__(self, id, name, instance, desc=None, input_exchange_items=[], output_exchange_items=[], params=None):
        self.__description = desc
        self.__iei = {}
        self.__oei = {}
        self.__id = id
        self.__params = params
        self.__attrib  = {}

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance
        self.__params_path = None

    def type(self,value=None):
        return self.instance().type()

    def attrib(self, value=None):
        """
        Provides a method for storing model specific attributes
        """
        if value is not None:
            self.__attrib = value
        return self.__attrib

    def get_input_exchange_items(self):
        if len(self.__iei.keys()) > 0:
            return [j for i,j in self.__iei.items()]
        else: return []

    def get_output_exchange_items(self):
        if len(self.__oei.keys()) > 0:
            return [j for i,j in self.__oei.items()]
        else: return []

    def get_input_exchange_item_by_name(self,value):

        i = self.instance()
        if value in i.inputs():
            return i.inputs()[value]
        else:
            elog.error('Could not find Input Exchange Item: '+value)

    def get_output_exchange_item_by_name(self,value):

        i = self.instance()
        if value in i.outputs():
            return i.outputs()[value]
        else:
            elog.error('Could not find Output Exchange Item: '+value)


    def description(self):
        return self.__description

    def name(self):
        return self.instance().name()

    def id(self):
        return self.__id

    def instance(self):
        return self.__inst

    def get_config_params(self):
        return self.__params

    def params_path(self, value=None):
        if value is not None:
            self.__params_path = value
        return self.__params_path

class Coordinator(object):
    def __init__(self):
        """
        globals
        """
        self.__models = {}
        self.__links = {}
        self._db = {}
        self.__default_db = None
        self.status = EngineStatus()

        # TODO: Get this from gui dialog
        self.preferences = os.path.abspath(os.path.join(os.path.dirname(__file__),'../data/preferences'))

    def get_status(self):
        """
        Returns: the current status of the Engine.
        """
        return self.status.get()

    def Models(self, model=None):
        if model is not None:
            self.__models[model.name()] = model
        return self.__models

    def add_db_connection(self,value):

        self._db.update(value)
        return self._db

    def get_db_connections(self):
        # return the database connection dictionary without sqlalchemy objects
        db = {}
        for db_id in self._db.iterkeys():
            args =  self._db[db_id]['args']

            # todo: remove this by migrating all databases to the latest ODM2 and use ODM2PythonAPI exclusively
            # make sure address is the string location of the database (this is necessary to be compatible with the old ODM2 and ODM2PythonAPI)(
            if isinstance(args['address'], sqlalchemy.engine.url.URL):
                args['address'] = self._db[db_id]['connection_string'].database

            db[db_id] = {'name': self._db[db_id]['name'],
                         'description': self._db[db_id]['description'],
                         'connection_string': self._db[db_id]['connection_string'],
                         'id': db_id, 'args': args}
        return db


    def get_db_args_by_name(self, db_name):
        # return the database args dictionary for a given name
        db = {}
        for db_id in self._db.iterkeys():
            database = self._db[db_id]
            if database['name'] == db_name:
                return database['args']
        return None

    def set_default_database(self,db_id=None):

        if db_id is not None:
            try:
                self.__default_db = self._db[db_id]
                self.__default_db['id'] = db_id
                sPrint('Default database : %s'%self._db[db_id]['connection_string'], MessageType.INFO)
            except Exception, e :
                msg = 'Encountered and error when setting default database: %s' % e
                elog.error(msg)
                sPrint(msg, MessageType.ERROR)
        else:
            sPrint('Could not set the default database', MessageType.ERROR)

    def get_default_db(self):
        if self.__default_db is None:
            return None
        else:
            return self.__default_db

    def add_model(self, id=None, attrib=None):
        """
        stores model component objects when added to a configuration
        """

        thisModel = None
        sPrint('Adding Model in Engine', MessageType.DEBUG)
        if id is None:
            id = 'M' + uuid.uuid4().hex


        if 'type' in attrib.keys():

            sPrint('Found type', MessageType.DEBUG)

            try:
                getattr(wrappers, attrib['type'])
            except:
                elog.critical('Could not locate wrapper of type %s.  Make sure the wrapper is specified in wrappers.__init__.' % (attrib['type']))
                sPrint('Could not locate wrapper of type %s.  Make sure the wrapper is specified in wrappers.__init__.' % (attrib['type']), MessageType.CRITICAL)

            sPrint('Instantiating the component wrapper', MessageType.DEBUG)
            # instantiate the component wrapper
            inst = getattr(wrappers, attrib['type']).Wrapper(attrib)
            oei = inst.outputs().values()
            iei = inst.inputs().values()
            sPrint('Model Instantiated', MessageType.DEBUG)

            # create a model instance
            thisModel = Model(id=id,
                              name=inst.name(),
                              instance=inst,
                              desc=inst.description(),
                              input_exchange_items= iei,
                              output_exchange_items=  oei,
                              params=attrib)
            thisModel.attrib(attrib)

        elif 'mdl' in attrib:
        # if type == datatypes.ModelTypes.FeedForward or type == datatypes.ModelTypes.TimeStep:

            sPrint('Found MDL', MessageType.DEBUG)

            ini_path = attrib['mdl']

            # exit early if mdl doesn't exist
            if not os.path.exists(ini_path):
                sPrint('Could not locate *.mdl at location: %s' % ini_path)
                return 0

            # parse the model configuration parameters
            params = parse_config(ini_path)

            if params is not None:

                try:
                    # load model
                    sPrint('Loading Model', MessageType.DEBUG)
                    name, model_inst = load_model(params)
                    sPrint('Finished Loading', MessageType.DEBUG)
                    # make sure this model doesnt already exist
                    if name in self.__models:
                        elog.warning('Model named '+name+' already exists in configuration')
                        sPrint('Model named '+name+' already exists in configuration', MessageType.WARNING)
                        return None

                    iei = model_inst.inputs().values()
                    oei = model_inst.outputs().values()

                    # create a model instance
                    thisModel = Model(id= id,
                                      name=model_inst.name(),
                                      instance=model_inst,
                                      desc=model_inst.description(),
                                      input_exchange_items= iei,
                                      output_exchange_items= oei,
                                      params=params)

                    thisModel.params_path(ini_path)
                    thisModel.attrib(attrib)

                except Exception, e:
                    sPrint('Encountered an error while loading model: %s' % e, MessageType.ERROR)
                    elog.error('Encountered an error while loading model: %s' % e)
                    thisModel = None


        elif 'databaseid' in attrib and 'resultid' in attrib:

            databaseid = attrib['databaseid']
            resultid = attrib['resultid']

            # get the database session
            session = self._db[databaseid]['session']

            # create odm2 datamodel instance
            inst = odm2_data.odm2(resultid=resultid, session=session)
            oei = inst.outputs().values()

            # Make sure the series is not already in the canvas
            # List of canvas models are kept as a dict with keys in the format of 'NAME-ID'
            if inst.name()+'-'+resultid in self.__models:
                elog.warning('Series named '+inst.name()+' already exists in configuration')
                sPrint('Series named '+inst.name()+' already exists in configuration', MessageType.WARNING)
                return None

            # create a model instance
            thisModel = Model(id=id,
                              name=inst.name(),
                              instance=inst,
                              desc=inst.description(),
                              input_exchange_items= [],
                              output_exchange_items=  oei,
                              params=None)


            # save the result and database ids
            att = {'resultid':resultid}
            att['databaseid'] = databaseid
            thisModel.attrib(att)

        if thisModel is not None:
            # save the model
            self.__models[thisModel.name()] = thisModel
            sPrint('Model Loaded', MessageType.DEBUG)
            return {'id':thisModel.id(), 'name':thisModel.name(), 'model_type':thisModel.type()}
        else:
            elog.error('Failed to load model.')
            sPrint('Failed to load model.', MessageType.ERROR)
            return 0

    def remove_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].id() == id:

                # remove the model
                self.__models.pop(m,None)

                # find all links associated with the model
                remove_these_links  = []
                for l in self.__links:
                    FROM, TO = self.__links[l].get_link()
                    if FROM[0].id() == id or TO[0].id() == id:
                        remove_these_links.append(l)

                # remove all links associated with the model
                for link in remove_these_links:
                    self.__links.pop(link,None)

                return id
        return None

    def get_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].id() == id:
                return self.__models[m]
        return None

    def add_link(self,from_id, from_item_id, to_id, to_item_id, spatial_interp=None, temporal_interp=None, uid=None):
        """
        adds a data link between two components
        """

        # check that from and to models exist in composition
        From = self.get_model_by_id(from_id)
        To = self.get_model_by_id(to_id)
        try:

            if self.get_model_by_id(from_id) is None: raise Exception('> '+from_id+' does not exist in configuration')
            if self.get_model_by_id(to_id) is None: raise Exception('> ' + to_id+' does not exist in configuration')
        except Exception, e:
            elog.error(e)
            return 0

        # check that input and output exchange items exist
        ii = To.get_input_exchange_item_by_name(to_item_id)
        oi = From.get_output_exchange_item_by_name(from_item_id)

        if ii is not None and oi is not None:
            # generate a unique model id
            if uid is None:
                id = 'L'+uuid.uuid4().hex
            else:
                id = uid

            # create link
            link = Link(id,From,To,oi,ii)

            # add spatial and temporal interpolations
            if spatial_interp is not None:
                link.spatial_interpolation(spatial_interp)
            if temporal_interp is not None:
                link.temporal_interpolation(temporal_interp)

            # save the link
            self.__links[id] = link

            # return link
            return link.get_id()
        else:
            elog.warning('Could Not Create Link :(')
            return 0

    def add_link_by_name(self,from_id, from_item_name, to_id, to_item_name):
        """
        adds a data link between two components
        """

        # check that from and to models exist in composition
        From = self.get_model_by_id(from_id)
        To = self.get_model_by_id(to_id)
        try:

            if self.get_model_by_id(from_id) is None: raise Exception(from_id+' does not exist in configuration')
            if self.get_model_by_id(to_id) is None: raise Exception(to_id+' does not exist in configuration')
        except Exception, e:
            elog.error(e)
            return None

        # check that input and output exchange items exist
        ii = To.get_input_exchange_item_by_name(to_item_name)
        oi = From.get_output_exchange_item_by_name(from_item_name)

        if ii is not None and oi is not None:
            # generate a unique model id
            #id = 'L'+str(self.get_new_id())
            id = 'L'+uuid.uuid4().hex[:5]

            # create link
            link = Link(id,From,To,oi,ii)
            self.__links[id] = link

            return link
        else:
            elog.warning('Could Not Create Link :(')

    def get_from_links_by_model(self, model_id):

        """
        returns only the links where the corresponding linkable component is the FROM item.
        This is useful for determining where data will pass (direction)
        """

        links = {}
        for linkid, link in self.__links.iteritems():
            # get the from/to link info

            if link.source_component().id() == model_id:
                links[linkid] = link

        return links

    def get_all_links(self):
        links = []
        for l in self.__links.iterkeys():

            spatial = self.__links[l].spatial_interpolation().name() \
                if self.__links[l].spatial_interpolation() is not None \
                else 'None'
            temporal = self.__links[l].temporal_interpolation().name() \
                if self.__links[l].temporal_interpolation() is not None \
                else 'None'
            links.append(dict(
                        id=l,
                        output_name=self.__links[l].source_exchange_item().name(),
                        output_id=self.__links[l].source_exchange_item().id(),
                        input_name=self.__links[l].target_exchange_item().name(),
                        input_id=self.__links[l].target_exchange_item().id(),
                        spatial_interpolation=spatial,
                        temporal_interpolation=temporal,
                        source_component_name=self.__links[l].source_component().name(),
                        target_component_name=self.__links[l].target_component().name(),
                        source_component_id=self.__links[l].source_component().id(),
                        target_component_id=self.__links[l].target_component().id(),
                            ))
        return links

    def get_all_models(self):
        models = []
        for m in self.__models:

            models.append(
                {'params': self.__models[m].get_config_params(),
                    'name': self.__models[m].name(),
                    'id': self.__models[m].id(),
                    'description': self.__models[m].description(),
                    'type': self.__models[m].type(),
                    'attrib': self.__models[m].attrib(),
                    }
            )
        return models

    def summarize_exhange_item(self, item, returnGeoms=True):

        # get data that is common for all geometries
        geom_srs = item.srs().ExportToPrettyWkt()
        geom_count = len(item.getGeometries2())
        geom_type = item.getGeometries2()[0].GetGeometryType()
        geom_extent = 'Not Implemented Yet'

        # initialize the geometry dictionary
        geom_dict = dict(srs = geom_srs,
                         type = geom_type,
                         count = geom_count,
                         extent = geom_extent,
                         wkb = [],
                         hash = [])

        if returnGeoms:

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

    def get_exchange_item_info(self, modelid, exchange_item_type=stdlib.ExchangeItemType.INPUT, returnGeoms=True):

        ei_values = []

        # get model by id
        model = self.get_model_by_id(modelid)

        # get input or output exchange items
        if exchange_item_type == stdlib.ExchangeItemType.INPUT:
            items = model.get_input_exchange_items()
        elif exchange_item_type == stdlib.ExchangeItemType.OUTPUT:
            items = model.get_output_exchange_items()
        else:
            sPrint('Invalid exchange item type provided')
            return None

        for i in items:
            ei_values.append(self.summarize_exhange_item(i, returnGeoms))

        return ei_values

    def update_link(self, link_id, from_geom_dict, from_to_spatial_map):
        """
        Updates a specific link.
        values stored on the link object
        :param model:
        :return:
        """

        link = self.__links[link_id]
        t_item = link.target_exchange_item()
        f_item = link.source_exchange_item()

        # loop through each of the from geoms
        for t_geom in t_item.geometries():

            # get this list index of the to-geom
            mapped = next((g for g in from_to_spatial_map if g[1] == t_geom), 0)

            # if mapping was found
            if mapped:

                f_geom ,t_geom= mapped

                # update the datavalues with the mapped dates and values
                t_geom.datavalues().set_timeseries(from_geom_dict[f_geom])

        # todo:
        # loop through spatial map array
        for f,t in from_to_spatial_map:
            if t != None:
                pass

    def update_links(self, model, exchangeitems):
        """
        Updates the model associated with the link.  This is necessary after the run phase to update the data
        values stored on the link object
        :param model:
        :return:
        """

        name = model.name()
        for id,link_inst in self.__links.iteritems():
            f,t = link_inst.get_link()

            if t[0].name() == name:
                for item in exchangeitems:
                    if t[1].name() == item.name():
                        self.__links[id] = Link(id, f[0], t[0], f[1], item)
                        #t[1] = item

            elif f[0].name() == name:
                for item in exchangeitems:
                    if f[1].name() == item.name():
                        self.__links[id] = Link(id, f[0], t[0], item, t[1])
                        #f[1] = item

    def determine_execution_order(self):
        """
        determines the order in which models will be executed.
         def get_link(self):
        return [self.__from_lc,self.__from_item], [self.__to_lc,self.__to_item]

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
            g.remove_edge(cycle[0],cycle[1])

        # perform toposort
        order = net.topological_sort(g)

        # re-add bidirectional dependencies (i.e. cycles)
        for cycle in cycles:
            # find index of inverse link
            for i in xrange(0,len(order)-1):
                if order[i] == cycle[1] and order[i+1] == cycle[0]:
                    order.insert(i+2, cycle[1])
                    order.insert(i+3,cycle[0])
                    break


        # return single model if one model and no links
        if len(order) == 0:
            if len(self.__models) == 1:
                order = [self.__models.values()[0].id()]

        # return execution order
        return order

    def run_simulation(self, simulationName=None, dbName=None, user_info=None, datasets=None):
        """
        coordinates the simulation effort
        """

        # create data info instance if all the necessary info is provided
        ds = None
        if None not in [simulationName, dbName, user_info, datasets]:
            db = self.get_db_args_by_name(dbName)

            # user_list= Users.BuildAffiliationfromJSON(user_info)

            ds = run.dataSaveInfo(simulationName, db, user_info, datasets)

        try:
            # determine if the simulation is feed-forward or time-step
            models = self.Models()
            types = []
            for model in models.itervalues() :
                types.extend(inspect.getmro(model.instance().__class__))

            # make sure that feed forward and time-step models are not mixed together
            if (feed_forward.Wrapper in types) and (time_step.time_step_wrapper in types):
                return dict(success=False, message='Cannot mix feed-forward and time-step models')

            else:
                # threadManager = ThreadManager()
                if feed_forward.Wrapper in types:
                    t = threading.Thread(target=run.run_feed_forward, args=(self,ds), name='Engine_RunFeedForward')
                    t.start()
                    # run.run_feed_forward(self)
                elif time_step.time_step_wrapper in types:

                    t = threading.Thread(target=run.run_time_step, args=(self,ds), name='Engine_RunTimeStep')
                    t.start()
                    #run.run_time_step(self)

            return dict(success=True, message='')

        except Exception as e:
            elog.debug(e)
            return dict(success=False, message=e)
            # raise Exception(e.args[0])



    def connect_to_db(self, title, desc, engine, address, name, user, pwd, default=False):

        connection = connect_to_db(title, desc, engine, address, name, user, pwd)

        if connection:
            dbs = self.add_db_connection(connection)

            if default:
                self.set_default_database(connection.keys()[0])

            return {'success':True, 'ids':connection.keys()}
        else:
            return {'success':False, 'ids':None}

    # todo: remove this function.  we only need connect_to_db, this parsing can be done in gui utils
    def connect_to_db_from_file(self,filepath=None):

        if filepath is None: return {'success':False, 'ids':None}

        if os.path.isfile(filepath):
            try:
                connections = create_database_connections_from_file(filepath)
                self._db = connections

                # set the default connection
                for id,conn in connections.iteritems():
                    if 'default' in conn['args']:
                        if conn['args']['default']:
                            self.set_default_database(db_id=id)
                            break
                if not self.get_default_db():
                    self.set_default_database()

                return {'success':True, 'ids':connections.keys()}
            except Exception, e:
                elog.error(e)
                elog.error('Could not create connections from file ' + filepath)
                sPrint('Could not create connection: %s'%e, MessageType.ERROR, PrintTarget.CONSOLE)

                return {'success':False, 'ids':None}

        else:
            return {'success':False, 'ids':None}


    def load_simulation(self, simulation_file):

        if simulation_file is list:
            abspath = os.path.abspath(simulation_file[0])
        else:
            abspath = os.path.abspath(simulation_file)

        link_objs = []
        if os.path.isfile(abspath):
            with open(abspath,'r') as f:
                lines = f.readlines()
                for line in lines:
                    command = line.strip()
                    if len(command) > 0:
                        if command[0] != '#':
                            # print '%s'%command
                            self.parse_args(command.split(' '))

                            if 'link' in command:
                                link_objs.append(command.split(' ')[1:])

            # return the models and links created
            return self.__models.values(), self.__links.values(), link_objs

        else:
            elog.error('Could not find path %s' % simulation_file)


    def show_db_results(self, args):

        # get database id
        db_id = args[0]

        if db_id not in self._db:
            elog.error('could not find database id: %s' % db_id)
            return


        # get all result entries
        self._coreread = readCore(self._db[db_id]['session'])

        results = self._coreread.getAllResult()

        if results:
            elog.info('Id   Type     Variable    Unit    ValueCount')
            for result in results:
                elog('%s    %s   %s  %s  %s '%(result.ResultID, result.ResultTypeCV,result.VariableObj.VariableCode,
                                         result.UnitObj.UnitsName,result.ValueCount))
        else:
            elog.info('No results found')

