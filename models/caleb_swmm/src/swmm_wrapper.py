__author__ = 'tonycastronova'

from os.path import *
import uuid
import re
from datetime import datetime
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

            # get the date and value from inputs, based on geom_id
            date, value = rainfall_item.get_timeseries_by_id(geom_id)

            # set the rainfall value
            sub.contents.rainfall = value[0]

            # apply the rainfall
            self.__swmmLib.setSubcatch(sub,c_char_p('rainfall'))

        error = self.__swmmLib.swmm_step(byref(step))

        # todo: increment time!
        elapsed = self.__begin_c_time + step.value
        new_time = self.decode_datetime(elapsed)
        increment = new_time - self.current_time()
        self.increment_time(increment)


        # # setup input file for simulation
        # self.setup_model(inputs)
        #
        # # todo: use input rainfall to write inp file
        #
        #
        # # run the simulation
        # subprocess.call([self.exe,self.inp,self.rpt,self.out], stdout=self.console)
        #
        # # set exchange item results from output file
        # l = ps.list(self.out)
        #
        # vars = ps.listvariables(self.out)
        #
        # links = ps.listdetail(self.out,'link')
        # nodes = ps.listdetail(self.out,'node')
        # catchments = ps.listdetail(self.out,'subcatchment')
        #
        # #link_= ps.getdata(self.out,items)
        # node_head = ps.getdata(self.out, ['node,'+N['Name']+',1' for N in nodes])
        # node_flow = ps.getdata(self.out, ['node,'+N['Name']+',4' for N in nodes])
        # link_frate = ps.getdata(self.out, ['link,'+L['Name']+',0' for L in links])
        # link_depth = ps.getdata(self.out, ['link,'+L['Name']+',1' for L in links])
        #
        # # get the stage output exchange item
        # stage = self.get_output_by_name('Hydraulic_head')
        #
        # # set the output results to each geometry
        # for geom in stage.geometries():
        #     id = geom.id()
        #     geom.datavalues().set_timeseries(node_head[id])
        #
        # self.outputs(name='Hydraulic_head', value=stage)
        #
        # return 1


    def save(self):
        pass
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

    def build_swmm_geoms(self,inp,type):
        lines = None
        with open(inp,'r') as f:
            lines = f.readlines()


        # first read all the node coordinates
        nodes = {}
        node_order = []
        cidx = self.find(lines, lambda x: 'COORDINATES' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())
            nodes[vals[0]] = (float(vals[1]), float(vals[2]))
            node_order.append(vals[0])


        idx = self.find(lines, lambda x: type.upper() in x)
        geoms = []
        links = {}
        prev_id = None
        # build line objects
        if type == 'vertices':
            for line in lines[idx+3:]:
                if line.strip() == '':
                    break

                vals = re.split(' +',line.strip())
                name = vals[0]
                x = float(vals[1])
                y = float(vals[2])

                if name != prev_id:
                    # save endnode for previous id
                    if prev_id is not None:
                        links[prev_id].append(nodes[node_order[node_order.index(prev_id)]])

                    # save the startnode for the current id
                    links[name] = [nodes[node_order[node_order.index(name)-1]]]
                    prev_id = name

                # save each of the coordinates in the link
                links[name].append((x,y))

        for link,coords in links.iteritems():
            geoms.append((link,LineString(coords)))



        return geoms

    def setup_model(self, inputs):

        # open the input file (original)
        sim = open(self.sim_input,'r')
        in_lines = sim.readlines()

        # set the simulation start and end times.
        st = self.simulation_start()
        et = self.simulation_end()
        cidx = self.find(in_lines, lambda x: 'OPTIONS' in x)
        i = cidx+1
        swmm_opts = {}
        for line in in_lines[cidx+1:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())
            swmm_opts[vals[0]] = vals[1]
            i += 1

        swmm_opts['START_DATE'] = st.strftime('%m/%d/%Y')
        swmm_opts['START_TIME'] = st.strftime('%H:%M:%S')
        swmm_opts['END_DATE'] = et.strftime('%m/%d/%Y')
        swmm_opts['END_TIME'] = et.strftime('%H:%M:%S')
        swmm_opts['REPORT_START_DATE'] = st.strftime('%m/%d/%Y')
        swmm_opts['REPORT_START_TIME'] = st.strftime('%H:%M:%S')

        for j in range(cidx+1,i):
            k,v = swmm_opts.popitem()
            in_lines[j] = "%s\t%s\n" % (k,v)


        # Format rainfall input
        for geom, dict in inputs.iteritems():
            if 'Rainfall' in dict:
                in_lines = self.set_rainfall_input(in_lines,dict['Rainfall'])

        # write simulation specific input file
        f = open(self.inp,'w')
        for line in in_lines:
            f.write(line)
        f.close()

    def set_rainfall_input(self, in_lines, precip):

        # get the time series associated with the input exchange item
        #geom, eitem = inputs.items()[0]
        #data = eitem.values()[0]
        d, v = precip.get_dates_values()
        dates = list(d)
        values = list(v)

        # map the rain gages to the catchments
        cidx = self.find(in_lines, lambda x: 'SUBCATCHMENTS' in x) + 4
        i = 0
        for line in in_lines[cidx:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())
            vals[1] = 'rain_gage_data'
            vals.append('\n')
            in_lines[cidx + i]  = '\t'.join(vals)

            i += 1



        # timeseries values must be relative to the start of the swmm simulation
        offset = (self.simulation_start() - dates[0]).total_seconds()
        for i in xrange(0, len(dates)):
            dates[i] -= datetime.timedelta(seconds=offset)

        # add a raingage
        in_lines.append('\n[RAINGAGES]\n')
        in_lines.append(';;;\n')
        in_lines.append(';;Name           Type      Intrvl Catch  Source\n')
        in_lines.append(';;-------------- --------- ------ ------ ----------\n')
        in_lines.append('rain_gage_data  CUMULATIVE 0:01   1.0    TIMESERIES precipitation\n')

        # write the rainfall data
        in_lines.append('\n[TIMESERIES\n')
        in_lines.append(';;Name           Date       Time       Value   \n')
        in_lines.append(';;-------------- ---------- ---------- ----------\n')
        for i in xrange(0, len(dates)):
            in_lines.append('precipitation\t%s\t%s\t%2.3f\n' %(dates[i].strftime('%m/%d/%Y'), dates[i].strftime('%H:%M'),values[i]))

        return in_lines


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