import math
import numpy as np
import stdlib
from emitLogging import elog
from sprint import *
from utilities import mdl, geometry
from wrappers import feed_forward
import datetime
import shutil

# make sure that the win32com library is installed. This is required for weap to run.
try:
    import win32com.client as com
except:
    msg = 'Error loading WEAP model, missing required library: Win32com.'
    msg_ext = 'This can be installed by issuing the following command:\n\t"pip install pypiwin32"\n'
    sPrint(msg+msg_ext, MessageType.CRITICAL)
    elog.critical(msg)
    raise Exception(msg)


class weap(feed_forward.Wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """
        super(weap,self).__init__(config_params)
        sPrint('WEAP Model - Begin Component Initialization')

        # open WEAP via COM
        try:

            self.weap_model = com.Dispatch("WEAP.WEAPApplication")
            self.weap_model.Visible = 0
        except:
            msg = 'Failed to load the WEAP application.  Make sure that WEAP is installed and running correctly on your machine before proceeding'
            elog.error(msg)
            raise Exception(msg)

        sPrint('..parsing model inputs')
        model_inputs = self.get_model_inputs(config_params)
        # move the input weap dir into the weap AreasDirectoryPath
        area_path = model_inputs['area_path']
        active_area = model_inputs['active_area']
        destPath = os.path.join(self.weap_model.AreasDirectory, active_area)
        sPrint('..moving model files in weap working directory')
        if os.path.exists(destPath):
            shutil.rmtree(destPath)
        os.mkdir(destPath)
        def copytree(src, dst):
            for item in os.listdir(model_inputs['area_path']):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
        copytree(area_path, destPath)

        # close and restart the weap model for the changes to take effect
        del self.weap_model
        self.weap_model = com.Dispatch("WEAP.WEAPApplication")

        # set the active area for the model
        self.weap_model.ActiveArea = active_area


        # get start, end, timestep info from weap instance
        self.start_year = self.weap_model.BaseYear
        self.end_year = self.weap_model.EndYear
        self.first_step = self.weap_model.FirstTimestep
        self.num_steps = self.weap_model.NumTimeSteps
        sPrint('..simulation timespan %d - %d' % (self.start_year, self.end_year))
        sPrint('..first timestep = %d, total timesteps per year %d' % (self.first_step, self.num_steps))


        # collect all the branch names
        sPrint('..collecting variable names')
        self.variables = {}
        for b in self.weap_model.Branches:
            for v in b.Variables:
                if v.IsResultVariable:
                    v_name = v.Name
                    if v_name in self.variables:
                        self.variables[v_name].append(b.FullName)
                    else:
                        self.variables[v_name] = [b.FullName]




        # build inputs and outputs
        # sPrint('..building exchange items')
        # io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        # self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        # self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])

        # model_inputs
        # inputs = config_params['model inputs'][0]

        # read input parameters
        # sPrint('..reading input parameters')


        # sPrint('..building input/output geometries')

        sPrint('..component initialization completed successfully')

    def run(self,inputs):
        sPrint('WEAP Model - Begin Run')

        self.output_calcs = []
        self.output_dates = []

        # perform calculation
        for current_year in range(self.start_year, self.end_year):

            sPrint('..executing year %s' % current_year)

            # change the base year
            self.weap_model.BaseYear = current_year

            self.weap_model.Calculate(self.weap_model.BaseYear, self.num_steps)

            for ts in range(self.first_step, self.num_steps):
                value = weap.ResultValue('Supply and Resources\\River\\Blue River\\Reaches\\Below Return Flow from Ind East:Streamflow',
                                         current_year, ts)
                self.output_calcs.append(value)
                self.output_dates.append(datetime.datetime(current_year, ts, 1))

        sPrint('..simulation completed successfully')

    def finish(self):
        sPrint('WEAP Model - Begin Finish')

        # print output
        for i in range(len(self.output_calcs)):
            msg = '.. %s \t %3.5f' % (self.output_dates[i].strftime('%m-%d-%Y'), self.output_calcs[i])
            sPrint(msg)


        # reset the active area to ensure that WEAP opens corectly next time
        sPrint('..resetting WEAP simulation parameters')
        self.weap_model.ActiveArea = 'Tutorial'
        self.weap_model.Visible = 0
        self.weap_model.Area
        del self.weap_model

        sPrint('..finish completed successfully')


    def get_model_inputs(self, config_params):
        return config_params['model inputs'][0]