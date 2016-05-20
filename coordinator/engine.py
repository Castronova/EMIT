import threading

import networkx as net
import sqlalchemy

import run
import wrappers
from api_old.ODM2.Core.services import *
from emitLogging import elog
from sprint import *
from transform import space_base
from transform import time_base
from utilities.gui import *
from utilities.mdl import *
from wrappers import feed_forward
from wrappers import odm2_data
from wrappers import time_step

"""
Purpose: This file contains the logic used to run coupled model simulations
"""


class EngineStatus(object):
    """
    Defines the current status of the Engine.  Status is defined using the stdlib.Status class
    """

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
    def __init__(self, id, from_linkable_component, to_linkable_component, from_item, to_item):
        """
        defines the link object.  Links are used to pass data between models during simulation runtime. This class
        captures the information that is necessary to define a unique linkage between model components.

        Args:
            id: unique id for the link object (type:string)
            from_linkable_component: the component object that is providing output  (type:Engine.Model)
            to_linkable_component: the component object that is accepting input (type:Engine.Model)
            from_item: The exchange item that is passed as output (type: stdlib.ExchangeItem)
            to_item: the exchange item that is accepted as input (type: stdlib.ExchangeItem)

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
        Gets the Engine.Model and Stdlib.ExchangeItem objects that comprise the like object
        Returns: tuple( [from model, from exchange item], [to model, to exchange item] )

        """

        return [self.__from_lc,self.__from_item], [self.__to_lc,self.__to_item]

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
    def __init__(self, id, name, instance, desc=None, input_exchange_items=[], output_exchange_items=[], params=None):
        """
        Defines a linkable model that can be loaded into a configuration
        Args:
            id: unique id for the model (type: string)
            name: name of the model (type: string)
            instance: instantiated model object
            desc: description of the model (type: string)
            input_exchange_items: list of input exchange items (type: list[stdlib.ExchangeItem] )
            output_exchange_items: list of output exchange items (type: list[stdlib.ExchangeItem] )
            params: model loading parameters (e.g. *.mdl params) (type: list[ dict{  )

        Returns: Model

        """
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

    def type(self):
        """
        Gets the type of model
        Returns: wrappers.Types

        """
        return self.instance().type()

    def attrib(self, value=None):
        """
        Provides a method for storing model specific attributes
        """
        if value is not None:
            self.__attrib = value
        return self.__attrib

    def get_input_exchange_items(self):
        """
        Gets model input exchange items
        Returns: list of exchange item objects (type: list[stdlib.ExchangeItem])

        """
        if len(self.__iei.keys()) > 0:
            return [j for i,j in self.__iei.items()]
        else: return []

    def get_output_exchange_items(self):
        """
        Gets model output exchange items
        Returns: list of exchange item objects (type: list[stdlib.ExchangeItem])

        """
        if len(self.__oei.keys()) > 0:
            return [j for i,j in self.__oei.items()]
        else: return []

    def get_input_exchange_item_by_name(self,value):
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

    def get_output_exchange_item_by_name(self,value):
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
            elog.error('Could not find Output Exchange Item: '+value)
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

        # TODO: Get this from gui dialog
        self.preferences = os.path.abspath(os.path.join(os.path.dirname(__file__),'../data/preferences'))

    def clear_all(self):
        """
        Clears all the model and link objects from the controller

        Returns: True
        """
    
        self.__links = {}
        self.__models = {}
        return True

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

    def add_db_connection(self,value):
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

        Returns: dictionary of database connection information (type:dict)

        """
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
        """
        Gets database arguments for a specific database name

        Args:
            db_name: name of the database to retrieve arguments for

        Returns: dictionary of database arguments or None (type:dict or type:None)

        """
        # return the database args dictionary for a given name
        db = {}
        for db_id in self._db.iterkeys():
            database = self._db[db_id]
            if database['name'] == db_name:
                return database['args']
        return None

    def set_default_database(self,db_id=None):
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
                sPrint('Default database : %s'%self._db[db_id]['connection_string'], MessageType.INFO)
            except Exception, e :
                msg = 'Encountered and error when setting default database: %s' % e
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

    def add_model(self, id=None, attrib=None):
        """
        Adds a model to the Coordinator

        Args:
            id: id that will be assigned to the model
            attrib: model load parameters (see *.mdl)

        Returns: dictionary of model id, name, and type or None (type:dict or type:None)

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

            # Comment these four lines to run a .mdl file instead of json
            json_path = ini_path[:-4] + ".json"
            data = parse_json(json_path)
            ini_path = json_path
            params = data

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
        """
        Removes a model from the Coordinator by id

        Args:
            id: id of the model to remove (type:string)

        Returns: the id of the model that was removed or None (type:string or None)

        """
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

    def get_model_by_id_summary(self,id):
        """
        Gets a summarized version of the model by id

        Args:
            id: id of the model to return (type:string)

        Returns: dictionary of summarized metadata (type:dict)

        """
        """
        finds the model that corresponds with the given id and return a summary of its metadata
        :param id: model id
        :return: serializable summary of the model's metadata
        """

        for m in self.__models:
            if self.__models[m].id() == id:
                return {'params': self.__models[m].get_config_params(),
                        'name': self.__models[m].name(),
                        'id': self.__models[m].id(),
                        'description': self.__models[m].description(),
                        'type': self.__models[m].type(),
                        'attrib': self.__models[m].attrib(),
                        }
        return None

    def get_model_by_id(self,id):
        """
        Gets a model within the Coordinator by id

        Args:
            id: id of the model to return (type:string)

        Returns: model or None (type:engine.Model or None)

        """
        for m in self.__models:
            if self.__models[m].id() == id:
                return self.__models[m]
        return None

    def add_link(self,from_id, from_item_id, to_id, to_item_id, spatial_interp=None, temporal_interp=None, uid=None):
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
        Creates a new link in the Coordinator

        Args:
            from_id: id of the source model (type:string)
            from_item_name: name of the source exchange item (type:string)
            to_id: id of the target model (type:string)
            to_item_name: name of the target exchange item (type:string)

        Returns: the link object that is created or None (type:engine.Link or None)

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
            id = 'L'+uuid.uuid4().hex[:5]

            # create link
            link = Link(id,From,To,oi,ii)
            self.__links[id] = link

            return link
        else:
            elog.warning('Could Not Create Link :(')
            return None

    def get_from_links_by_model(self, model_id):
        """
        Gets links corresponding to a specific model id in which the model is the source component. This is useful for determining where data will pass (direction)

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

        Returns: dictionary of summarized link information (type:dict)

        """
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
        """
        Gets all the models that have been loaded into the Coordinator

        Returns: dictionary of summarized models that have been loaded (type:dict)

        """
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
        """
        Summarizes exchange item information into a serializable object

        Args:
            item: the exchange item to summarize (type:stdlib.ExchangeItem)
            returnGeoms: indicate if geometries should be returned (type:bool)

        Returns: summarized exchange item (type:dict)

        """

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

    def remove_link_by_id(self,id):
        """
        Removes a link using the link id
        Args:
            id: id of the link to remove

        Returns: 1 if successful, otherwise 0

        """
        if id in self.__links:
            self.__links.pop(id,None)
            return 1
        return 0

    def get_links_btwn_models(self, from_model_id, to_model_id):
        """
        Gets all information related to a link between the specified models
        Args:
            from_model_id: id of the source model (type:string)
            to_model_id: id of the target model (type:string)

        Returns: list of link dictionary objects (one for each exchange item on the link)

        """

        links = []
        link_dict = {}
        for linkid, link in self.__links.iteritems():
            source_id = link.source_component().id()
            target_id = link.target_component().id()
            if source_id == from_model_id and target_id == to_model_id:
                # links.append(link)
                spatial = link.spatial_interpolation().name() \
                    if link.spatial_interpolation() is not None \
                    else 'None'
                temporal = link.temporal_interpolation().name() \
                    if link.temporal_interpolation() is not None \
                    else 'None'
                link_dict = dict(id=link.get_id(),
                                 source_id=source_id,
                                 target_id=target_id,
                                 source_name=link.source_component().name(),
                                 target_name=link.target_component().name(),
                                 source_item=link.source_exchange_item().name(),
                                 target_item=link.target_exchange_item().name(),
                                 spatial_interpolation=spatial,
                                 temporal_interpolation=temporal)
                links.append(link_dict)

        return links

    def get_exchange_item_info(self, modelid, exchange_item_type=stdlib.ExchangeItemType.INPUT, returnGeoms=True):
        """
        Gets all information related to input or output exchange items for a specific model
        Args:
            modelid: id of the model for which the exchange item will be retrieved (type:string)
            exchange_item_type: the type of exchange item to retrieve (type: stdlib.ExchangeItemType)
            returnGeoms: indicate if geometries should be returned (type: bool)

        Returns: list of exchange items in a serializable format 

        """

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

        link = self.__links[link_id]
        t_item = link.target_exchange_item()

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
        Updates the model associated with the link.  This is necessary after the run phase to update the data values stored on the link object
        Args:
            model: model object that will be updated (type:engine.Model)
            exchangeitems: list of exchange item to be updated (type:stdlib.ExchangeItem)

        Returns: None

        """

        name = model.name()
        for id,link_inst in self.__links.iteritems():
            f,t = link_inst.get_link()

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
        Executes a model simulation.

        Args:
            simulationName: Name of the simulation
            dbName: name of the database to save results
            user_info: user's information 
            datasets: datasets to save

        Returns: None

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



    def connect_to_db(self, title, desc, engine, address, dbname, user, pwd, default=False):
        """
        Establishes a connection with a database for saving simulation results

        Args:
            title: title to give database (local use only)
            desc: database description
            engine: the engine that should be used to connect to the data base (e.g. postgres)
            address: address of the database
            dbname: name of the database to connect with (server name)
            user: user name, required to establish a connection
            pwd:  password for connecting to the database
            default: designates if this database should be used as the default for saving simulation results

        Returns: returns database id 

        """

        connection = connect_to_db(title, desc, engine, address, dbname, user, pwd)

        if connection:
            dbs = self.add_db_connection(connection)

            if default:
                self.set_default_database(connection.keys()[0])

            return {'success':True, 'ids':connection.keys()}
        else:
            return {'success':False, 'ids':None}

        # TODO: this function only needs to resturn the connection key or None.  It is not necessary to also indicate success or failure as it will be apparent from the returned data.


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
        self._coreread = readCore(self._db[db_id]['session'])

        results = self._coreread.getAllResult()

        if results:
            elog.info('Id   Type     Variable    Unit    ValueCount')
            for result in results:
                elog('%s    %s   %s  %s  %s '%(result.ResultID, result.ResultTypeCV,result.VariableObj.VariableCode,
                                         result.UnitObj.UnitsName,result.ValueCount))
        else:
            elog.info('No results found')

