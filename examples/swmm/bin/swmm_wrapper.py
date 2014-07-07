__author__ = 'tonycastronova'


import parse_swmm as ps
from wrappers.feed_forward import feed_forward_wrapper





import os


class swmm_wrapper(feed_forward_wrapper):

    def __init__(self,config_params):
        super(feed_forward_wrapper,self).__init__(config_params)

        reldatadir = config_params['data'][0]['directory']
        self.datadir(os.path.join(os.path.dirname(os.path.realpath(__file__)),reldatadir))

    def run(self,inputs):


        

        pass



    def save(self):
        """
            returns a list of data objects that will be saved to the database

            This method is called by the coordinator when simulation is complete and data will be saved to the simulations database
        """

        #
        data = self.data_directory()
        parse = ps.SwmmExtract(data+'/sim.out')



# wrapper = swmm_wrapper()
# data = wrapper.data_directory()
# print ps.list(data+'/sim.out')
# print ps.listdetail(data+'/sim.out',type='subcatchment')
# print ps.listvariables(data+'/sim.out')
#
#
#
# #wrapper.save()
# print 'done'