__author__ = 'tonycastronova'

from os.path import *

import subprocess

from shapely.geometry import *
from stdlib import Geometry, DataValues
import parse_swmm as ps
from wrappers.feed_forward import feed_forward_wrapper
import uuid
import re

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
        link_geoms = self.build_swmm_geoms(self.sim_input,'vertices')

        # get the stage output exchange item
        stage = self.get_output_by_name('Hydraulic_head')

        # add link geometries to stage exchange item
        elems = []
        for link, geom in link_geoms:
            dv = DataValues()
            elem = Geometry(geom=geom,id=link)
            elem.type(geom.geom_type)
            elem.srs(None)
            elem.datavalues(dv)
            elems.append(elem)
        stage.add_geometry(elems)


    def run(self,inputs):

        # todo: use input rainfall to write inp file
        self.set_rainfall_input(inputs)


        # run the simulation
        subprocess.call([self.exe,self.inp,self.rpt,self.out], stdout=self.console)

        # set exchange item results from output file
        l = ps.list(self.out)

        vars = ps.listvariables(self.out)

        links = ps.listdetail(self.out,'link')
        #flow = ps.getdata(out,'link:Flow_rate')

        #for l in links:
        #    print '%s, %s, %s, %s, %s, %s'%\
        #          (l['Name'],l['Type'],l['Inv_offset'],l['Inv_offset'],l['Max_depth'],l['Length'])

        items = ['link,'+L['Name']+',1' for L in links]
        data = ps.getdata(self.out,items)
        #['link,1,1']


        # get the stage output exchange item
        stage = self.get_output_by_name('Hydraulic_head')

        # set the output results to each geometry
        for geom in stage.geometries():
            id = geom.id()
            geom.datavalues().set_timeseries(data[id])



        return 1



    def save(self):
        return self.outputs()


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


    def set_rainfall_input(self, inputs):

        '''
        [RAINGAGES]
        ;;               Rain      Time   Snow   Data
        ;;Name           Type      Intrvl Catch  Source
        ;;-------------- --------- ------ ------ ----------
        300_main_street  CUMULATIVE 0:01   1.0    TIMESERIES 300_main_st_7_11_2012
        '''

        # open the input file (original)
        sim = open(self.sim_input,'r')
        in_lines = sim.readall()

        # write simulation specific input file
        f = open(self.inp,'w')
        f.write(in_lines)





    def find(self, lst, predicate):
        return (i for i, j in enumerate(lst) if predicate(j)).next()
