import time

__author__ = 'tonycastronova'

from wrappers import feed_forward
from utilities import mdl
import stdlib

class slowloading(feed_forward.Wrapper):

    def __init__(self,config_params):
        super(slowloading, self).__init__(config_params)

        print "begin loading module"
        # loop designed to cause slow initialization

        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)
        self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])

        cnt = 0
        for i in range(0, 50000000):
            cnt += i
        print "Done loading module"

    def run(self, inputs):
        pass
