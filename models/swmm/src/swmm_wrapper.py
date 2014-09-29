__author__ = 'tonycastronova'

from os.path import *
import subprocess
import uuid
import re
import datetime

from shapely.geometry import *

from stdlib import Geometry, DataValues, ExchangeItem, ExchangeItemType
import parse_swmm as ps
from wrappers.feed_forward import feed_forward_wrapper
from utilities import mdl
import geometry as swmm_geom

"""
NOTES:
* .mdl must have a 'data' section which includes a 'directory' key providing the path to the swmm inputs/outputs
"""

class swmm(feed_forward_wrapper):


    def __init__(self,config_params):
        super(swmm,self).__init__(config_params)

        reldatadir = config_params['data'][0]['directory']
        self.__datadir = join(dirname(realpath(__file__)),reldatadir)


        #--- get input and output directories ---
        cwd = abspath(dirname(__file__))
        self.exe = join(cwd,'swmm5')
        self.sim_input = join(self.__datadir,config_params['data'][0]['input'])

        # generate random names for inp, rpt, and out
        self.swmm_file_name = uuid.uuid4().hex[:5]
        self.inp = join(self.__datadir,self.swmm_file_name+'.inp')
        self.rpt = join(self.__datadir,self.swmm_file_name+'.rpt')
        self.out = join(self.__datadir,self.swmm_file_name+'.out')
        self.console = open(join(self.__datadir,'console.out'),'w')

        #--- read input file and build geometries ---

        # build link geometries
        #geoms = self.build_swmm_geoms(self.sim_input,'vertices')

        geoms = self.build_geometries()
        io = self.build_swmm_inputs_and_outputs(geoms)

        # build inputs and outputs from inp file


        # # add link geometries to stage exchange item
        # for geom_name, geoms in geoms.iteritems():
        #
        #     elements = []
        #     for geom in geoms:
        #         dv = DataValues()
        #         elem = Geometry(geom=geom,id=link)
        #         elem.type(geom.geom_type)
        #         elem.srs(None)
        #         elem.datavalues(dv)
        #         elements.append(elem)



        # todo: only build the geometry if it is defined in the config
        # save the inputs and outputs to the exchange items

        # outputs = self.outputs()
        # for o in outputs:
        #     name = o.name()
        #
        #     # set the geometry for hydraulic head
        #     if name == 'Hydraulic_head':
        #
        # stage = self.get_output_by_name('Hydraulic_head')
        # stage.add_geometry(elements)


        print 'done with initialize'


    def run(self,inputs):

        # setup input file for simulation
        self.setup_model(inputs)

        # todo: use input rainfall to write inp file


        # run the simulation
        subprocess.call([self.exe,self.inp,self.rpt,self.out], stdout=self.console)

        # set exchange item results from output file
        l = ps.list(self.out)

        vars = ps.listvariables(self.out)

        links = ps.listdetail(self.out,'link')
        nodes = ps.listdetail(self.out,'node')
        catchments = ps.listdetail(self.out,'subcatchment')

        #flow = ps.getdata(out,'link:Flow_rate')

        #for l in links:
        #    print '%s, %s, %s, %s, %s, %s'%\
        #          (l['Name'],l['Type'],l['Inv_offset'],l['Inv_offset'],l['Max_depth'],l['Length'])

        #link_= ps.getdata(self.out,items)
        node_head = ps.getdata(self.out, ['node,'+N['Name']+',1' for N in nodes])
        node_flow = ps.getdata(self.out, ['node,'+N['Name']+',4' for N in nodes])
        link_frate = ps.getdata(self.out, ['link,'+L['Name']+',0' for L in links])
        link_depth = ps.getdata(self.out, ['link,'+L['Name']+',1' for L in links])

        #catchment_data =
        #['link,1,1']


        # get the stage output exchange item
        stage = self.get_output_by_name('Hydraulic_head')

        # set the output results to each geometry
        for geom in stage.geometries():
            id = geom.id()
            geom.datavalues().set_timeseries(node_head[id])

            self.outputs()

        return 1


    def save(self):
        return self.outputs()



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
                    elem.srs(None)
                    elem.datavalues(dv)
                    elementset.append(elem)


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
                    elem.srs(None)
                    elem.datavalues(dv)
                    elementset.append(elem)
                    id_inc += 1


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


