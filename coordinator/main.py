__author__ = 'tonycastronova'


import os
import sys

#sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../../odm2/src')))


import sys, getopt
from coordinator import help as h
from utilities.gui import *
from utilities.mdl import *

import math
import networkx as net
import threading
from api.ODM2.Simulation.services import readSimulation
from api.ODM2.Simulation.services import createSimulation
from api.ODM2.Core.services import readCore
# from ODM2.Core.services import readCore
from db.dbapi import postgresdb
import wrappers
import time

from wrappers import odm2_data
import datatypes

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

    def get_link(self):
        return [self.__from_lc,self.__from_item], [self.__to_lc,self.__to_item]

    def get_id(self):
        return self.__id

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
        if value is not None:
            self.__type = value
        return self.__type

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
            print '>  Could not find Input Exchange Item: '+value

        return ii

    def get_output_exchange_item(self,value):
        oi = None

        for k,v in self.__oei.iteritems():
            if v.get_id() == value:
                oi = self.__oei[k]

        if oi is None:
            print '>  Could not find Output Exchange Item: '+value

        return oi


    def get_input_exchange_item_by_name(self,value):
        ii = None

        for k,v in self.__iei.iteritems():
            if v.name() == value:
                ii = self.__iei[k]

        if ii is None:
            print '>  Could not find Input Exchange Item: '+value

        return ii

    def get_output_exchange_item_by_name(self,value):
        oi = None

        for k,v in self.__oei.iteritems():
            if v.name() == value:
                oi = self.__oei[k]

        if oi is None:
            print '>  Could not find Output Exchange Item: '+value

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
        
    def clear_all(self):
        self.__links = {}
        self.__models = {}

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
        return self._db

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
            print '> Default database : %s'%self._db[db_id]['connection_string']
        except:
            print '> [error] could not find database: %s'%db_id

    def get_new_id(self):
        self.__incr += 1
        return self.__incr

    def get_default_db(self):
        return self.__default_db

    def add_model(self, type, id=None, attrib=None):
        """
        stores model component objects when added to a configuration
        """
        thisModel = None


        if type == datatypes.ModelTypes.FeedForward:

            ini_path = attrib['mdl']

            # parse the model configuration parameters
            params = parse_config(ini_path)

            if params is not None:
                # load model
                name,model_inst = load_model(params)

                # make sure this model doesnt already exist
                if name in self.__models:
                    print 'Model named '+name+' already exists in configuration'
                    return None

                # build exchange items
                # ei = build_exchange_items_from_config(params)
                #
                # # organize input and output items
                # iei = [item for item in ei if item.get_type() == 'input']
                # oei = [item for item in ei if item.get_type() == 'output']

                iei = model_inst.inputs().values()
                oei = model_inst.outputs().values()

                # generate a unique model id
                if id is None:
                    id = uuid.uuid4().hex[:5]
                #id = 'M'+str(self.get_new_id())

                # create a model instance
                thisModel = Model(id= id,
                                  name=name,
                                  instance=model_inst,
                                  desc=params['general'][0]['description'],    #todo: get this from the feed forward wrapper b/c it may not exist in mdl!!!
                                  input_exchange_items= iei,
                                  output_exchange_items= oei,
                                  params=params)

                thisModel.params_path(ini_path)

        elif type == datatypes.ModelTypes.Data:

            databaseid = attrib['databaseid']
            resultid = attrib['resultid']

            # get the database session
            session = self.get_db_connections()[databaseid]['session']

            # create odm2 datamodel instance
            inst = odm2_data.odm2(resultid=resultid, session=session)

            # create a model instance
            thisModel = Model(id=attrib['id'],
                              name=inst.name(),
                              instance=inst,
                              desc=inst.description(),
                              input_exchange_items= [],
                              output_exchange_items=  [inst.outputs()],
                              params=None)


            # save the result and database ids
            att = {'resultid':resultid}
            att['databaseid'] = databaseid
            thisModel.attrib(att)


        # set type and attribute params
        thisModel.type(type)
        thisModel.attrib(attrib)

        # save the model
        self.__models[thisModel.get_name()] = thisModel

        # return the model id
        return thisModel

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

    def get_model_by_id(self,id):
        for m in self.__models:
            if self.__models[m].get_id() == id:
                return self.__models[m]
        return None

    def add_link(self,from_id, from_item_id, to_id, to_item_id):
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
        ii = To.get_input_exchange_item_by_name(to_item_id)
        oi = From.get_output_exchange_item_by_name(from_item_id)

        if ii is not None and oi is not None:
            # generate a unique model id
            #id = 'L'+str(self.get_new_id())
            id = 'L'+uuid.uuid4().hex[:5]

            # create link
            link = Link(id,From,To,oi,ii)
            self.__links[id] = link

            return id
        else:
            print '>  Could Not Create Link :('

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

            return id
        else:
            print '>  Could Not Create Link :('

    def get_links_by_model(self,model_id):
        """
        returns all the links corresponding with a linkable component
        """
        links = []
        for linkid, link in self.__links.iteritems():
            # get the from/to link info
            From, To = link.get_link()

            if  From[0].get_id() == model_id or To[0].get_id() == model_id:
                links.append([From, To])

        if len(links) == 0:
            print '>  Could not find any links associated with model id: '+str(model_id)

        return links

    def get_links_btwn_models(self, from_model, to_model):

        links = []
        for linkid, link in self.__links.iteritems():
            # get the from/to link info
            From, To = link.get_link()

            if  From[0].get_id() == from_model and To[0].get_id() == to_model:
                #links.append([From, To])
                links.append(link)

        return links

    def get_link_by_id(self,id):
        """
        returns all the links corresponding with a linkable component
        """
        for l in self.__links:
            if l == id:
                return self.__links[l]
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
            f, t = link.get_link()
            from_node = f[0].get_id()
            to_node = t[0].get_id()
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

        # get the read and write database connections

        #reader = readSimulation(self.get_default_db()['connection_string'])
        #writer = createSimulation(self.get_default_db()['connection_string'])


        # store db sessions
        db_sessions = {}



        
        # todo: determine unresolved exchange items (utilities)


        sim_st = time.time()

        activethreads = []

        # determine execution order
        sys.stdout.write('> Determining execution order... ')
        exec_order = self.determine_execution_order()
        sys.stdout.write('done\n')
        for i in range(0, len(exec_order)):
            print '> %d.) %s'%(i+1,self.get_model_by_id(exec_order[i]).get_name())


        # store model db sessions
        for modelid in exec_order:
            session = self.get_model_by_id(modelid).get_instance().session()
            if session is None:
                session = self.get_default_db()['session']

            # todo: this should be stored in the model instance
            # model_obj = self.get_model_by_id(modelid)
            # model_inst = model_obj.get_instance()
            # model_inst.session


            # todo: need to consider other databases too!
            db_sessions[modelid] = postgresdb(session)

        # loop through models and execute run
        for modelid in exec_order:

            # get the database session
            #simulation_dbapi = postgresdb(self.get_default_db()['session'])
            simulation_dbapi = db_sessions[modelid]

            st = time.time()

            # get the current model instance
            model_obj = self.get_model_by_id(modelid)
            model_inst = model_obj.get_instance()

            # set the default session if it hasn't been specified otherwise
            #if model_inst.session() is None:
            #    model_inst.session(self.get_default_db()['session'])

            print '> '
            print '> ------------------'+len(model_inst.name())*'-'
            print '> Executing module: %s ' % model_inst.name()
            print '> ------------------'+len(model_inst.name())*'-'

            #  retrieve inputs from database
            sys.stdout.write('> [1 of 4] Retrieving input data... ')

            # todo: pass db_sessions instead of simulation_dbapi
            input_data =  get_ts_from_link(simulation_dbapi,db_sessions, self._dbresults, self.__links, model_inst)
            sys.stdout.write('done\n')

            sys.stdout.write('> [2 of 4] Performing calculation... ')
            # pass these inputs ts to the models' run function
            model_inst.run(input_data)
            sys.stdout.write('done\n')

            # save these results
            sys.stdout.write('> [3 of 4] Saving calculations to database... ')
            exchangeitems = model_inst.save()


            # only insert data if its not already in a database
            if type(model_inst) != wrappers.odm2_data.odm2:

                #  set these input data as exchange items in stdlib or wrapper class
                simulation = simulation_dbapi.create_simulation(preferences_path=self.preferences,
                                               config_params=model_obj.get_config_params(),
                                               output_exchange_items=exchangeitems,
                                               )

                sys.stdout.write('done\n')

                # store the database action associated with this simulation
                self._dbresults[model_inst.name()] = (simulation.ActionID,model_inst.session(),'action')

            else:
                self._dbresults[model_inst.name()] = (model_inst.resultid(), model_inst.session(), 'result')

            # update links
            sys.stdout.write('> [4 of 4] Updating links... ')
            self.update_links(model_inst,exchangeitems)
            sys.stdout.write('done\n')

            print '> module simulation completed in %3.2f seconds' % (time.time() - st)


        print '> '
        print '> ------------------------------------------'
        print '>           Simulation Summary '
        print '> ------------------------------------------'
        print '> Completed without error :)'
        print '> Simulation duration: %3.2f seconds' % (time.time()-sim_st)
        print '> ------------------------------------------'

    def get_configuration_details(self,arg):

        if len(self.__models.keys()) == 0:
            print '>  [warning] no models found in configuration.'

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

    def connect_to_db(self,in_args):

        # remove any empty list objects
        args = [in_arg for in_arg in in_args if in_arg != '']

        # parse from file
        if len(args) == 1:
            # curdir = os.path.dirname(__file__)
            # abspath = os.path.abspath(os.path.join(curdir, args[0]))
            abspath = os.path.abspath(os.path.join(os.getcwd(),args[0]))
            if os.path.isfile(abspath):
                try:
                    connections = create_database_connections_from_file(args[0])
                    #self.set_default_database()

                    self._db = connections


                    # set the default connection
                    for id,conn in connections.iteritems():
                        if 'default' in conn['args']:
                            if conn['args']['default']:
                                self.set_default_database(db_id=id)
                                break
                    if not self.get_default_db():
                        self.set_default_database()

                    return True
                except Exception,e:
                    print e
                    print '> [error] Could not create connections from file '+args[0]
                    return None

        else:
            pass

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
                            print '> %s'%command
                            self.parse_args(command.split(' '))

                            if 'link' in command:
                                link_objs.append(command.split(' ')[1:])

            # return the models and links created
            return self.__models.values(), self.__links.values(), link_objs

        else: print '> Could not find path %s'%simulation_file

    def show_db_results(self, args):

        # get database id
        db_id = args[0]

        if db_id not in self._db:
            print '> [error] could not find database id: %s'%db_id
            return


        # get all result entries
        from api.odm2.api.ODM2.Core.services import *
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
                print '> Running Simulation in Feed Forward Mode'
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
                print '> [error] command not recognized.  Type "help" for a complete list of commands.'





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