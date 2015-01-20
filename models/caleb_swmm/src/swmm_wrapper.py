__author__ = 'tonycastronova'

from os.path import *
import uuid
import re
from datetime import datetime, timedelta
from ctypes import *


from shapely.geometry import *
from stdlib import Geometry, DataValues, ExchangeItem, ExchangeItemType
from wrappers.time_step import time_step_wrapper
from utilities import mdl, spatial


#import parse_swmm as ps
import geometry as swmm_geom
from structures import *


class swmm(time_step_wrapper):


    def __init__(self,config_params):
        super(swmm,self).__init__(config_params)

        reldatadir = config_params['data'][0]['directory']
        self.__datadir = join(dirname(realpath(__file__)),reldatadir)
        self.config_params = config_params

        #--- get input and output directories ---
        #cwd = abspath(dirname(__file__))
        #self.exe = join(cwd,'swmm5')
        self.sim_input = join(self.__datadir,config_params['data'][0]['input'])

        # generate random names for inp, rpt, and out
        self.swmm_file_name = config_params['data'][0]['input'].split('.')[0]
        self.__inp = join(self.__datadir,self.swmm_file_name+'.inp')
        self.__rpt = join(self.__datadir,self.swmm_file_name+'.rpt')
        self.__out = join(self.__datadir,self.swmm_file_name+'.out')
        self.__console = open(join(self.__datadir,'console.out'),'w')

        # store swmm geometry list to lookup geoms later on
        self.__geom_lookup = {}

        #--- read input file and build geometries ---
        geoms = self.build_geometries()
        io = self.build_swmm_inputs_and_outputs(geoms)

        # create instance of the SWMM C model
        # todo: get this from the config_params
        self.__swmmLib = CDLL(join(self.__datadir,'libSWMMQOpenMI.dylib'))

        # open input file
        error = self.__swmmLib.swmm_open(self.__inp,self.__rpt,self.__out)
        error = self.__swmmLib.swmm_start(True)

        # get start and end times
        self.set_start_end_from_swmm()

        # todo: start here.  How can I get the timestep value from SWMM?
        # set timestep
        self.__begin_c_time = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('begin'))).value
        self.__end_c_time = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('end'))).value

        #self.time_step(1,'second')

        print 'done with initialize'


    def run_timestep(self,inputs, current_time):

        # get rainfall from inputs
        rainfall_item = inputs['Rainfall']
        rainfall_data = rainfall_item.get_geoms_and_timeseries()



        self.__swmmLib.getObjectTypeCount.restype = c_int
        subcatchment_count = self.__swmmLib.getObjectTypeCount(SWMM_Types.SUBCATCH)
        self.__swmmLib.getSubcatch.restype = POINTER(TSubcatch)
        self.__swmmLib.setSubcatch.argtypes = [POINTER(TSubcatch), c_char_p]
        step = c_double()

        # loop through all of the subcatchments and apply inputs
        for i in range(0,subcatchment_count):

            # get the subcatchment
            sub = self.__swmmLib.getSubcatch(c_int(i))

            # get the subcatchment and geometry ids
            sub_id = sub.contents.ID
            geom_id = self.__geom_lookup[sub_id].id()

            # APPLY RAINFALL

            # get the date and value from inputs, based on geom_id
            date, value = rainfall_item.get_timeseries_by_id(geom_id)

            # set the rainfall value
            if value[0]: sub.contents.rainfall = value[0]
            else: sub.contents.rainfall = c_double(0.0)

                #(None, )


            # apply the rainfall
            self.__swmmLib.setSubcatch(sub,c_char_p('rainfall'))



        print self.__swmmLib.getSubcatch(c_int(0)).contents.newRunoff


        error = self.__swmmLib.swmm_step(byref(step))

        # todo: increment time!
        elapsed = self.__begin_c_time + step.value
        new_time = self.decode_datetime(elapsed)
        increment = new_time - self.current_time()

        if increment.total_seconds() < 0:  # i.e. simulation has completed
            # force the increment to step beyond the simulation end time
            increment = timedelta(0,5)
        self.increment_time(increment)


    def save(self):
        return self.outputs()
        #return [self.get_output_by_name(outputname='Hydraulic_head')]



    def build_swmm_inputs_and_outputs(self, geoms):

        # define the model inputs and outputs
        outputs = {'subcatchment':['Groundwater_outflow','Wash_off_concentration','Groundwater_elevation','Runoff_rate'],
                   'link' : ['Flow_depth','Flow_rate','Flow_velocity'],
                   'node' : ['Volume_stored_ponded','Lateral_inflow','Total_inflow','Depth_above_invert','Hydraulic_head','Flow_lost_flooding']
        }

        inputs = {'subcatchment' : ['Evaporation','Rainfall','Snow_depth'],
                   'link' : ['Froude_number','Capacity'],
                   'node' : []
        }

        # get spatial reference system (use default if none is provided in config)
        srs = spatial.get_srs_from_epsg(code=None)
        if self.config_params.has_key('spatial'):
            if self.config_params['spatial'].has_key('srs'):
                srs = spatial.get_srs_from_epsg(self.config_params['spatial']['srs'])


        # build outputs
        output_items = []
        for key, vars in outputs.iteritems():
            for var_name in vars:

                # build variable and unit
                variable = mdl.create_variable(var_name)
                unit = mdl.create_unit(var_name)

                # build elementset
                geometries = geoms[key]
                elementset = []
                for i, geom in geometries:
                    dv = DataValues()
                    elem = Geometry(geom=geom,id=i)
                    elem.type(geom.geom_type)
                    elem.srs(srs)
                    elem.datavalues(dv)
                    elementset.append(elem)

                    # save the geometry for lookup later
                    self.__geom_lookup[i] = elem


                # create exchange item
                ei = ExchangeItem(id,
                                name=variable.VariableNameCV(),
                                desc=variable.VariableDefinition(),
                                geometry=elementset,
                                unit= unit,
                                variable=variable,
                                type=ExchangeItemType.Output)

                # save the output item
                output_items.append(ei)

        # build inputs
        input_items = []
        for key, vars in inputs.iteritems():
            for var_name in vars:

                # build variable and unit
                variable = mdl.create_variable(var_name)
                unit = mdl.create_unit(var_name)

                # build elementset
                id_inc = 0
                geometries = geoms[key]
                elementset = []
                for i, geom in geometries:
                    dv = DataValues()
                    elem = Geometry(geom=geom,id=id_inc)
                    elem.type(geom.geom_type)
                    elem.srs(srs)
                    elem.datavalues(dv)
                    elementset.append(elem)
                    id_inc += 1

                    # save the geometry for lookup later
                    self.__geom_lookup[i] = elem

                # create exchange item
                ei = ExchangeItem(id,
                                name=variable.VariableNameCV(),
                                desc=variable.VariableDefinition(),
                                geometry=elementset,
                                unit= unit,
                                variable=variable,
                                type=ExchangeItemType.Input)

                # save the output item
                input_items.append(ei)



        # set the input and output items
        self.outputs(value = output_items)
        self.inputs(value = input_items)

    def build_geometries(self):

        # store the geometries based on type
        geoms = {}

        input_file = self.sim_input

        # build catchments
        catchments = swmm_geom.build_catchments(input_file)


        # build rivers
        streams = swmm_geom.build_links(input_file)

        # build nodes
        nodes = swmm_geom.build_nodes(input_file)


        # store the geoms by their type
        geoms['subcatchment'] = catchments
        geoms['link'] = streams
        geoms['node'] = nodes

        return geoms

    # def setup_model(self, inputs):
    #
    #     # open the input file (original)
    #     sim = open(self.sim_input,'r')
    #     in_lines = sim.readlines()
    #
    #     # set the simulation start and end times.
    #     st = self.simulation_start()
    #     et = self.simulation_end()
    #     cidx = self.find(in_lines, lambda x: 'OPTIONS' in x)
    #     i = cidx+1
    #     swmm_opts = {}
    #     for line in in_lines[cidx+1:]:
    #         if line.strip() == '':
    #             break
    #         vals = re.split(' +',line.strip())
    #         swmm_opts[vals[0]] = vals[1]
    #         i += 1
    #
    #     swmm_opts['START_DATE'] = st.strftime('%m/%d/%Y')
    #     swmm_opts['START_TIME'] = st.strftime('%H:%M:%S')
    #     swmm_opts['END_DATE'] = et.strftime('%m/%d/%Y')
    #     swmm_opts['END_TIME'] = et.strftime('%H:%M:%S')
    #     swmm_opts['REPORT_START_DATE'] = st.strftime('%m/%d/%Y')
    #     swmm_opts['REPORT_START_TIME'] = st.strftime('%H:%M:%S')
    #
    #     for j in range(cidx+1,i):
    #         k,v = swmm_opts.popitem()
    #         in_lines[j] = "%s\t%s\n" % (k,v)
    #
    #
    #     # Format rainfall input
    #     for geom, dict in inputs.iteritems():
    #         if 'Rainfall' in dict:
    #             in_lines = self.set_rainfall_input(in_lines,dict['Rainfall'])
    #
    #     # write simulation specific input file
    #     f = open(self.inp,'w')
    #     for line in in_lines:
    #         f.write(line)
    #     f.close()



    def find(self, lst, predicate):
        return (i for i, j in enumerate(lst) if predicate(j)).next()


    def decode_datetime(self, time):
        year = c_int(0)
        month = c_int(0)
        day = c_int(0)
        hour = c_int(0)
        minute = c_int(0)
        second = c_int(0)

        self.__swmmLib.datetime_decodeDateTime(c_double(time), byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))

        return datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)


    def set_start_end_from_swmm(self):
        year = c_int(0)
        month = c_int(0)
        day = c_int(0)
        hour = c_int(0)
        minute = c_int(0)
        second = c_int(0)

        self.__swmmLib.swmm_getDateTime.restype = c_double
        begin = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('begin')))
        end = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('end')))

        self.__swmmLib.datetime_decodeDateTime(end, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        end_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        self.__swmmLib.datetime_decodeDateTime(begin, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        begin_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        self.simulation_start(value=begin_time)
        self.simulation_end(value=end_time)