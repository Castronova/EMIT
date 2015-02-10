__author__ = 'tonycastronova'

from os.path import *
import uuid
import re
from datetime import datetime, timedelta
from ctypes import *
import os

from shapely.geometry import *
from stdlib import Geometry, DataValues, ExchangeItem, ExchangeItemType
from wrappers.time_step import time_step_wrapper
from utilities import mdl, spatial

import sys

#import parse_swmm as ps
import geometry as swmm_geom
from structures import *


class swmm(time_step_wrapper):


    def __init__(self,config_params):
        super(swmm,self).__init__(config_params)

        reldatadir = config_params['data'][0]['directory']
        self.__datadir = join(dirname(realpath(__file__)),reldatadir)
        self.config_params = config_params

        # get input and output directories
        self.sim_input = join(self.__datadir,config_params['data'][0]['input'])
        self.swmm_file_name = config_params['data'][0]['input'].split('.')[0]
        self.__inp = join(self.__datadir,self.swmm_file_name+'.inp')
        self.__rpt = join(self.__datadir,self.swmm_file_name+'.rpt')
        self.__out = join(self.__datadir,self.swmm_file_name+'.out')
        self.__console = open(join(self.__datadir,'console.out'),'w')
        self.__dll = config_params['software'][0]['library']   # relative path to dll

        self.__geom_lookup = {}     # for mapping between swmm geometry ids and exchange item ids
        self.__geom_atts = {}       # for storing geomerty attributes (e.g. to and from nodes)


        #--- read input file and build geometries ---
        geoms = self.build_geometries()
        io = self.build_swmm_inputs_and_outputs(geoms)

        # create instance of the SWMM C model
        # todo: get this from the config_params
        # self.__swmmLib = CDLL(join(self.__datadir,'libSWMMQOpenMI.dylib'))
        self.__swmmLib = cdll.LoadLibrary(join(os.path.dirname(__file__),self.__dll))

        # set input and output CTYPES (GENERAL)
        self.__swmmLib.swmm_open.restype = POINTER(c_void_p)
        self.__swmmLib.getObjectTypeCount.restype = c_int
        self.__swmmLib.swmm_getDateTime.restype = c_double

        # set input and output CTYPES (SUBCATCH)
        self.__swmmLib.getSubcatch.restype = POINTER(TSubcatch)
        self.__swmmLib.setSubcatch.argtypes = [POINTER(c_void_p), POINTER(TSubcatch), c_char_p]

        # set input and output CTYPES (LINK)
        self.__swmmLib.getLink.restype = POINTER(TLink)
        self.__swmmLib.setLink.argtypes = [POINTER(c_void_p), POINTER(TLink), c_char_p]

        # set input and output CTYPES (NODE)

        self.__swmmLib.getNode.restype = POINTER(TNode)
        self.__swmmLib.setNode.argtypes = [POINTER(c_void_p), POINTER(TNode), c_char_p]
        self.__swmmLib.getNodeById.restype = POINTER(TNode)
        self.__swmmLib.getNodeById.argtypes = [POINTER(c_void_p), c_char_p]

        # open input file
        self.ptr = self.__swmmLib.swmm_open(self.__inp,self.__rpt,self.__out)
        err = self.__swmmLib.swmm_getErrorCode(self.ptr)

        error = self.__swmmLib.swmm_start(self.ptr, True)
        err = self.__swmmLib.swmm_getErrorCode(self.ptr)

        # get geometry info about the SWMM project
        self.subcatchment_count = self.__swmmLib.getObjectTypeCount(self.ptr, SWMM_Types.SUBCATCH)
        self.link_count = self.__swmmLib.getObjectTypeCount(self.ptr, SWMM_Types.LINK)
        self.node_count = self.__swmmLib.getObjectTypeCount(self.ptr, SWMM_Types.NODE)

        # get start and end times
        self.set_start_end_from_swmm(self.ptr)

        # todo: start here.  How can I get the timestep value from SWMM?
        # set timestep
        self.__begin_c_time = c_double( self.__swmmLib.swmm_getDateTime(self.ptr, c_char_p('begin'))).value
        self.__end_c_time = c_double( self.__swmmLib.swmm_getDateTime(self.ptr, c_char_p('end'))).value
        self.__step = c_double()

        #self.time_step(1,'second')

        print 'done with initialize'


    def run_timestep(self,inputs, current_time):

        # get catchment inputs
        rainfall_data = inputs['Rainfall'].get_geoms_and_timeseries()
        evaporation = inputs['Evaporation'].get_geoms_and_timeseries()
        snow = inputs['Snow_depth'].get_geoms_and_timeseries()

        # get link inputs
        flow_rate = inputs['Flow_rate'].get_geoms_and_timeseries()

        # get node inputs
        stage = inputs['Hydraulic_head'].get_geoms_and_timeseries()

        # check to see which inputs will be applied (i.e. values are provided)
        apply_rainfall = True if len([v for g in rainfall_data.keys() for v in rainfall_data[g] if v is not None]) > 0 else False
        apply_evaporation = True if len([v for g in evaporation.keys() for v in evaporation[g] if v is not None]) > 0 else False
        apply_snow = True if len([v for g in snow.keys() for v in snow[g] if v is not None]) > 0 else False
        apply_flowrate = True if len([v for g in flow_rate.keys() for v in flow_rate[g] if v is not None]) > 0 else False
        apply_stage = True if len([v for g in stage.keys() for v in stage[g] if v is not None]) > 0 else False

        has_catchment_input = True if True in [apply_rainfall,apply_evaporation,apply_snow] else False
        has_link_input = True if True in [apply_flowrate] else False
        has_node_input = True if True in [apply_stage] else False


        sys.stdout.write(' - - > HasRainfall = %s | HasFlow = %s | HasStage = %s\n'
                         % (apply_rainfall,
                            apply_flowrate,
                            apply_stage))

        # ----------------
        # Catchment Inputs
        # ----------------

        if has_catchment_input:

            # loop through all of the subcatchments and apply inputs
            for i in range(0,self.subcatchment_count):

                # get the subcatchment
                sub = self.__swmmLib.getSubcatch(self.ptr, c_int(i))

                # get the subcatchment and geometry ids
                sub_id = sub.contents.ID
                geom_id = self.__geom_lookup[sub_id].id()

                # APPLY RAINFALL if values are given (i.e. not all None)
                if apply_rainfall:

                    # get the date and value from inputs, based on geom_id
                    date, value = inputs['Rainfall'].get_timeseries_by_id(geom_id)

                    # set the rainfall value
                    if value[0]: sub.contents.rainfall = value[0]
                    else: sub.contents.rainfall = c_double(0.0)

                    self.__swmmLib.setSubcatch(self.ptr, sub, c_char_p('rainfall'))

                if apply_evaporation:
                    # todo: implement this

                    self.__swmmLib.setSubcatch(self.ptr, sub,c_char_p('evapLoss'))
                    pass

                if apply_snow:
                    # todo: implement this

                    self.__swmmLib.setSubcatch(self.ptr, sub,c_char_p('newSnowDepth'))
                    pass




        # ------------
        # Link Inputs
        # ------------
        if has_link_input:

            # loop through the links and apply inputs
            for i in range(0, self.link_count):


                # get the current link
                l = self.__swmmLib.getLink(self.ptr, c_int(i))

                # get the geom id
                link_id = l.contents.ID
                if link_id in self.__geom_lookup:
                    geom_id = self.__geom_lookup[link_id].id()
                    att = self.__geom_atts[link_id]

                    # get input and output node ids
                    in_node_id = att['inlet']
                    out_node_id = att['outlet']

                    # APPLY STREAMFLOW if values are given (i.e. not all None)
                    if apply_flowrate:

                        # get the date and value from inputs, based on geom_id
                        date, value = inputs['Flow_rate'].get_timeseries_by_id(geom_id)

                        node = self.__swmmLib.getNodeById(self.ptr, c_char_p(out_node_id))

                        # apply flowrate at outlets
                        if value[0]: node.contents.inflow = value[0]
                        else: node.contents.inflow = c_double(0.0)

                        self.__swmmLib.setNode(self.ptr, node, c_char_p('inflow'))

        # ------------
        # Node Inputs
        # ------------
        # todo: implement this
        if has_node_input:
            pass



        # for debugging only
        #print self.__swmmLib.getSubcatch(self.ptr, c_int(0)).contents.newRunoff

        # step the SWMM simulation
        error = self.__swmmLib.swmm_step(self.ptr, byref(self.__step))

        # track the new time within the SWMM wrapper
        elapsed = self.__begin_c_time + self.__step.value
        new_time = self.decode_datetime(elapsed)
        increment = new_time - self.current_time()

        if increment.total_seconds() < 0:  # i.e. simulation has completed
            # force the increment to step beyond the simulation end time
            increment = timedelta(0,5)
        self.increment_time(increment)

        # set link outputs
        for i in range(0, self.link_count):

            l = self.__swmmLib.getLink(self.ptr, c_int(i))

            # get the geom id
            link_id = l.contents.ID

            if link_id in self.__geom_lookup:
                geom= self.__geom_lookup[link_id]

                # get new flow
                f = self.__swmmLib.getLink(self.ptr, c_int(i)).contents.newFlow

                # set geometry values
                self.set_geom_values_by_hash('Flow_rate',geom,zip([new_time],[f]))


        for i in range(0, self.node_count):
            n = self.__swmmLib.getNode(self.ptr, c_int(i))
            node_id = n.contents.ID
            if node_id in self.__geom_lookup:
                geom = self.__geom_lookup[node_id]
                depth = n.contents.newDepth
                self.set_geom_values_by_hash('Hydraulic_head',geom, zip([new_time],[depth]))


        msg = 'Done with PTS'

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
                   'link' : ['Froude_number','Capacity','Flow_rate','Flow_velocity'],
                   'node' : ['Lateral_inflow','Hydraulic_head']
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
                for i, v in geometries.iteritems():
                    geom = v['geometry']
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
                for i, v in geometries.iteritems():
                    geom = v['geometry']
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


        # populate geometry attributes lookup table
        for k,v in dict(catchments.items() + streams.items() + nodes.items()).iteritems():
            self.__geom_atts[k] = v


        return geoms

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

    def set_start_end_from_swmm(self,ptr):
        year = c_int(0)
        month = c_int(0)
        day = c_int(0)
        hour = c_int(0)
        minute = c_int(0)
        second = c_int(0)

        begin = c_double( self.__swmmLib.swmm_getDateTime(ptr, c_char_p('begin')))
        end = c_double( self.__swmmLib.swmm_getDateTime(ptr, c_char_p('end')))

        self.__swmmLib.datetime_decodeDateTime(end, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        end_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        self.__swmmLib.datetime_decodeDateTime(begin, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        begin_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        self.simulation_start(value=begin_time)
        self.simulation_end(value=end_time)