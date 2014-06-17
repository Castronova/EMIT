__author__ = 'tonycastronova'

import sys, getopt
from coordinator import help as h
from utilities import *
import math
import networkx as net
from odm2.api.ODM2.Simulation.services import read as simulation_read
from odm2.api.ODM2.Simulation.services import write as simulation_write

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
    def __init__(self, id, name, instance, desc=None, input_exchange_items={}, output_exchange_items={}):
        self.__name = name
        self.__description = desc
        self.__iei = {}
        self.__oei = {}
        self.__id = id

        for iei in input_exchange_items:
            self.__iei[iei.name()] = iei

        for oei in output_exchange_items:
            self.__oei[oei.name()] = oei

        self.__inst = instance

    def get_input_exchange_items(self):
        return [j for i,j in self.__iei.items()]
    def get_output_exchange_items(self):
        return [j for i,j in self.__oei.items()]

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

    def get_description(self):
        return self.__description
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id

    def get_instance(self):
        return self.__inst

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

    def get_new_id(self):
        self.__incr += 1
        return self.__incr

    def get_default_db(self):
        return self.__default_db

    def add_model(self, ini_path):
        """
        stores model component objects when added to a configuration
        """

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
            ei = build_exchange_items(params)

            # organize input and output items
            iei = [item for item in ei if item.get_type() == 'input']
            oei = [item for item in ei if item.get_type() == 'output']

            # generate a unique model id
            id = 'M'+str(self.get_new_id())

            # create a model instance
            thisModel = Model(id,name,
                              model_inst,
                              params['general'][0]['description'],
                              iei,
                              oei)

            # save the model
            self.__models[name] = thisModel

            # return the model id
            return id

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

    def add_link(self,from_id, from_item_name, to_id, to_item_name):
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
        ii = To.get_input_exchange_item(to_item_name)
        oi = From.get_output_exchange_item(from_item_name)

        if ii is not None and oi is not None:
            # generate a unique model id
            id = 'L'+str(self.get_new_id())

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
        reader = simulation_read.read(self.get_default_db())
        writer = simulation_write.write(self.get_default_db())


        # todo: determine unresolved exchange items (utilities)

        # determine execution order
        exec_order = self.determine_execution_order()

        # loop through models and execute run
        for modelid in exec_order:

            # get the current model instance
            model = self.get_model_by_id(modelid)

            #  retrieve inputs from database
            input_data =  get_ts_from_link(self.__default_db,self.__links,model)

            # pass these inputs ts to the models' run function
            model.get_instance().run(input_data)

            # save these results
            save_these_series = model.get_instance().save()

            #  set these input data as exchange items in stdlib or wrapper class
            writer.insertSimulation()

            # save exchange items in database
            writer.insertData(save_these_series)


        #   save output (model.save)

        pass

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

            for name,db_dict in self._db.iteritems():

                # string to store db output
                db_output = []
                # longest line in db_output
                maxlen = 0

                # get the session args
                desc = db_dict['description']
                engine = db_dict['args']['engine']
                address = db_dict['args']['address']
                user = db_dict['args']['user']
                pwd = db_dict['args']['pwd']
                db = db_dict['args']['db']


                db_output.append('DATABASE : ' + name)
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

    def get_db_connections(self):
        return self._db

    def connect_to_db(self,in_args):

        # remove any empty list objects
        args = [in_arg for in_arg in in_args if in_arg != '']

        # parse from file
        if len(args) == 1:
            basedir = args[0]
            abspath = os.path.abspath(os.path.join(basedir,args[0]))
            filename = os.path.basename(abspath)
            if os.path.isfile(abspath):
                try:
                    connections = create_database_connections_from_file(args[0])
                    self._db = connections
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

    def set_default_database(self,db_name):
        try:
            self.__default_db = self._db[db_name]['session']
        except:
            print '> [error] could not find database: %s'%db_name


def main(argv):
    print '|-------------------------------------------------|'
    print '|      Welcome to the Utah State University       |'
    print '| Environmental Model InTegration (EMIT) Project! |'
    print '|-------------------------------------------------|'
    print '\nPlease enter a command or type "help" for a list of commands'

    arg = None

    # create instance of coordinator
    coordinator = Coordinator()

    while arg != 'exit':

        # get the users command
        arg = raw_input("> ").split(' ')

        if ''.join(arg).strip() != '':
            if arg[0] == 'help':
                if len(arg) == 1: print h.help()
                else: print h.help_function(arg[1])

            elif arg[0] == 'add' :
                if len(arg) == 1: print h.help_function('add')
                else: coordinator.add_model(arg[1])

            elif arg[0] == 'remove':
                if len(arg) == 1: print h.help_function('remove')
                else: coordinator.remove_model_by_id(arg[1])

            elif arg[0] == 'link':
                if len(arg) != 5: print h.help_function('link')
                else: coordinator.add_link(arg[1],arg[2],arg[3],arg[4])

            elif arg[0] == 'showme':
                if len(arg) == 1: print h.help_function('showme')
                else: coordinator.get_configuration_details(arg[1])

            elif arg[0] == 'connect_db':
                if len(arg) == 1: print h.help_function('connect_db')
                else: coordinator.connect_to_db(arg[1:])

            elif arg[0] == 'default_db':
                if len(arg) == 1: print h.help_function('default_db')
                else: coordinator.set_default_db(arg[1:])

            #todo: show database time series that are available

            elif arg[0] == 'info': print h.info()

            else:
                print '> [error] command not recognized.  Type "help" for a complete list of commands.'


    # try:
    #   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    # except getopt.GetoptError:
    #   print 'test.py -i <inputfile> -o <outputfile>'
    #   sys.exit(2)
    # for opt, arg in opts:
    #   if opt == '-h':
    #      print 'test.py -i <inputfile> -o <outputfile>'
    #      sys.exit()
    #   elif opt in ("-i", "--ifile"):
    #      inputfile = arg
    #   elif opt in ("-o", "--ofile"):
    #      outputfile = arg
    # print 'Input file is "', inputfile
    # print 'Output file is "', outputfile

if __name__ == '__main__':
    main(sys.argv[1:])