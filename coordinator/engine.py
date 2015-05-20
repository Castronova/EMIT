__author__ = 'tonycastronova'


#sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../../odm2/src')))


import threading

import networkx as net

from coordinator import help as h
from utilities.gui import *
from utilities.mdl import *
from api.ODM2.Core.services import readCore

# from ODM2.Core.services import readCore
#import wrappers

from transform import space_base
from transform import time_base

from wrappers import odm2_data
from wrappers import feed_forward
from wrappers import time_step


import datatypes

import run
import inspect
# import coordinator.engineProcessor as engineProcessor
from api.ODM2.Core.services import *
from copy import deepcopy

"""
Purpose: This file contains the logic used to run coupled model simulations
"""

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
        print 'ERROR |[Deprecated] This function has been deprecated...do not use! '
        print 'ERROR | [Deprecated] main.py -> get_link()'
        for caller in inspect.stack():
            if 'EMIT' in caller[1]:
                print 'ERROR | [Deprecated Call Stack] ',caller[1],caller[3],caller[2]

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
        self.__name = name
        self.__description = desc
        self.__iei = {}
        self.__oei = {}
        self.__id = id
        self.__params = params
        self.__type = None
        self.__attrib  = {}

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance
        self.__params_path = None

    def type(self,value=None):
        # if value is not None:
        #     self.__type = value
        # return self.__type
        return self.get_instance().type()

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

    def get_input_exchange_item(self,value):
        ii = None

        for k,v in self.__iei.iteritems():
            if v.get_id() == value:
                ii = self.__iei[k]

        if ii is None:
            print 'ERROR | Could not find Input Exchange Item: '+value

        return ii

    def get_output_exchange_item(self,value):
        oi = None

        for k,v in self.__oei.iteritems():
            if v.get_id() == value:
                oi = self.__oei[k]

        if oi is None:
            print 'ERROR | Could not find Output Exchange Item: '+value

        return oi


    def get_input_exchange_item_by_name(self,value):
        ii = None

        for k,v in self.__iei.iteritems():
            if v.name() == value:
                ii = self.__iei[k]

        if ii is None:
            print 'ERROR |Could not find Input Exchange Item: '+value

        return ii

    def get_output_exchange_item_by_name(self,value):
        oi = None

        for k,v in self.__oei.iteritems():
            if v.name() == value:
                oi = self.__oei[k]

        if oi is None:
            print 'ERROR | Could not find Output Exchange Item: '+value

        return oi

    def get_description(self):
        return self.__description
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id

    def get_instance(self):
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
        self.__incr = 0
        self._db = {}
        self.__default_db = None
        self._dbresults = {}


        # TODO: Get this from gui dialog
        self.preferences = os.path.abspath(os.path.join(os.path.dirname(__file__),'../data/preferences'))


        # initialize multiprocessing classes
        # self.processes = engineProcessor.TaskServer()

    def clear_all(self):
        self.__links = {}
        self.__models = {}
        return True

    def DbResults(self,key=None, value = None):
        if key is not None:
            if key not in self._dbresults.keys():
                self._dbresults[key] = value
        return self._dbresults

    def Models(self, model=None):
        if model is not None:
            self.__models[model.get_name()] = model
        return self.__models

    def Links(self, link=None):
        return self.__links

    def set_db_connections(self,value={}):
        self._db = value
        return self._db

    def add_db_connection(self,value):

        self._db.update(value)
        return self._db

    def get_db_connections(self):
        # return the database connection dictionary without sqlalchemy objects
        db = {}
        for db_id in self._db.iterkeys():
            db[db_id] = {'name': self._db[db_id]['name'],
                         'description': self._db[db_id]['description'],
                         'connection_string': self._db[db_id]['connection_string'],
                         'id': db_id}
        return db

    def set_default_database(self,db_id=None):

        # set it to the first postgres db
        if db_id is None:
            db_id = 'Any PostGreSQL Database'
            for id,d in self._db.iteritems():
                if d['args']['engine'] == 'postgresql':
                    db_id = id
                    break

        try:
            self.__default_db = self._db[db_id]
            self.__default_db['id'] = db_id
            print 'Default database : %s'%self._db[db_id]['connection_string']
        except:
            print 'ERROR | could not find database: %s'%db_id

    def get_new_id(self):
        self.__incr += 1
        return self.__incr

    def get_default_db(self):
        if self.__default_db is None:
            return None
        else:
            db = {'name': self.__default_db['name'],
                  'description': self.__default_db['description'],
                  'connection_string': self.__default_db['connection_string'],
                  'id': self.__default_db['id']}
            return db

    def add_model(self, id=None, attrib=None):
        """
        stores model component objects when added to a configuration
        """
        thisModel = None

        if 'mdl' in attrib:
        # if type == datatypes.ModelTypes.FeedForward or type == datatypes.ModelTypes.TimeStep:

            ini_path = attrib['mdl']

            # parse the model configuration parameters
            params = parse_config(ini_path)

            if params is not None:
                # load model
                name, model_inst = load_model(params)

                # make sure this model doesnt already exist
                if name in self.__models:
                    print 'WARNING | Model named '+name+' already exists in configuration'
                    return None

                iei = model_inst.inputs().values()
                oei = model_inst.outputs().values()

                # generate a unique model id
                if id is None:
                    id = uuid.uuid4().hex[:5]

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

        elif 'databaseid' in attrib and 'resultid' in attrib:
        # elif type == datatypes.ModelTypes.Data:

            databaseid = attrib['databaseid']
            resultid = attrib['resultid']

            # get the database session
            session = self._db[databaseid]['session']

            # create odm2 datamodel instance
            inst = odm2_data.odm2(resultid=resultid, session=session)

            oei = inst.outputs().values()

            if id is None:
                id = uuid.uuid4().hex[:5]

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


        # set type and attribute params
        # thisModel.type(type)
        # thisModel.attrib(attrib)


        # save the model
        self.__models[thisModel.get_name()] = thisModel

        # return the model id
        # return thisModel
        return {'id':thisModel.get_id(), 'name':thisModel.get_name(),'model_type':thisModel.type()}

    def remove_model(self,linkablecomponent):
        """
        removes model component objects from the registry
        """

        if linkablecomponent in self.__models:
            # remove the model
            self.__models.pop(linkablecomponent,None)

            #todo: remove all associated links

    def remove_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].get_id() == id:

                # remove the model
                self.__models.pop(m,None)

                # find all links associated with the model
                remove_these_links  = []
                for l in self.__links:
                    FROM, TO = self.__links[l].get_link()
                    if FROM[0].get_id() == id or TO[0].get_id() == id:
                        remove_these_links.append(l)

                # remove all links associated with the model
                for link in remove_these_links:
                    self.__links.pop(link,None)

                return 1
        return 0

    def get_model_by_id_summary(self,id):
        """
        finds the model that corresponds with the given id and return a summary of its metadata
        :param id: model id
        :return: serializable summary of the model's metadata
        """

        for m in self.__models:
            if self.__models[m].get_id() == id:
                return {'params': self.__models[m].get_config_params(),
                        'name': self.__models[m].get_name(),
                        'id': self.__models[m].get_id(),
                        'description': self.__models[m].get_description(),
                        'type': self.__models[m].type(),
                        'attrib': self.__models[m].attrib(),
                        }
        return None

    def get_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].get_id() == id:
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
            print e
            return None

        # check that input and output exchange items exist
        ii = To.get_input_exchange_item_by_name(to_item_id)
        oi = From.get_output_exchange_item_by_name(from_item_id)

        if ii is not None and oi is not None:
            # generate a unique model id
            if uid is None:
                id = 'L'+uuid.uuid4().hex[:5]
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
            print 'WARNING | Could Not Create Link :('
            return None

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
            print e
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
            print 'WARNING | Could Not Create Link :('

    def get_from_links_by_model(self, model_id):

        """
        returns only the links where the corresponding linkable component is the FROM item.
        This is useful for determining where data will pass (direction)
        """

        links = {}
        for linkid, link in self.__links.iteritems():
            # get the from/to link info

            if link.source_component().get_id() == model_id:
                links[linkid] = link

        return links

    def get_links_by_model(self,model_id):
        """
        returns all the links corresponding with a linkable component
        """
        links = {}
        for linkid, link in self.__links.iteritems():
            links[linkid] = link


        if len(links) == 0:
            print 'ERROR |  Could not find any links associated with model id: '+str(model_id)

        # todo: this should return a dict of link objects, NOT some random list

        return links

    def get_links_btwn_models(self, from_model_id, to_model_id):

        links = []
        link_dict = {}
        for linkid, link in self.__links.iteritems():
            source_id = link.source_component().get_id()
            target_id = link.target_component().get_id()
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
                                 source_name=link.source_component().get_name(),
                                 target_name=link.target_component().get_name(),
                                 source_item=link.source_exchange_item().name(),
                                 target_item=link.target_exchange_item().name(),
                                 spatial_interpolation=spatial,
                                 temporal_interpolation=temporal)
                links.append(link_dict)
                # return link_dict

        return links

    def get_link_by_id(self,id):
        """
        returns all the links corresponding with a linkable component
        """
        for l in self.__links:
            if l == id:
                return self.__links[l]
        return None

    def get_link_by_id_summary(self,id):
        """
        returns all the links corresponding with a linkable component
        """
        for l in self.__links.iterkeys():
            if l == id:
                spatial = self.__links[l].spatial_interpolation().name() \
                    if self.__links[l].spatial_interpolation() is not None \
                    else 'None'
                temporal = self.__links[l].temporal_interpolation().name() \
                    if self.__links[l].temporal_interpolation() is not None \
                    else 'None'
                return dict(
                        output_name=self.__links[l].source_exchange_item().name(),
                        output_id=self.__links[l].source_exchange_item().get_id(),
                        input_name=self.__links[l].target_exchange_item().name(),
                        input_id=self.__links[l].target_exchange_item().get_id(),
                        spatial_interpolation=spatial,
                        temporal_interpolation=temporal,
                        source_component_name=self.__links[l].source_component().get_name(),
                        target_component_name=self.__links[l].target_component().get_name(),
                        source_component_id=self.__links[l].source_component().get_id(),
                        target_component_id=self.__links[l].target_component().get_id(),)
        return None

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
                        output_name=self.__links[l].source_exchange_item().name(),
                        output_id=self.__links[l].source_exchange_item().get_id(),
                        input_name=self.__links[l].target_exchange_item().name(),
                        input_id=self.__links[l].target_exchange_item().get_id(),
                        spatial_interpolation=spatial,
                        temporal_interpolation=temporal,
                        source_component_name=self.__links[l].source_component().get_name(),
                        target_component_name=self.__links[l].target_component().get_name(),
                        source_component_id=self.__links[l].source_component().get_id(),
                        target_component_id=self.__links[l].target_component().get_id(),
                            ))
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
                        output_name=self.__links[l].source_exchange_item().name(),
                        output_id=self.__links[l].source_exchange_item().get_id(),
                        input_name=self.__links[l].target_exchange_item().name(),
                        input_id=self.__links[l].target_exchange_item().get_id(),
                        spatial_interpolation=spatial,
                        temporal_interpolation=temporal,
                        source_component_name=self.__links[l].source_component().get_name(),
                        target_component_name=self.__links[l].target_component().get_name(),
                        source_component_id=self.__links[l].source_component().get_id(),
                        target_component_id=self.__links[l].target_component().get_id(),
                            ))
        return links

    def get_all_models(self):
        models = []
        for m in self.__models:

            models.append(
                {'params': self.__models[m].get_config_params(),
                    'name': self.__models[m].get_name(),
                    'id': self.__models[m].get_id(),
                    'description': self.__models[m].get_description(),
                    'type': self.__models[m].type(),
                    'attrib': self.__models[m].attrib(),
                    }
            )
        return models



    def get_output_exchange_items_summary(self, id):
        """
        gets a serializable version of the output exchange items
        :param id: model id
        :return: dictionary of serializable objects
        """
        for m in self.__models:
            if self.__models[m].get_id() == id:
                eitems = self.__models[m].get_output_exchange_items()
                items_list = []
                for ei in eitems:
                    geoms = [ dict(shape=g.geom(),srs_proj4=g.srs().ExportToProj4(),z=g.elev(),id=g.id()) for g in ei.geometries()]
                    items_list.append(dict(name=ei.name(), description=ei.description(), id=ei.get_id(), unit=ei.unit(),
                                           variable=ei.variable(),type=ei.get_type(),geom=geoms))
                return items_list
        return None

    def get_input_exchange_items_summary(self, id):
        """
        gets a serializable version of the input exchange items
        :param id: model id
        :return: dictionary of serializable objects
        """
        for m in self.__models:
            if self.__models[m].get_id() == id:
                eitems = self.__models[m].get_input_exchange_items()
                items_list = []
                for ei in eitems:
                    geoms = [ dict(shape=g.geom(),srs_proj4=g.srs().ExportToProj4(),z=g.elev(),id=g.id()) for g in ei.geometries()]
                    items_list.append(dict(name=ei.name(), description=ei.description(), id=ei.get_id(), unit=ei.unit(),
                                           variable=ei.variable(),type=ei.get_type(),geom=geoms))
                return items_list
        return None

    def remove_link_by_id(self,id):
        """
        removes a link using the link id
        """
        if id in self.__links:
            self.__links.pop(id,None)
            return 1
        return 0

        # for l in self.__links:
        #     if self.__links[l].get_id() == id:
        #         self.__links.pop(l,None)
        #         return 1
        # return 0

    def remove_link_all(self):
        """
        removes the last link
        """
        removelinks = self.__links = {}

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
        f_geoms = f_item.geometries()
        for t_geom in t_item.geometries():

            # get this list index of the to-geom
            mapped = next((g for g in from_to_spatial_map if g[1] == t_geom), 0)

            # if mapping was found
            if mapped:

                f_geom ,t_geom= mapped

                # update the datavalues with the mapped dates and values
                t_geom.datavalues().set_timeseries(from_geom_dict[f_geom])

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

            if t[0].get_name() == name:
                for item in exchangeitems:
                    if t[1].name() == item.name():
                        self.__links[id] = Link(id, f[0], t[0], f[1], item)
                        #t[1] = item

            elif f[0].get_name() == name:
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

        # add models as graph nodes
        #for name,model in self.__models.iteritems():
        #    g.add_node(model.get_id())

        # create links between these nodes
        for id, link in self.__links.iteritems():

            # replaced with the two lines below b/c get_link has been deprecated
            #f, t = link.get_link()
            #from_node = f[0].get_id()
            #to_node = t[0].get_id()

            from_node = link.source_component().get_id()
            to_node = link.target_component().get_id()


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
                order = [self.__models.values()[0].get_id()]

        # return execution order
        return order

    def transfer_data(self, link):
        """
        retrieves data exchange item from one component and passes it to the next
        """
        pass

    def get_global_start_end_times(self,linkablecomponents=[]):
        """
        determines the simulation start and end times from the linkablecomponent attributes
        """
        pass

    def run_simulation(self):
        """
        coordinates the simulation effort
        """

        try:
            # determine if the simulation is feed-forward or time-step
            models = self.Models()
            types = []
            for model in models.itervalues() :
                types.extend(inspect.getmro(model.get_instance().__class__))

            # make sure that feed forward and time-step models are not mixed together
            if (feed_forward.feed_forward_wrapper in types) and (time_step.time_step_wrapper in types):
                return dict(success=False, message='Cannot mix feed-forward and time-step models')

            else:
                # threadManager = ThreadManager()
                if feed_forward.feed_forward_wrapper in types:
                    t = threading.Thread(target=run.run_feed_forward, args=(self,))
                    t.start()
                    # run.run_feed_forward(self)
                elif time_step.time_step_wrapper in types:

                    t = threading.Thread(target=run.run_time_step, args=(self,))
                    t.start()
                    #run.run_time_step(self)

            return dict(success=True, message='')

        except Exception as e:
            return dict(success=False, message=e)
            # raise Exception(e.args[0])

    def get_configuration_details(self,arg):

        if len(self.__models.keys()) == 0:
            print 'WARNING | no models found in configuration.'

        if arg.strip() == 'summary':
            print '\n   Here is everything I know about the current simulation...\n'

        # print model info
        if arg.strip() == 'models' or arg.strip() == 'summary':

            # loop through all known models
            for name,model in self.__models.iteritems():
                model_output = []
                model_output.append('Model: '+name)
                model_output.append('desc: ' + model.get_description())
                model_output.append('id: '+ model.get_id())

                # print exchange items
                #print '  '+(27+len(name))*'-'
                #print '  |' + ((33-len(name))/2)*' ' +'Model: '+name + ((33-len(name))/2)*' '+'|'
                #print '  '+(27+len(name))*'-'

                #print '   * desc: ' + model.get_description()
                #print '   * id : '+ model.get_id()
                #print '  '+(27+len(name))*'-'

                for item in model.get_input_exchange_items() + model.get_output_exchange_items():
                    # print '   '+item.get_type().upper()
                    # print '   * id: '+str(item.get_id())
                    # print '   * name: '+item.name()
                    # print '   * description: '+item.description()
                    # print '   * unit: '+item.unit().UnitName()
                    # print '   * variable: '+item.variable().VariableNameCV()
                    # print '  '+(27+len(name))*'-'
                    model_output.append( str(item.get_id()))
                    model_output.append( 'name: '+item.name())
                    model_output.append( 'description: '+item.description())
                    model_output.append( 'unit: '+item.unit().UnitName())
                    model_output.append( 'variable: '+item.variable().VariableNameCV())
                    model_output.append( ' ')

                # get formatted width
                w = self.get_format_width(model_output)

                # print model info
                print '  |'+(w)*'-'+'|'
                print '  *'+self.format_text(model_output[0], w,'center')+'*'
                print '  |'+(w)*'='+'|'
                print '  |'+self.format_text(model_output[1], w,'left')+'|'
                print '  |'+self.format_text(model_output[2], w,'left')+'|'
                print '  |'+(w)*'-'+'|'
                for l in model_output[3:]: print '  |'+self.format_text(l,w,'left')+'|'
                print '  |'+(w)*'-'+'|'
                print ' '

        # print link info
        if arg.strip() == 'links' or arg.strip() == 'summary':
            # string to store link output
            link_output = []
            # longest line in link_output
            maxlen = 0

            for linkid,link in self.__links.iteritems():
                # get the link info
                From, To = link.get_link()

                link_output.append('LINK ID : ' + linkid)
                link_output.append('from: '+From[0].get_name()+' -- output --> '+From[1].name())
                link_output.append('to: '+To[0].get_name()+' -- input --> '+To[1].name())

                # get the formatted width
                w = self.get_format_width(link_output)

                # pad the width and make sure that it is divisible by 2
                #w += 4 if w % 2 == 0 else 5

                # print the output
                print '  |'+(w)*'-'+'|'
                print '  *'+self.format_text(link_output[0], w,'center')+'*'
                print '  |'+(w)*'='+'|'
                for l in link_output[1:]: print '  |'+self.format_text(l,w,'left')+'|'
                print '  |'+(w)*'-'+'|'

        # print database info
        if arg.strip() == 'db' or arg.strip() == 'summary':

            for id,db_dict in self._db.iteritems():

                # string to store db output
                db_output = []
                # longest line in db_output
                maxlen = 0

                # get the session args
                name = db_dict['name']
                desc = db_dict['description']
                engine = db_dict['args']['engine']
                address = db_dict['args']['address']
                user = db_dict['args']['user']
                pwd = db_dict['args']['pwd']
                db = db_dict['args']['db']


                db_output.append('DATABASE : ' + id)
                db_output.append('name: '+name)
                db_output.append('description: '+desc)
                db_output.append('engine: '+engine)
                db_output.append('address: '+address)
                db_output.append('database: '+db)
                db_output.append('user: '+user)
                db_output.append('connection string: '+db_dict['args']['connection_string'])

                # get the formatted width
                w = self.get_format_width(db_output)

                # print the output
                print '  |'+(w)*'-'+'|'
                print '  *'+self.format_text(db_output[0], w,'center')+'*'
                print '  |'+(w)*'='+'|'
                for l in db_output[1:]: print '  |'+self.format_text(l,w,'left')+'|'
                print '  |'+(w)*'-'+'|'

    def discover_timeseries(self,db_connection_name):

        # if db_connection_name not in self._db:
        #     print '> [error] could not find database named %s'%db_connection_name
        #     return 0
        # else:
        #     # get the database session
        #     session = self._db[db_connection_name]['sesssion']
        #
        #     # get all timeseries using db api
        #     from odm2.api.ODM2.Results.services import read
        #     result_query = read.read(self._db[db_connection_name]['args']['connection_string'])
        #     ts = result_query.getAllTimeSeriesResults()

            print 'test'

    def connect_to_db(self, title, desc, engine, address, name, user, pwd):

        connection = connect_to_db(title, desc, engine, address, name, user, pwd)

        if connection:
            self.add_db_connection(connection)
            return {'success':True}
        else:
            return {'success':False}


    def connect_to_db_from_file(self,filepath=None):

        if filepath is None: return {'success':False}

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

                return {'success':True}
            except Exception,e:
                print e
                print 'ERROR | Could not create connections from file '+filepath
                return {'success':False}

        else:
            return {'success':False}

    def get_format_width(self,output_array):
        width = 0
        for line in output_array:
            if len(line) > width: width = len(line)
        return width + 4

    def format_text(self,text,width,option='right'):

        if option == 'center':
            # determine the useable padding
            padding = width - len(text)
            lpadding = padding/2
            rpadding = padding - lpadding

            # center the text
            return lpadding*' '+text+rpadding*' '

        elif option == 'left':
            # determine the useable padding
            padding = width - len(text)

            # center the text
            return text+padding*' '

        elif option == 'right':
            # determine the useable padding
            padding = width - len(text)

            # center the text
            return padding*' ' + text

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

        else: print 'ERROR | Could not find path %s'%simulation_file

    def show_db_results(self, args):

        # get database id
        db_id = args[0]

        if db_id not in self._db:
            print 'ERROR | could not find database id: %s'%db_id
            return


        # get all result entries
        self._coreread = readCore(self._db[db_id]['session'])

        results = self._coreread.getAllResult()

        if results:
            print 'Id   Type     Variable    Unit    ValueCount'
            for result in results:
                print '%s    %s   %s  %s  %s '%(result.ResultID, result.ResultTypeCV,result.VariableObj.VariableCode,
                                         result.UnitObj.UnitsName,result.ValueCount)
        else:
            print 'No results found'

    def parse_args(self, arg):

        if ''.join(arg).strip() != '':
            if arg[0] == 'help':
                if len(arg) == 1: print h.help()
                else: print h.help_function(arg[1])

            elif arg[0] == 'add' :
                if len(arg) == 1: print h.help_function('add')
                else: self.add_model(arg[1])

            elif arg[0] == 'remove':
                if len(arg) == 1: print h.help_function('remove')
                else: self.remove_model_by_id(arg[1])

            elif arg[0] == 'link':
                if len(arg) != 5: print h.help_function('link')
                else: self.add_link(arg[1],arg[2],arg[3],arg[4])

            elif arg[0] == 'showme':
                if len(arg) == 1: print h.help_function('showme')
                else: self.get_configuration_details(arg[1])

            elif arg[0] == 'connect_db':
                if len(arg) == 1: print h.help_function('connect_db')
                else: self.connect_to_db(arg[1:])

            elif arg[0] == 'default_db':
                if len(arg) == 1: print h.help_function('default_db')
                else: self.set_default_db(arg[1:])

            elif arg[0] == 'run':
                print 'Running Simulation in Feed Forward Mode'
                self.run_simulation()

            elif arg[0] == 'load':
                if len(arg) == 1: print h.help_function('load')
                else: self.load_simulation(arg[1:])

            elif arg[0] == 'db':
                if len(arg) == 1: print h.help_function('db')
                else: self.show_db_results(arg[1:])



            #todo: show database time series that are available

            elif arg[0] == 'info': print h.info()

            else:
                print 'ERROR | command not recognized.  Type "help" for a complete list of commands.'

def main(argv):
    print '|-------------------------------------------------|'
    print '|      Welcome to the Utah State University       |'
    print '| Environmental Model InTegration (EMIT) Project! |'
    print '|-------------------------------------------------|'
    print '\nPlease enter a command or type "help" for a list of commands'

    arg = None

    # create instance of coordinator
    coordinator = Coordinator()


    # TODO: This should be handled by gui
    # connect to databases
    coordinator.connect_to_db(['../data/connections'])
    coordinator.set_default_database()

    while arg != 'exit':
        # get the users command
        arg = raw_input("> ").split(' ')
        coordinator.parse_args(arg)

if __name__ == '__main__':
    main(sys.argv[1:])