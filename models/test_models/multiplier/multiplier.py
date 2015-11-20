__author__ = 'tonycastronova'


from wrappers import feed_forward
import stdlib
from utilities import mdl
from coordinator.emitLogging import elog

class multiply(feed_forward.feed_forward_wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """

        super(multiply,self).__init__(config_params)


        # build inputs and outputs
        io = mdl.build_exchange_items_from_config(config_params)

        # set inputs and outputs
        self.inputs(value=io[stdlib.ExchangeItemType.INPUT])
        self.outputs(value=io[stdlib.ExchangeItemType.OUTPUT])


    def run(self,inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        iei = inputs['some_value']
        indices, dates = zip(*iei.getDates2())

        new_vals = []
        for idx in indices:

            # get all values for this date/time index
            values = iei.getValues2(time_idx=idx)

            for geom_idx in range(0, len(values)):
                values[geom_idx] = values[geom_idx]**2
            new_vals.append(values)

        # set these new values
        oei_name = self.outputs().keys()[0]
        oei = self.outputs()[oei_name]
        oei.setValues2(values=new_vals, timevalue=dates)



    def save(self):
        return self.outputs()


