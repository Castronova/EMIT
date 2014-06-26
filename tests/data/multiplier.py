__author__ = 'tonycastronova'


from wrappers import feed_forward
import stdlib

class multiply(feed_forward.feed_forward_wrapper):


    def __init__(self,config_params):
        """
        initialization that will occur when loaded into a configuration

        """

        super(multiply,self).__init__(config_params)


    def run(self,inputs):
        """
        This is an abstract method that must be implemented.
        :param exchangeitems: list of input exchange items
        :return: true
        """

        # loop through each geometry
        for geom, dataset in inputs.iteritems():

            time = self.current_time()

            ts = []
            while time <= self.simulation_end():


                # data for desired variable (e.g. 'some_value')
                datavalues = dataset['some_value']
                dates, values = datavalues.get_dates_values()

                # get value at required time
                # todo: have these values already temporally mapped, so that this isn't necessary here
                closest_date = min(dates,key=lambda date : abs(time-date))
                idx = dates.index(closest_date)

                # get value at this location / time
                value = values[idx]


                # perform computation
                new_value = value**2

                # save this new value in a timeseries
                ts.append((time,new_value))

                # increment time
                time = self.increment_time(time)


            # save results to this geometry as an output variable
            self.set_geom_values('multipliedValue',geom,ts)




        # # todo: some sort of automatic geometry mapping (utilites.py)



    def save(self):
        return self.outputs()


